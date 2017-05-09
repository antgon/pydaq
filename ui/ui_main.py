# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(780, 538)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.configurationGroupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.configurationGroupBox.setObjectName("configurationGroupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.configurationGroupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.configureButton = QtWidgets.QPushButton(self.configurationGroupBox)
        self.configureButton.setObjectName("configureButton")
        self.verticalLayout_2.addWidget(self.configureButton)
        self.loadConfigButton = QtWidgets.QPushButton(self.configurationGroupBox)
        self.loadConfigButton.setObjectName("loadConfigButton")
        self.verticalLayout_2.addWidget(self.loadConfigButton)
        self.saveConfigButton = QtWidgets.QPushButton(self.configurationGroupBox)
        self.saveConfigButton.setObjectName("saveConfigButton")
        self.verticalLayout_2.addWidget(self.saveConfigButton)
        self.verticalLayout.addWidget(self.configurationGroupBox)
        self.displayGroupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.displayGroupBox.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.displayGroupBox.setObjectName("displayGroupBox")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.displayGroupBox)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.playButton = QtWidgets.QPushButton(self.displayGroupBox)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/play.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        icon1.addPixmap(QtGui.QPixmap(":/pause.svg"), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.playButton.setIcon(icon1)
        self.playButton.setIconSize(QtCore.QSize(24, 24))
        self.playButton.setCheckable(False)
        self.playButton.setObjectName("playButton")
        self.horizontalLayout_3.addWidget(self.playButton)
        self.stopButton = QtWidgets.QPushButton(self.displayGroupBox)
        self.stopButton.setEnabled(False)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/stop.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.stopButton.setIcon(icon2)
        self.stopButton.setIconSize(QtCore.QSize(24, 24))
        self.stopButton.setCheckable(False)
        self.stopButton.setObjectName("stopButton")
        self.horizontalLayout_3.addWidget(self.stopButton)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.physUnitsCheckBox = QtWidgets.QCheckBox(self.displayGroupBox)
        self.physUnitsCheckBox.setObjectName("physUnitsCheckBox")
        self.verticalLayout_3.addWidget(self.physUnitsCheckBox)
        self.verticalLayout.addWidget(self.displayGroupBox)
        self.captureGroupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.captureGroupBox.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.captureGroupBox.setObjectName("captureGroupBox")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.captureGroupBox)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.recordButton = QtWidgets.QPushButton(self.captureGroupBox)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/rec.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.recordButton.setIcon(icon3)
        self.recordButton.setIconSize(QtCore.QSize(24, 24))
        self.recordButton.setCheckable(False)
        self.recordButton.setObjectName("recordButton")
        self.horizontalLayout.addWidget(self.recordButton)
        self.stopRecordButton = QtWidgets.QPushButton(self.captureGroupBox)
        self.stopRecordButton.setEnabled(False)
        self.stopRecordButton.setIcon(icon2)
        self.stopRecordButton.setIconSize(QtCore.QSize(24, 24))
        self.stopRecordButton.setCheckable(False)
        self.stopRecordButton.setObjectName("stopRecordButton")
        self.horizontalLayout.addWidget(self.stopRecordButton)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.videoCheckBox = QtWidgets.QCheckBox(self.captureGroupBox)
        self.videoCheckBox.setObjectName("videoCheckBox")
        self.verticalLayout_4.addWidget(self.videoCheckBox)
        self.verticalLayout.addWidget(self.captureGroupBox)
        self.markersGroupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.markersGroupBox.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.markersGroupBox.setObjectName("markersGroupBox")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.markersGroupBox)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.addMarkerButton = QtWidgets.QPushButton(self.markersGroupBox)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/add.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.addMarkerButton.setIcon(icon4)
        self.addMarkerButton.setIconSize(QtCore.QSize(24, 24))
        self.addMarkerButton.setObjectName("addMarkerButton")
        self.gridLayout_7.addWidget(self.addMarkerButton, 0, 0, 1, 1)
        self.editMarkerButton = QtWidgets.QPushButton(self.markersGroupBox)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/edit.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.editMarkerButton.setIcon(icon5)
        self.editMarkerButton.setIconSize(QtCore.QSize(24, 24))
        self.editMarkerButton.setObjectName("editMarkerButton")
        self.gridLayout_7.addWidget(self.editMarkerButton, 0, 1, 1, 1)
        self.verticalLayout.addWidget(self.markersGroupBox)
        spacerItem = QtWidgets.QSpacerItem(20, 17, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.quitButton = QtWidgets.QPushButton(self.centralwidget)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/quit.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.quitButton.setIcon(icon6)
        self.quitButton.setIconSize(QtCore.QSize(24, 24))
        self.quitButton.setObjectName("quitButton")
        self.horizontalLayout_2.addWidget(self.quitButton)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_4.addLayout(self.verticalLayout)
        self.graphicsView = GraphicsLayoutWidget(self.centralwidget)
        self.graphicsView.setObjectName("graphicsView")
        self.horizontalLayout_4.addWidget(self.graphicsView)
        self.horizontalLayout_4.setStretch(0, 1)
        self.horizontalLayout_4.setStretch(1, 50)
        self.gridLayout.addLayout(self.horizontalLayout_4, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "PyDAQ"))
        self.configurationGroupBox.setTitle(_translate("MainWindow", "Configuration"))
        self.configureButton.setToolTip(_translate("MainWindow", "Configure [Ctrl+C]"))
        self.configureButton.setText(_translate("MainWindow", "Configure"))
        self.configureButton.setShortcut(_translate("MainWindow", "Ctrl+C"))
        self.loadConfigButton.setText(_translate("MainWindow", "Load"))
        self.saveConfigButton.setText(_translate("MainWindow", "Save"))
        self.displayGroupBox.setTitle(_translate("MainWindow", "Display"))
        self.playButton.setToolTip(_translate("MainWindow", "Start [P]"))
        self.playButton.setShortcut(_translate("MainWindow", "P"))
        self.stopButton.setToolTip(_translate("MainWindow", "Stop [S]"))
        self.stopButton.setShortcut(_translate("MainWindow", "S"))
        self.physUnitsCheckBox.setText(_translate("MainWindow", "Physical units"))
        self.captureGroupBox.setTitle(_translate("MainWindow", "Capture"))
        self.recordButton.setToolTip(_translate("MainWindow", "Capture data to file [C]"))
        self.recordButton.setShortcut(_translate("MainWindow", "C"))
        self.stopRecordButton.setToolTip(_translate("MainWindow", "Stop [S]"))
        self.stopRecordButton.setShortcut(_translate("MainWindow", "S"))
        self.videoCheckBox.setText(_translate("MainWindow", "Video"))
        self.markersGroupBox.setTitle(_translate("MainWindow", "Markers"))
        self.addMarkerButton.setToolTip(_translate("MainWindow", "Add marker [M]"))
        self.addMarkerButton.setShortcut(_translate("MainWindow", "M"))
        self.editMarkerButton.setToolTip(_translate("MainWindow", "Edit marker(s) [E]"))
        self.editMarkerButton.setShortcut(_translate("MainWindow", "E"))
        self.quitButton.setToolTip(_translate("MainWindow", "Quit [Ctrl+Q]"))
        self.quitButton.setShortcut(_translate("MainWindow", "Ctrl+Q"))
        self.actionQuit.setText(_translate("MainWindow", "&Quit"))
        self.actionQuit.setShortcut(_translate("MainWindow", "Ctrl+Q"))

from pyqtgraph import GraphicsLayoutWidget
from . import resources_rc
