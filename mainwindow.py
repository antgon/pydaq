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

from itertools import count
import datetime as dt
import time
from PyQt5 import (QtCore, QtGui, QtWidgets)
import pyqtgraph as pg
import numpy as np
from serial import (SerialException)  # SerialTimeoutException)

from edfrw import (SubjectId, RecordingId, Signal)
from ui.ui_main import Ui_MainWindow
from acquisition import (DataAcquisition)
from dialogs import (ConfigurationDialog, NewFileDialog)

# TODO
# Upon rec stop, wait for one full cycle to complete to ensure that the
# last data acquired are saved.

# Set a limit to sampling freq. What is reasonable and manageable? At
# the moment the ange 1 to 999 are set directly in the UI because
# configuration cmd in its current form can only take 3 digits for
# sampling freq.

# Plot displays physical instead of digital values

# EDF items must be int16 (not uint16)-check that this is consistent.

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    '''
    Data acquisition main window
    '''
    # GUI refresh rate in milliseconds.
    GUI_REFRESH_RATE = 100

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.setupUi(self)

        self.newFileButton.setDisabled(True)
        self.displayGroupBox.setDisabled(True)
        self.captureGroupBox.setDisabled(True)
        self.markersGroupBox.setDisabled(True)

        self.daq = DataAcquisition()

    def on_quitButton_clicked(self, checked=None):
        if checked is None:
            return
        if hasattr(self, 'timer'):
            self.timer.stop()
        self.daq.stop()
        self.close()

    # Configuration-----------------------------------------------------

    def on_configureButton_clicked(self, checked=None):
        if checked is None:
            return

        self.statusbar.clearMessage()

        # If there are no signals create 3 empty signals to start with.
        if len(self.daq.signals) == 0:
            for n in (1, 2, 3):
                s = Signal(label='Signal {}'.format(n))
                self.daq.signals.append(s)

        dialog = ConfigurationDialog(self.daq, parent=self)
        ok_clicked = dialog.exec_()
        if ok_clicked:
            # TODO EDF allows to acquire each signal at different sample
            # rates, but for the time being this software aquires all
            # signals at the same rate. This lines are to ensure that
            # the signals sampling frequency match.
            for signal in self.daq.signals:
                signal.sampling_freq = self.daq.sampling_freq
            # TODO check that there are enough signals and config is
            # valid
            # set sampling freq to each signal
            self.newFileButton.setEnabled(True)
            self.displayGroupBox.setEnabled(True)
            # At low sampling frequencies the GUI refresh rate must
            # be slowed down to avoid errors. GUI refresh rate is in
            # milliseconds.
            if self.daq.sampling_freq < 1000/self.GUI_REFRESH_RATE:
                self.GUI_REFRESH_RATE = 1000/self.daq.sampling_freq
            else:
                # Reset to the default
                self.GUI_REFRESH_RATE = 100

    # New file ---------------------------------------------------------

    # TODO if a file was previously created, a new file dialog should
    # load previous values to save time typing

    # TODO set up this dialog in a model/view manner instead, as with
    # configuration

    def on_newFileButton_clicked(self, checked=None):
        if checked is None:
            return
        dialog = NewFileDialog(self.daq, parent=self)
        ok_clicked = dialog.exec_()
        if ok_clicked:
            # Subject variables
            code = dialog.codeLineEdit.text()
            if dialog.sexMradioButton.isChecked():
                sex = 'M'
            elif dialog.sexFradioButton.isChecked():
                sex = 'F'
            else:
                sex = 'X'
            dob = dialog.dobDateEdit.date().toPyDate()
            dob = dob.isoformat()
            name = dialog.nameLineEdit.text()

            # Recording variables
            startdate = dialog.startdateDateEdit.date().toPyDate()
            startdate = startdate.isoformat()
            experiment_id = dialog.experimentIdLineEdit.text()
            investigator_id = dialog.investigatorIdLineEdit.text()
            equipment_code = dialog.equipmentCodeLineEdit.text()

            # Create EDF entries
            subject_id = SubjectId(code, sex, dob, name)
            recording_id = RecordingId(startdate, experiment_id,
                                       investigator_id,
                                       equipment_code)

            # Flush data period
            self.daq.saving_period_s = dialog.flushSecondsSpinBox.value()

            # Filename
            filename = dialog.filenameLineEdit.text()
            #filename = os.path.join(self.config.working_dir, filename)
            self.daq.open_edf(filename, subject_id, recording_id)

            self.captureGroupBox.setEnabled(True)

    # Display group ----------------------------------------------------

    def connect(self):
        self.statusbar.showMessage('Connecting to µC...')
        try:
            self.daq.start()
        except SerialException as error:
            msg = 'Connection error'
            self.statusbar.showMessage(msg)
            QtWidgets.QMessageBox.critical(self, msg, error.args[0])
            return False
        else:
            self.statusbar.clearMessage()
            start = dt.datetime.fromtimestamp(self.daq.mcu.timestamp)
            start = dt.datetime.strftime(start, '%Y-%m-%d %H:%M:%S')
            self.statusbar.showMessage(
                    'µC port: {} | '.format(self.daq.mcu.port) +
                    'Sampling frequency: {:.2f} Hz | '.format(
                            self.daq.sampling_freq) +
                    'Start: {}'.format(start))
            self.setup_plot()
            return True

    def on_playButton_clicked(self, checked=None):
        if checked is None:
            return

        if self.connect():
            # Reset buttons.
            self.playButton.setDisabled(True)
            self.stopButton.setEnabled(True)
            self.configurationGroupBox.setDisabled(True)
            self.captureGroupBox.setDisabled(True)
            self.display_status('running')

    def on_stopButton_clicked(self, checked=None):
        if checked is None:
            return
        if hasattr(self, 'timer'):
            self.timer.stop()
        self.daq.stop()

        #tend = dt.datetime.fromtimestamp(time.time())
        #tend = dt.datetime.strftime(tend, '%Y-%m-%d %H:%M:%S')
        #print('Stop: {}'.format(tend))

        self.playButton.setEnabled(True)
        self.stopButton.setDisabled(True)
        self.configurationGroupBox.setEnabled(True)
        self.captureGroupBox.setEnabled(True)
        self.display_status('stop')

    def on_physUnitsCheckBox_toggled(self):
        self.update_y_labels()

    # Capture group ----------------------------------------------------

    def on_recordButton_clicked(self, checked=None):
        if checked is None:
            return

        if self.daq.edffile is None:
            msg = ('Create a new file first.')
            QtGui.QMessageBox.information(self, 'No EDF file',
                                          msg, QtGui.QMessageBox.Ok)
            return

        else:
            if self.connect():
                self.stopRecordButton.setEnabled(True)
                self.displayGroupBox.setDisabled(True)
                self.configurationGroupBox.setDisabled(True)
                self.videoCheckBox.setDisabled(True)
                self.daq.start_recording()
                self.display_status('rec')

    def on_stopRecordButton_clicked(self, checked=None):
        if checked is None:
            return
        if hasattr(self, 'timer'):
            self.timer.stop()
        self.daq.stop_recording()
        self.stopRecordButton.setDisabled(True)
        self.displayGroupBox.setEnabled(True)
        self.configurationGroupBox.setEnabled(True)
        self.videoCheckBox.setEnabled(True)
        self.display_status('stop')

    def on_videoCheckBox_toggled(self):
        pass

    def on_loadProfileButton_clicked(self, checked=None):
        if checked is None:
            return

    # TODO Markers -----------------------------------------------------

    # def on_addMarkerButton_clicked(self, checked=None):
    #     if checked is None:
    #         return
    #     position = self.display_buffer.xmax
    #     marker = pg.InfiniteLine(angle=90, movable=False,
    #                              pen=config.marker_colour, pos=position)
    #     for plot in self.plots:
    #         plot.addItem(marker, ignoreBounds=True)
    #     self._items.append(marker)
    #     self.markers.extend(position)
    #
    # def on_editMarkerButton_clicked(self, checked=None):
    #     if checked is None:
    #         return
    #     self.dialog = MarkerDialog(self)
    #     self.dialog.display_markers(self.markers)
    #     self.dialog.show()

    # Plotting functions ----------------------------------------------

    def update_plot(self):
        with self.daq.lock:
            x = np.array(self.daq.x)
            y = np.array(self.daq.y).T
            for (index, curve, samples) in zip(count(), self.curves, y):
                if self.physUnitsCheckBox.isChecked():
                    samples = self.daq.signals[index].dig_to_phys(samples)
                curve.setData(x, samples)

    def setup_plot(self):

        title_fontsize = 10
        x_tick_fontsize = 10
        y_tick_fontsize = 10
        # marker_fontsize = 8
        y_tick_margin = 60
        curve_colour = "#acfa58"

        xfont = pg.QtGui.QFont()
        yfont = pg.QtGui.QFont()
        yfont.setPointSize(y_tick_fontsize)
        xfont.setPointSize(x_tick_fontsize)

        # Format with bounding box...
        # self.layout = pg.GraphicsLayout(border=(100, 100, 100))
        # or no box.
        self.layout = pg.GraphicsLayout()

        # Add a 'status label' at the top right corner.
        self.status_label = self.layout.addLabel(justify='right')

        self.graphicsView.setCentralItem(self.layout)
        self.plots = []
        self.curves = []

        # Create a plot for each signal and initialise a curve for
        # each plot. These curves are the ones that will be updated
        # with serial data.
        for row in range(self.daq.nsignals):
            self.layout.nextRow()
            plot = self.layout.addPlot()

            # Format y-axis.
            # Add a fixed margin to the left so that the plots are
            # aligned regardless of the width of the y-ticklabels.
            yaxis = plot.axes['left']['item']
            yaxis.setWidth(y_tick_margin)
            yaxis.setTickFont(yfont)

            # Format x-axis. Do not show x-ticklabels but do retain
            # the x-axis line and the vertical grid lines.
            xaxis = plot.axes['bottom']['item']
            xaxis.setStyle(showValues=False)
            plot.showGrid(x=True, y=True)

            # Set titles.
            title = "<span style='font-size:{}pt'>{}</span>".format(
                    title_fontsize, self.daq.signals[row].label)
            plot.setTitle(title, justify='left')

            # Create curves.
            curve = plot.plot(pen=curve_colour)
            self.plots.append(plot)
            self.curves.append(curve)

        # Link x-axis from all plots to that of the last one.
        for plot in self.plots[:-1]:
            plot.setXLink(self.plots[-1])

        # Show the x-axis and the x-label in the last plot.
        last_plot = self.plots[-1]
        xaxis = last_plot.axes['bottom']['item']
        xaxis.setStyle(showValues=True)
        xaxis.setTickFont(yfont)
        last_plot.setLabel('bottom', 'Time', units='s', size=10)

        # Add labesl to y axis
        self.update_y_labels()

        # Update plot at regular intervals.
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(self.GUI_REFRESH_RATE)

    def update_y_labels(self):
        ylab_fontsize = 9
        fmt = "<span style='font-size:{}pt'>".format(ylab_fontsize)
        fmt += "{}</span>"
        for indx, plot in enumerate(self.plots):
            if self.physUnitsCheckBox.isChecked():
                text = self.daq.signals[indx].physical_dim
            else:
                text = 'ADC'
            plot.setLabel('left', fmt.format(text), units=None)

    def display_status(self, status):
        if status == 'running':
            colour = "#acfa58"
        elif status == 'stop':
            colour = 'grey'
        elif status == 'pause':
            colour = 'grey'
        elif status == 'rec':
            colour = 'red'
        elif status == 'ready':
            colour = "#a9f5f2"
        else:
            status, colour = '??', 'yellow'
        text = status.upper()
        self.status_label.setText(
                "<span style='font-size: 16 pt; color: {}'>{}</span>".
                format(colour, text))

    def clear_plot(self):
        self.display_buffer.clear()
        self.clear_regions()
        for curve in self.curves:
            curve.clear()
        for item in self._items:
            item.setVisible(False)
        self._items = []


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication([])
    self = MainWindow()
    self.show()
    # sys.exit(app.exec_())
    # QtWidgets.QApplication.instance().exec_()
