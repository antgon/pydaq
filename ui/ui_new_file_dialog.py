# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'new_file_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_NewFileDialog(object):
    def setupUi(self, NewFileDialog):
        NewFileDialog.setObjectName("NewFileDialog")
        NewFileDialog.resize(268, 556)
        self.gridLayout = QtWidgets.QGridLayout(NewFileDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.subjectGroupBox = QtWidgets.QGroupBox(NewFileDialog)
        self.subjectGroupBox.setObjectName("subjectGroupBox")
        self.formLayout = QtWidgets.QFormLayout(self.subjectGroupBox)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(self.subjectGroupBox)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.codeLineEdit = QtWidgets.QLineEdit(self.subjectGroupBox)
        self.codeLineEdit.setObjectName("codeLineEdit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.codeLineEdit)
        self.label_3 = QtWidgets.QLabel(self.subjectGroupBox)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.sexFrame = QtWidgets.QFrame(self.subjectGroupBox)
        self.sexFrame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.sexFrame.setObjectName("sexFrame")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.sexFrame)
        self.horizontalLayout.setContentsMargins(-1, 0, -1, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.sexMradioButton = QtWidgets.QRadioButton(self.sexFrame)
        self.sexMradioButton.setChecked(False)
        self.sexMradioButton.setObjectName("sexMradioButton")
        self.horizontalLayout.addWidget(self.sexMradioButton)
        self.sexFradioButton = QtWidgets.QRadioButton(self.sexFrame)
        self.sexFradioButton.setObjectName("sexFradioButton")
        self.horizontalLayout.addWidget(self.sexFradioButton)
        self.sexXradioButton = QtWidgets.QRadioButton(self.sexFrame)
        self.sexXradioButton.setChecked(True)
        self.sexXradioButton.setObjectName("sexXradioButton")
        self.horizontalLayout.addWidget(self.sexXradioButton)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.horizontalLayout.setStretch(3, 10)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.sexFrame)
        self.label_4 = QtWidgets.QLabel(self.subjectGroupBox)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.label_5 = QtWidgets.QLabel(self.subjectGroupBox)
        self.label_5.setObjectName("label_5")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.nameLineEdit = QtWidgets.QLineEdit(self.subjectGroupBox)
        self.nameLineEdit.setObjectName("nameLineEdit")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.nameLineEdit)
        self.dobDateEdit = QtWidgets.QDateEdit(self.subjectGroupBox)
        self.dobDateEdit.setObjectName("dobDateEdit")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.dobDateEdit)
        self.gridLayout.addWidget(self.subjectGroupBox, 0, 0, 1, 1)
        self.recordingGroupBox = QtWidgets.QGroupBox(NewFileDialog)
        self.recordingGroupBox.setObjectName("recordingGroupBox")
        self.formLayout_2 = QtWidgets.QFormLayout(self.recordingGroupBox)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_2 = QtWidgets.QLabel(self.recordingGroupBox)
        self.label_2.setObjectName("label_2")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.startdateDateEdit = QtWidgets.QDateEdit(self.recordingGroupBox)
        self.startdateDateEdit.setObjectName("startdateDateEdit")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.startdateDateEdit)
        self.label_6 = QtWidgets.QLabel(self.recordingGroupBox)
        self.label_6.setObjectName("label_6")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.experimentIdLineEdit = QtWidgets.QLineEdit(self.recordingGroupBox)
        self.experimentIdLineEdit.setObjectName("experimentIdLineEdit")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.experimentIdLineEdit)
        self.label_7 = QtWidgets.QLabel(self.recordingGroupBox)
        self.label_7.setObjectName("label_7")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_7)
        self.investigatorIdLineEdit = QtWidgets.QLineEdit(self.recordingGroupBox)
        self.investigatorIdLineEdit.setObjectName("investigatorIdLineEdit")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.investigatorIdLineEdit)
        self.label_8 = QtWidgets.QLabel(self.recordingGroupBox)
        self.label_8.setObjectName("label_8")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_8)
        self.equipmentCodeLineEdit = QtWidgets.QLineEdit(self.recordingGroupBox)
        self.equipmentCodeLineEdit.setObjectName("equipmentCodeLineEdit")
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.equipmentCodeLineEdit)
        self.gridLayout.addWidget(self.recordingGroupBox, 1, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_9 = QtWidgets.QLabel(NewFileDialog)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_2.addWidget(self.label_9)
        self.flushSecondsSpinBox = QtWidgets.QSpinBox(NewFileDialog)
        self.flushSecondsSpinBox.setMinimum(1)
        self.flushSecondsSpinBox.setMaximum(600)
        self.flushSecondsSpinBox.setProperty("value", 5)
        self.flushSecondsSpinBox.setObjectName("flushSecondsSpinBox")
        self.horizontalLayout_2.addWidget(self.flushSecondsSpinBox)
        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 0, 1, 1)
        self.filenameGroupBox = QtWidgets.QGroupBox(NewFileDialog)
        self.filenameGroupBox.setObjectName("filenameGroupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.filenameGroupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.filedirLabel = QtWidgets.QLabel(self.filenameGroupBox)
        self.filedirLabel.setObjectName("filedirLabel")
        self.verticalLayout.addWidget(self.filedirLabel)
        self.filenameLineEdit = QtWidgets.QLineEdit(self.filenameGroupBox)
        self.filenameLineEdit.setReadOnly(True)
        self.filenameLineEdit.setObjectName("filenameLineEdit")
        self.verticalLayout.addWidget(self.filenameLineEdit)
        self.gridLayout.addWidget(self.filenameGroupBox, 3, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(NewFileDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 4, 0, 1, 1)

        self.retranslateUi(NewFileDialog)
        self.buttonBox.accepted.connect(NewFileDialog.accept)
        self.buttonBox.rejected.connect(NewFileDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(NewFileDialog)

    def retranslateUi(self, NewFileDialog):
        _translate = QtCore.QCoreApplication.translate
        NewFileDialog.setWindowTitle(_translate("NewFileDialog", "New file"))
        self.subjectGroupBox.setTitle(_translate("NewFileDialog", "Subject"))
        self.label.setText(_translate("NewFileDialog", "Code"))
        self.codeLineEdit.setToolTip(_translate("NewFileDialog", "Subject ID"))
        self.codeLineEdit.setText(_translate("NewFileDialog", "X"))
        self.label_3.setText(_translate("NewFileDialog", "Sex"))
        self.sexMradioButton.setToolTip(_translate("NewFileDialog", "Male"))
        self.sexMradioButton.setText(_translate("NewFileDialog", "M"))
        self.sexFradioButton.setToolTip(_translate("NewFileDialog", "Female"))
        self.sexFradioButton.setText(_translate("NewFileDialog", "F"))
        self.sexXradioButton.setToolTip(_translate("NewFileDialog", "Unknown"))
        self.sexXradioButton.setText(_translate("NewFileDialog", "X"))
        self.label_4.setText(_translate("NewFileDialog", "DoB"))
        self.label_5.setText(_translate("NewFileDialog", "Name"))
        self.nameLineEdit.setToolTip(_translate("NewFileDialog", "Subject name"))
        self.nameLineEdit.setText(_translate("NewFileDialog", "X"))
        self.dobDateEdit.setToolTip(_translate("NewFileDialog", "Date of birth"))
        self.dobDateEdit.setDisplayFormat(_translate("NewFileDialog", "yyyy-MM-dd"))
        self.recordingGroupBox.setTitle(_translate("NewFileDialog", "Recording"))
        self.label_2.setText(_translate("NewFileDialog", "Start date"))
        self.startdateDateEdit.setDisplayFormat(_translate("NewFileDialog", "yyyy-MM-dd"))
        self.label_6.setText(_translate("NewFileDialog", "Experiment ID"))
        self.experimentIdLineEdit.setToolTip(_translate("NewFileDialog", "Code of the experiment/investigation"))
        self.experimentIdLineEdit.setText(_translate("NewFileDialog", "X"))
        self.label_7.setText(_translate("NewFileDialog", "Investigator ID"))
        self.investigatorIdLineEdit.setToolTip(_translate("NewFileDialog", "Code of responsible investigator"))
        self.investigatorIdLineEdit.setText(_translate("NewFileDialog", "X"))
        self.label_8.setText(_translate("NewFileDialog", "Equipment code"))
        self.equipmentCodeLineEdit.setToolTip(_translate("NewFileDialog", "Code of equipment used"))
        self.equipmentCodeLineEdit.setText(_translate("NewFileDialog", "X"))
        self.label_9.setText(_translate("NewFileDialog", "Flush to disk every"))
        self.flushSecondsSpinBox.setToolTip(_translate("NewFileDialog", "How often are data saved to disk?"))
        self.flushSecondsSpinBox.setSuffix(_translate("NewFileDialog", " seconds"))
        self.filenameGroupBox.setTitle(_translate("NewFileDialog", "File name"))
        self.filedirLabel.setToolTip(_translate("NewFileDialog", "Working directory (change in Configuration)"))
        self.filedirLabel.setText(_translate("NewFileDialog", "<working dir>"))
        self.filenameLineEdit.setToolTip(_translate("NewFileDialog", "File name (read only)"))

