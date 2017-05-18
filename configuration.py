'''
Configuration

Main : Parameters required for the process of acquiring data from the
    microcontroller.

Subject and Record: Information related to the patient and to the
    record characteristics. This infromation is part of the EDF
    specification but it is not required by pydaq: empty fields are OK.

Signals: Describes each of the signals (or channels) that are to be
    acquired. The fields may be empty, but a signal block must exist for
    each signal to be acquired.



1. Save a pydaq.ini file in user's config dir.
    1.1 If no ~/.config/pydaq.ini, make one with default values
    1.2 When pydaq is closed, ~/.config/pydaq.ini is overwriten with
        last config values
    1.3 [Future] This file should also contain
        window params (position , size)
        plot params (line colour, font size, ...)
2. Allow user to load configuration from config.ini file
3. Allow user to save current configuration to a config.ini of their
   choice



Two options seem reasonable: yaml or configparser. The latter is part
of the standard library so no need for extra dependencies.
'''

import os
import configparser
from collections import OrderedDict
from edfrw import (EdfSubjectId, EdfRecordingId, EdfSignal)

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


class Configuration(object):
    """
    Configuration parameters for data acquisition.

    baud : :obj:`uint`
        Baud rate for communicating with the MCU.
    sampling_freq :  :obj:`uint`
        Sampling frequency in Hz.
    working_dir : :obj:`str`
        Directory where data files will be saved. Defaults to ``'.'``.
    signals : :obj:`list` of :obj:`edfrw.EdfSignal`
        List of signals to acquire. The contents must match those
        signals expected from the MCU.
    saving_period_s : :obj:`int`
        How often (seconds) are data samples saved to disk. Defaults
        to 5 seconds.
    """
    def __init__(self, baud=115200, sampling_freq=100, data_path='.',
                 saving_period_s=5, signals=[]):
        self.baud = baud
        self.sampling_freq = sampling_freq
        self.data_path = data_path
        self.saving_period_s = saving_period_s

        self.subject_id = EdfSubjectId()
        self.recording_id = EdfRecordingId()

        if len(signals) == 0:
            signals = [EdfSignal(label = 'Signal ' + str(n+1))
                            for n in range(3)]
        # Each signal must have sampling frequency defined. Pydaq in its
        # current form acquires all signals at the same rate but EDF
        # allows for different sampling rates.
        for signal in signals:
            signal.sampling_freq = self.sampling_freq
        self.signals = signals

        config_dir = os.path.join(os.environ['HOME'], '.config')
        if not os.path.exists(config_dir):
            self._config_f = os.path.join(os.environ['HOME'],
                                         '.pydaq.ini')
        else:
            self._config_f = os.path.join(config_dir, 'pydaq.ini')
        self.load(self._config_f)

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
        else:
            self._baud = value

    @property
    def data_path(self):
        '''
        Directory where data files will be saved.

        Setting an empty path will save data in the user's home
        directory.

        Setting the path as '.' will save data in the current directory.

        Any other path must already exist.
        '''
        return self._data_path

    @data_path.setter
    def data_path(self, path):
        # '.' sets the current working directory as the working_dir.
        if path == '.':
            self._data_path = os.getcwd()
        # an empty string sets home as the working_dir.
        elif path == '':
            self._data_path = os.path.expanduser('~')
        # any other path must already exist.
        else:
            if not os.path.exists(path):
                raise ValueError('Path {} does not exist'.format(path))
            self._data_path = path

    @property
    def nsignals(self):
        '''
        Number of signals (read-only)
        '''
        return len(self.signals)

    @property
    def saving_period_s(self):
        return self._saving_period_s

    @saving_period_s.setter
    def saving_period_s(self, val):
        # Ensure that the saving period is an integer
        self._saving_period_s = int(val)

    def load(self, config_f):
        '''
        Load configuration from file *config_f*.
        '''
        config = configparser.ConfigParser(empty_lines_in_values=False)
        config.read(config_f)
        # config.read works even if config_f does not exist. In that
        # case config.sections() will be an empty list, so the following
        # 'if' statements will fail and thus no configuration will take
        # place, but no errors are raised.

        if 'Main' in config.sections():
            main = config['Main']
            self.baud = main.getint('baud', self.baud)
            self.sampling_freq = main.getint('sampling_freq',
                                             self.sampling_freq)
            self.data_path = main.get('data_path', self.data_path)
            self.saving_period_s = main.getint('saving_period_s',
                                               self.saving_period_s)

        if 'Subject' in config.sections():
            subject = config['Subject']
            code = subject.get('code', 'X')
            sex = subject.get('sex', 'X')
            dob = subject.get('dob', 'X')
            name = subject.get('name', 'X')
            self.subject_id = EdfSubjectId(code, sex, dob, name)

        if 'Recording' in config.sections():
            rec = config['Recording']
            experiment_id = rec.get('experiment_id', 'X')
            investigator_id = rec.get('investigator_id', 'X')
            equipment_code = rec.get('equipment_code', 'X')
            self.recording_id = EdfRecordingId(None, experiment_id,
                                            investigator_id,
                                            equipment_code)

        signal_names = [section for section in config.sections()
                        if section.startswith('Signal')]
        if len(signal_names) > 0:
            self.signals = []
            signal_names.sort()
            for name in signal_names:
                sig = config[name]
                self.signals.append(EdfSignal(
                        label = sig.get('label', ''),
                        transducer_type = sig.get('transducer_type', ''),
                        physical_dim = sig.get('physical_dim', ''),
                        physical_min = sig.getfloat('physical_min', -1),
                        physical_max =  sig.getfloat('physical_max', 1),
                        digital_min =  sig.getint('digital_min', -32768),
                        digital_max = sig.getint('digital_max', 32767),
                        prefiltering = sig.get('prefiltering', ''),
                        sampling_freq = self.sampling_freq))

    def save(self, config_f=None):
        main_dict = OrderedDict([
                ('baud', self.baud),
                ('sampling_freq', self.sampling_freq),
                ('data_path', self.data_path),
                ('saving_period_s', self.saving_period_s),
                ])

        subject_dict = OrderedDict([
                ('code', self.subject_id.code),
                ('sex', self.subject_id.sex),
                ('dob', self.subject_id.dob),
                ('name', self.subject_id.name),
                ])

        recording_dict = OrderedDict([
                ('experiment_id', self.recording_id.experiment_id),
                ('investigator_id', self.recording_id.investigator_id),
                ('equipment_code', self.recording_id.equipment_code),
                ])

        config_dict = OrderedDict([
                ('Main', main_dict),
                ('Subject', subject_dict),
                ('Recording', recording_dict)
                ])

        for n, signal in enumerate(self.signals):
            section = 'Signal {}'.format(n+1)
            section_contents = OrderedDict([
                    ('label', signal.label),
                    ('transducer_type', signal.transducer_type),
                    ('physical_dim', signal.physical_dim),
                    ('physical_min', signal.physical_min),
                    ('physical_max', signal.physical_max),
                    ('digital_min', signal.digital_min),
                    ('digital_max', signal.digital_max),
                    ('prefiltering', signal.prefiltering),
                    ])
            config_dict[section] = section_contents

        config = configparser.ConfigParser()
        config.read_dict(config_dict)
        if config_f is None:
            config_f = self._config_f
        with open(config_f, 'w') as f:
            config.write(f)

'''
Using daq from command line--

A config.ini file must be specified. This may only contain info about
signals, in which case empty subject and recording_id fields will be
created. E.g.

    pydaq -c config.ini

Using daq in GUI mode--

When launched,
1. Read default parameters ('defaults.ini')
2. If there is a pydaq.ini, read this and overwrite default params.
   Loading first defaults is good to ensure that all parameters are
   defined. If the user were to modify somehow pydaq.ini (e.g. delete
   some fields) and there were no defaults loading configuration would
   fail.
3. If user loads manually a config.ini, overwrite fields. This file may
   only define a few fields, so those not defined explicitly will be
   taken from defaults.ini.
4. When closing, save pydaq.ini


DataAcquisition(baud, sampling_freq, working_dir, signals=[],
    saving_period_s)
'''
