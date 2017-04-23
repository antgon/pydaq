#! /usr/bin/env python3
# coding=utf-8
#
# Copyright (c) 2016-2017 Antonio González
#
# This file is part of pydaq.
#
# Pydaq is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# Pydaq is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
# for more details.
#
# You should have received a copy of the GNU General Public License
# along with pydaq. If not, see <http://www.gnu.org/licenses/>.

import os
import time
import threading
from collections import deque

from serial import (Serial, SerialException)
from serial.tools import list_ports
import numpy as np

from edfrw import (SubjectId, RecordingId, Signal, EdfWriter)

# Arduino baud rates, according to https://www.arduino.cc/en/Serial
# /Begin: 300, 600, 1200, 2400, 4800, 9600, 14400, 19200, 28800, 38400,
# 57600, 115200
#
# mbed supported baud rates: 110, 300, 600, 1200, 2400, 4800, 9600,
# 14400, 19200, 38400, 57600, 115200, 230400, 460800, 921600 (Source:
# https://developer.mbed.org/forum/mbed/topic/893/?page=1#comment-4526)
#
# It makes sense to only allow some of these.
BAUD_RATES = (115200, 57600, 38400, 19200, 14400, 9600)


def print_ports():
    '''
    Utility function for displaying available serial ports.

    Example:

    >>> print_ports()
    manufacturer : None
    device       : /dev/ttyS0
    product      : None
    '''
    properties = ['manufacturer', 'device', 'product']
    for port in list_ports.comports():
        for prop in properties:
            print('{:<13}: {}'.format(prop, port.__dict__[prop]))
        print()


class Configuration(object):
    """
    Configuration parameters for data acquisition.

    baud : :obj:`uint`
        Baud rate for communicating with the MCU.
    sampling_freq :  :obj:`uint`
        Sampling frequency in Hz.
    working_dir : :obj:`str`
        Directory where data files will be saved. Defaults to ``'.'``.
    signals : :obj:`list` of :obj:`edfrw.Signal`
        List of signals to acquire. The contents must match those
        signals expected from the MCU.
    saving_period_s : :obj:`int`
        How often (seconds) are data samples saved to disk. Defaults
        to 5 seconds.
    """
    def __init__(self, baud, sampling_freq, working_dir='.',
                 signals=[], saving_period_s=5):
        self.baud = baud
        self.sampling_freq = sampling_freq
        self.working_dir = working_dir
        self.signals = signals
        self.saving_period_s = saving_period_s

    @property
    def baud(self):
        '''
        Baud rate used for communicating with the microcontroller.
        '''
        return self._baud

    @baud.setter
    def baud(self, value):
        if value not in BAUD_RATES:
            raise ValueError(
                    'Baud rate {} is not supported'.format(value))
        self._baud = value

    @property
    def working_dir(self):
        '''
        Directory where data files will be saved.
        '''
        return self._working_dir

    @working_dir.setter
    def working_dir(self, path):
        if path == '.':
            self._working_dir = os.getcwd()
        else:
            if not os.path.exists(path):
                raise ValueError('Path {} does not exist'.format(path))
            self._working_dir = path

    @property
    def signals(self):
        '''
        List of signals.

        Each element of the list must be of class edfrw.Signal.
        '''
        return self._signals

    @signals.setter
    def signals(self, signals):
        self._signals = signals

    @property
    def nsignals(self):
        '''
        Number of signals (read-only)
        '''
        return len(self._signals)


class MCU(object):
    """
    Microcontroller unit manager.

    manufacturer is a string. If unsure what to use run print_ports()
    after plugging in your microcontroller and check.
    """

    def __init__(self, manufacturer='mbed'):
        self.manufacturer = manufacturer

    def reset(self):
        # Send reset character 'R'.
        self.serial.write(b'R')
        # Empty input buffer.
        self.serial.reset_input_buffer()
        # Wait for a bit and clear again the buffer. This is necessary
        # because when the master buffer is full and then cleared, the
        # mbed sends the contents of its own buffer that were queuing,
        # filling up the input buffer again.
        time.sleep(0.01)
        while self.serial.in_waiting:
            self.serial.reset_input_buffer()

    def connect(self, baud, sampling_freq):
        self.baud = baud
        self.sampling_freq = sampling_freq

        # Find and connect to the microcontroller.
        ports = [port for port in list_ports.comports()]
        manufacturers = [port.manufacturer for port in ports]
        try:
            index = manufacturers.index(self.manufacturer)
        except ValueError:
            raise SerialException('{} not found in serial ports'.format(
                    self.manufacturer))
        self.port = ports[index].device
        self.serial = Serial(port=self.port, baudrate=self.baud,
                             timeout=None)

        time.sleep(0.1)
        self.configure()

    def configure(self):
        # Reset the MCU and input buffer just to be sure.
        self.reset()

        # The microcontroller requires configuration information.
        # This is expected to be a string composed of:
        #  (1) A 'T' (one char)
        #  (2) Datetime in seconds (10 digits)
        #  (3) An 'F' (one char)
        #  (4) sampling frequency in Hz (3 digits)
        #  E.g. T1234567890F100 (15 chars in total)
        self.timestamp = int(time.time())
        cmd = 'T{:d}F{:03d}'.format(self.timestamp, self.sampling_freq)
        cmd = cmd.encode('ascii')
        assert(len(cmd) == 15)
        self.serial.write(cmd)

        # In return, the microcontroller will send back one line of
        # space-separated values: seconds, sampling_freq,
        # output_buffer_size. Check that these match the local
        # configuration. The readline operation is enclosed in a timer
        # to timeout the process if no data are available in the input
        # buffer.
        timer = threading.Timer(3, self.disconnect)
        timer.start()
        confirm = self.serial.readline()
        timer.cancel()

        try:
            confirm = [int(chars) for chars in confirm.split()]
        except ValueError:
            # A value error will occurr if the received data are bytes
            # instead of ascii characters.
            self.disconnect()
            print("Microcontroller's 'confirm': ", confirm)
            raise SerialException(
                    'Microcontroller configuration not received')

        seconds, sampling_freq, buffer_size = confirm

        if (
                (int(seconds) != self.timestamp) or
                (int(sampling_freq) != self.sampling_freq)):
            msg = ('Microcontroller configuration mismatch.' +
                   '\n(MCU time: {}, MCU sampling: {})'.format(
                           seconds, sampling_freq))
            self.disconnect()
            raise SerialException(msg)
        self.buffer_size = int(buffer_size)

    def read(self, nbytes):
        return self.serial.read(nbytes)

    @property
    def in_waiting(self):
        return self.serial.in_waiting

    def disconnect(self):
        #self.reset()
        self.serial.close()


class DataAcquisition(Configuration):

    _start = b'\xff\xff\xff\xff'
    _start_size = 4
    _header_size = 4

    def __init__(self, baud=115200, sampling_freq=100,
                 working_dir='.', signals=[], saving_period_s=5):
        Configuration.__init__(self, baud=baud,
                               sampling_freq=sampling_freq,
                               working_dir=working_dir,
                               signals=signals,
                               saving_period_s=saving_period_s)

        # Public variables
        self.x = None
        self.y = None
        self.mcu = MCU('mbed')

        # Private variables.
        self._edffile = None
        self._iobuffer = None

        # Flags for flow control
        self._read_flag = False

    @property
    def edffile(self):
        if self._edffile is None or self._edffile.closed:
            self._iomaxlen = 0
            self._edffile = None
        return self._edffile

    def open_edf(self, filename, subject_id, recording_id,
                date_time=None):
        filename = os.path.join(self.working_dir, filename)
        self._edffile = EdfWriter(
                filename, subject_id, recording_id,
                signals=self.signals,
                saving_period_s=self.saving_period_s,
                date_time=date_time)
        # Maximum length of input buffer before its data are flushed
        # to disk.
        self._iomaxlen = (
                self.edffile.header.number_of_samples_in_data_record)

    def start(self, seconds=30):
        '''
        Connect and read serial input. Configuration must be done
        beforehand.

        'seconds' is the length of data to keep in self.x and self.y to
        be displayed.
        '''
        # Do nothing if reading is already in progress.
        if self._read_flag is True:
            return

        # Initialise data buffers.
        maxlen = seconds * self.sampling_freq
        self.y = deque([np.ones(self.nsignals) * np.nan],
                       maxlen=maxlen)
        self.x = deque([0], maxlen=maxlen)

        # Connect to microcontroller
        self.mcu.connect(baud=self.baud,
                         sampling_freq=self.sampling_freq)
                         #buffer_size=self.buffer_size)

        # Set flags and start thread for reading data
        self._read_flag = True
        self.lock = threading.Lock()
        self._thread = threading.Thread(target=self._read)
        self._thread.daemon = True
        self._thread.start()

    def stop(self):
        # Do nothing if reading is not in progress.
        if self._read_flag is False:
            return
        self._read_flag = False
        self.y = None
        self.x = None
        self._iobuffer = None
        time.sleep(0.2)
        self.mcu.disconnect()

    def _read(self):
        '''
        Read serial data repeatedly.
        '''
        # By design incoming data samples are two bytes long.
        serial_dtype = np.dtype('uint16')

        # Number of bytes to expect from microcontroller at every
        # iteration (i.e. packet size).
        nbytes = (self._header_size +
                  (self.mcu.buffer_size * serial_dtype.itemsize))

        # Find the header at the start of each data packet. Timeout
        # after 3 seconds if the header is not received.
        timeout = 3
        timer = threading.Timer(timeout, self.stop)
        timer.start()
        start = self.mcu.read(self._start_size)
        while start != self._start:
            start = start[1:] + self.mcu.read(1)
        timer.cancel()

        while self._read_flag:
            # The size of the serial buffer is 4096 (2**12) bytes.
            # Print a warning if we get close to this value. Useful
            # for debugging.
            # if self.serial.bytesAvailable() > 4000:
            # if self.serial.in_waiting > 4000:
            #    print('Warning: buffer overflowing')

            # Wait until the incoming buffer has enough values. Then
            # read serial data.
            while self.mcu.in_waiting < nbytes:
                time.sleep(0.1)
            samples = self.mcu.read(nbytes)

            # The data just read should be the set of samples delimited
            # by the start sequence. Here the data are split into these
            # two groups with `partition`, which - if all is good -
            # should return three items: the samples before the start
            # sequence, the start sequence itself, and the samples after
            # the start sequence. The start sequence was read once
            # before (above), so from now on it will appear at the end
            # of each data set. Thus, `after` should always be empty.
            samples, start, after = samples.partition(self._start)
            assert(len(after) == 0)

            # If the start sequence was not found, `partition` will
            # return an empty start. If that happens top acquiring data.
            if start == b'':
                print('Missing start sequence.')
                self._read_flag = False
            # If all is fine unpack the data and push into buffers as
            # required.
            else:
                # Convert data bytes into required data type (uint16
                # by default).
                samples = np.frombuffer(samples,
                                        dtype=serial_dtype)

                # If the standard buffer is active, add the newly-
                # read samples to it.
                if self.y is not None:
                    y = np.reshape(samples,
                                   (-1, self.nsignals))
                    x = np.arange(len(y)) / self.sampling_freq
                    x = x + self.x[-1] + (1/self.sampling_freq)
                    self.x.extend(x)
                    self.y.extend(y)

                # If the input/output buffer is active, add the
                # newly-read samples to it.
                if self._iobuffer is not None:
                    self._iobuffer.extend(samples)
                    if len(self._iobuffer) == self._iomaxlen:
                        # reshape buffer
                        samples = np.reshape(
                                self._iobuffer,
                                (-1, self.edffile.number_of_signals))
                        samples = samples.flatten(order='F')
                        # write to file
                        self.edffile.write_data_record(samples)
                        self.edffile.flush()
                        # reset buffer
                        self._iobuffer.clear()

    def start_recording(self):
        '''
        Save data to file. requires an open edf file.
        '''
        if self.edffile is None:
            print('Cannot save data. A new EDF file is required.')
            return
        self.stop()
        self._iobuffer = deque()
        self.start()

    def stop_recording(self):
        if self._iobuffer is None:
            return

        # TODO Wait for last data record to be flushed to disk

        self._iobuffer = None
        time.sleep(0.2)
        self.edffile.close()
        self.stop()
