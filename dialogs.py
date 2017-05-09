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
from datetime import datetime
from PyQt5 import (QtCore, QtGui, QtWidgets)

from edfrw import Signal
from ui.ui_configuration_dialog import Ui_ConfigurationDialog
from ui.ui_signal_dialog import Ui_SignalDialog
from configuration import BAUD_RATES

CONFIG_NROWS = 4
(BAUD, SAMPLING_FREQ, DATA_PATH, SAVING_PERIOD) = range(CONFIG_NROWS)

SIGNAL_NCOLS = 8
(LABEL, TRANSDUCER_TYPE, PHYSICAL_DIM, PHYSICAL_MIN, PHYSICAL_MAX,
 DIGITAL_MIN, DIGITAL_MAX, PREFILTERING) = range(SIGNAL_NCOLS)

SUBJECT_NROWS = 4
(CODE, SEX, DOB, NAME) = range(SUBJECT_NROWS)

RECORDING_NROWS = 3
(EXPERIMENT_ID, INVESTIGATOR_ID, EQUIPMENT) = range(RECORDING_NROWS)

class SignalDialog(QtWidgets.QDialog, Ui_SignalDialog):

    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)


class ConfigurationDialog(QtWidgets.QDialog, Ui_ConfigurationDialog):

    def __init__(self, config, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)

        baud_rates = [str(baud) for baud in BAUD_RATES]
        baud_model = QtCore.QStringListModel(baud_rates, self)
        self.baudComboBox.setModel(baud_model)
        sex_model = QtCore.QStringListModel(['F', 'M', 'X'], self)
        self.sexComboBox.setModel(sex_model)

        self.config = config

        config_model = ConfigurationModel(self.config)
        mapper = QtWidgets.QDataWidgetMapper(self)
        mapper.setOrientation(QtCore.Qt.Vertical)
        mapper.setModel(config_model)
        mapper.addMapping(self.baudComboBox, BAUD)
        mapper.addMapping(self.samplFreqSpinBox, SAMPLING_FREQ)
        mapper.addMapping(self.pathLineEdit, DATA_PATH)
        mapper.addMapping(self.flushSecondsSpinBox, SAVING_PERIOD)
        mapper.toFirst()

        self.signals_model = SignalModel(self.config.signals)
        self.tableView.setModel(self.signals_model)

        subject_model = SubjectIdModel(self.config.subject_id)
        mapper = QtWidgets.QDataWidgetMapper(self)
        mapper.setOrientation(QtCore.Qt.Vertical)
        mapper.setModel(subject_model)
        mapper.addMapping(self.codeLineEdit, CODE)
        mapper.addMapping(self.sexComboBox, SEX)
        mapper.addMapping(self.dobDateEdit, DOB)
        mapper.addMapping(self.nameLineEdit, NAME)
        mapper.toFirst()

        recording_model = RecordingIdModel(self.config.recording_id)
        mapper = QtWidgets.QDataWidgetMapper(self)
        mapper.setOrientation(QtCore.Qt.Vertical)
        mapper.setModel(recording_model)
        mapper.addMapping(self.experimentIdLineEdit, EXPERIMENT_ID)
        mapper.addMapping(self.investigatorIdLineEdit, INVESTIGATOR_ID)
        mapper.addMapping(self.equipmentCodeLineEdit, EQUIPMENT)
        mapper.toFirst()

    def on_tableView_doubleClicked(self):
        row = self.tableView.currentIndex().row()

        dialog = SignalDialog(self)
        mapper = QtWidgets.QDataWidgetMapper(dialog)
        mapper.setSubmitPolicy(
                QtWidgets.QDataWidgetMapper.ManualSubmit)
        mapper.setModel(self.signals_model)
        mapper.addMapping(dialog.labelLineEdit, LABEL)
        mapper.addMapping(dialog.transducerLineEdit, TRANSDUCER_TYPE)
        mapper.addMapping(dialog.physicalDimLineEdit, PHYSICAL_DIM)
        mapper.addMapping(dialog.physicalMinLineEdit, PHYSICAL_MIN)
        mapper.addMapping(dialog.physicalMaxLineEdit, PHYSICAL_MAX)
        mapper.addMapping(dialog.digitalMinLineEdit, DIGITAL_MIN)
        mapper.addMapping(dialog.digitalMaxLineEdit, DIGITAL_MAX)
        mapper.addMapping(dialog.prefilteringTextEdit, PREFILTERING)

        mapper.setCurrentIndex(row)

        ok_clicked = dialog.exec_()
        if ok_clicked:
            mapper.submit()

    def on_pathToolButton_clicked(self, checked=None):
        if checked is None:
            return

        path = QtWidgets.QFileDialog.getExistingDirectory(
                self, caption='Select default data directory')
        if path:
            self.config.data_path = path
            self.pathLineEdit.setText(path)

    def on_samplFreqSpinBox_valueChanged(self):
        self.update_sampl_interval()

    def update_sampl_interval(self):
        val = self.samplFreqSpinBox.value()
        interval = 1.0 / val * 1000.0  # Hz to milliseconds
        txt = '{:.3f}'.format(interval)
        self.samplIntervalLabel.setText(txt)

    def on_addSignalPushButton_clicked(self, checked=None):
        if checked is None:
            return
        row = self.signals_model.rowCount()
        self.signals_model.insertRows(row)

    def on_removeSignalPushButton_clicked(self, checked=None):
        if checked is None:
            return
        row = self.tableView.currentIndex().row()
        self.signals_model.removeRows(row)


class ConfigurationModel(QtCore.QAbstractListModel):

    def __init__(self, config, parent=None):
        super(ConfigurationModel, self).__init__(parent)
        self.config = config

    def rowCount(self, index=QtCore.QModelIndex()):
        return CONFIG_NROWS

    def data(self, index, role=QtCore.Qt.DisplayRole):
        row = index.row()

        if role in (QtCore.Qt.DisplayRole, QtCore.Qt.EditRole):
            if row == BAUD:
                return QtCore.QVariant(self.config.baud)
            elif row == SAMPLING_FREQ:
                return QtCore.QVariant(self.config.sampling_freq)
            elif row == DATA_PATH:
                return QtCore.QVariant(self.config.data_path)
            elif row == SAVING_PERIOD:
                return QtCore.QVariant(self.config.saving_period_s)
        else:
            return QtCore.QVariant()

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if index.isValid():
            row = index.row()
            if row == BAUD:
                self.config.baud = int(value)
            elif row == SAMPLING_FREQ:
                self.config.sampling_freq = value
            elif row == DATA_PATH:
                self.config.data_path = value
            elif row == SAVING_PERIOD:
                self.config.saving_period_s = value
            self.dataChanged.emit(index, index, [])
            return True
        else:
            return False

    def flags(self, index):
        if not index.isValid():
            return QtCore.Qt.ItemIsEnabled
        else:
            return QtCore.Qt.ItemFlags(
                    QtCore.QAbstractListModel.flags(self, index) |
                    QtCore.Qt.ItemIsEditable)


class SignalModel(QtCore.QAbstractTableModel):

    headers = ('Label',
               'Transducer type',
               'Physical dim',
               'Physical min',
               'Physical max',
               'Digital min',
               'Digital max',
               'Prefiltering')

    def __init__(self, signals):
        super(QtCore.QAbstractTableModel, self).__init__()
        self.signals = signals

    def rowCount(self, index=QtCore.QModelIndex()):
        return len(self.signals)

    def columnCount(self, index=QtCore.QModelIndex()):
        return SIGNAL_NCOLS

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if not index.isValid():
            return QtCore.QVariant()

        row = index.row()
        column = index.column()
        signal = self.signals[row]

        if role in (QtCore.Qt.DisplayRole, QtCore.Qt.EditRole):
            if column == LABEL:
                return QtCore.QVariant(signal.label)
            elif column == TRANSDUCER_TYPE:
                return QtCore.QVariant(signal.transducer_type)
            elif column == PHYSICAL_DIM:
                return QtCore.QVariant(signal.physical_dim)
            elif column == PHYSICAL_MIN:
                return QtCore.QVariant(signal.physical_min)
            elif column == PHYSICAL_MAX:
                return QtCore.QVariant(signal.physical_max)
            elif column == DIGITAL_MIN:
                return QtCore.QVariant(signal.digital_min)
            elif column == DIGITAL_MAX:
                return QtCore.QVariant(signal.digital_max)
            elif column == PREFILTERING:
                return QtCore.QVariant(signal.prefiltering)

        elif role == QtCore.Qt.TextAlignmentRole:
            return QtCore.QVariant(
                    int(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter))

        return QtCore.QVariant()

    def headerData(self, section, orientation,
                   role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.TextAlignmentRole:
            if orientation == QtCore.Qt.Horizontal:
                return QtCore.QVariant(int(QtCore.Qt.AlignLeft |
                                           QtCore.Qt.AlignVCenter))
            return QtCore.QVariant(int(QtCore.Qt.AlignRight |
                                       QtCore.Qt.AlignVCenter))
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()
        if orientation == QtCore.Qt.Horizontal:
            header = self.headers[section]
            return QtCore.QVariant(header)
        return QtCore.QVariant(int(section + 1))

    def flags(self, index):
        if not index.isValid():
            return QtCore.Qt.ItemIsEnabled
        return QtCore.Qt.ItemFlags(
                QtCore.QAbstractTableModel.flags(self, index) |
                QtCore.Qt.ItemIsEditable)

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if index.isValid():
            row = index.row()
            column = index.column()
            signal = self.signals[row]

            if column == LABEL:
                # Signal labels must be unique. To enforce this a list
                # is created with current labels and the new entry is
                # checked against this list before accepting it.
                labels = [signal.label for signal in self.signals]
                labels.pop(row)
                if value in labels:
                    QtGui.QMessageBox.warning(
                            None, "Invalid label",
                            "Signal labels must be unique.")
                    return False
                else:
                    signal.label = value
            elif column == TRANSDUCER_TYPE:
                signal.transducer_type = value
            elif column == PHYSICAL_DIM:
                signal.physical_dim = value
            elif column == PHYSICAL_MIN:
                signal.physical_min = value
            elif column == PHYSICAL_MAX:
                signal.physical_max = value
            elif column == DIGITAL_MIN:
                signal.digital_min = value
            elif column == DIGITAL_MAX:
                signal.digital_max = value
            elif column == PREFILTERING:
                signal.prefiltering = value
            return True

        else:
            return False

    def insertRows(self, position, rows=1, index=QtCore.QModelIndex()):
        self.beginInsertRows(QtCore.QModelIndex(), position,
                             position + rows - 1)
        n = len(self.signals) + 1
        new_signal = Signal(label='Signal {}'.format(n))
        new_signal.sampling_freq = self.data
        self.signals.append(new_signal)
        self.endInsertRows()
        return True

    def removeRows(self, position, rows=1, index=QtCore.QModelIndex()):
        self.beginRemoveRows(QtCore.QModelIndex(), position,
                             position + rows - 1)
        self.signals.pop(position)
        self.endRemoveRows()
        return True


class SubjectIdModel(QtCore.QAbstractListModel):

    def __init__(self, subject_id, parent=None):
        super(SubjectIdModel, self).__init__(parent)
        self.subject_id = subject_id

    def rowCount(self, index=QtCore.QModelIndex()):
        return SUBJECT_NROWS

    def data(self, index, role=QtCore.Qt.DisplayRole):
        row = index.row()

        if role in (QtCore.Qt.DisplayRole, QtCore.Qt.EditRole):
            if row == CODE:
                return QtCore.QVariant(self.subject_id.code)
            elif row == SEX:
                return QtCore.QVariant(self.subject_id.sex)
            elif row == DOB:
                return QtCore.QVariant(self.subject_id.dob)
            elif row == NAME:
                return QtCore.QVariant(self.subject_id.name)
        else:
            return QtCore.QVariant()

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if index.isValid():
            row = index.row()
            if row == CODE:
                self.subject_id.code = value
            elif row == SEX:
                self.subject_id.sex = value
            elif row == DOB:
                self.subject_id.dob = value.toPyDate()
            elif row == NAME:
                self.subject_id.name = value
            self.dataChanged.emit(index, index, [])
            return True
        else:
            return False

    def flags(self, index):
        if not index.isValid():
            return QtCore.Qt.ItemIsEnabled
        else:
            return QtCore.Qt.ItemFlags(
                    QtCore.QAbstractListModel.flags(self, index) |
                    QtCore.Qt.ItemIsEditable)


class RecordingIdModel(QtCore.QAbstractListModel):

    def __init__(self, recording_id, parent=None):
        super(RecordingIdModel, self).__init__(parent)
        self.recording_id = recording_id

    def rowCount(self, index=QtCore.QModelIndex()):
        return RECORDING_NROWS

    def data(self, index, role=QtCore.Qt.DisplayRole):
        row = index.row()

        if role in (QtCore.Qt.DisplayRole, QtCore.Qt.EditRole):
            if row == EXPERIMENT_ID:
                return QtCore.QVariant(self.recording_id.experiment_id)
            elif row == INVESTIGATOR_ID:
                return QtCore.QVariant(self.recording_id.investigator_id)
            elif row == EQUIPMENT:
                return QtCore.QVariant(self.recording_id.equipment_code)
        else:
            return QtCore.QVariant()

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        if index.isValid():
            row = index.row()
            if row == EXPERIMENT_ID:
                self.recording_id.experiment_id = value
            elif row == INVESTIGATOR_ID:
                self.recording_id.investigator_id = value
            elif row == EQUIPMENT:
                self.recording_id.equipment_code = value
            self.dataChanged.emit(index, index, [])
            return True
        else:
            return False

    def flags(self, index):
        if not index.isValid():
            return QtCore.Qt.ItemIsEnabled
        else:
            return QtCore.Qt.ItemFlags(
                    QtCore.QAbstractListModel.flags(self, index) |
                    QtCore.Qt.ItemIsEditable)


if __name__ == "__main__":
    import sys
    from configuration import Configuration
    config = Configuration()
    app = QtWidgets.QApplication([])
    self = ConfigurationDialog(config)
    self.show()
