#!/usr/bin/env python3
#-- coding: utf-8 --

from PyQt5 import QtCore
from PyQt5 import Qt
from nexstar import *

class goto_frame(Qt.QFrame):
    def __init__(self, parent=None):
        super(goto_frame, self).__init__()
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.setFrameShape(Qt.QFrame.StyledPanel)
        self.init_widgets()
        self.connect_signals()

    def init_widgets(self):
        lbl_width = 50
        val_width = 125
        lbl_height = 12
        btn_height = 20

        frame_lbl = Qt.QLabel("GoTo Controls:")
        frame_lbl.setAlignment(Qt.Qt.AlignLeft|Qt.Qt.AlignVCenter)
        frame_lbl.setStyleSheet("QLabel {font:12pt; font-weight:bold; text-decoration: underline; color:rgb(255,0,0);}")
        frame_lbl.setFixedWidth(200)
        frame_lbl.setFixedHeight(20)

        self.azLabel = Qt.QLabel("Target Azimuth:")
        self.azLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        self.azLabel.setStyleSheet("QLabel {font:10pt; color:rgb(255,0,0);}")
        self.azTextBox = Qt.QLineEdit()
        self.azTextBox.setText("000.000")
        self.azTextBox.setInputMask("#00.000;")
        self.azTextBox.setEchoMode(Qt.QLineEdit.Normal)
        self.azTextBox.setStyleSheet("QLineEdit {font:10pt; background-color:rgb(200,75,75); color:rgb(0,0,0);}")
        self.azTextBox.setMaxLength(3)
        self.azTextBox.setFixedWidth(80)
        self.azTextBox.setFixedHeight(20)
        az_hbox = Qt.QHBoxLayout()
        az_hbox.addWidget(self.azLabel)
        az_hbox.addWidget(self.azTextBox)

        self.elLabel = Qt.QLabel("Target Elevation:")
        self.elLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        self.elLabel.setStyleSheet("QLabel {font:10pt; color:rgb(255,0,0);}")
        self.elTextBox = Qt.QLineEdit()
        self.elTextBox.setText("00.000")
        self.elTextBox.setInputMask("#00.000;")
        self.elTextBox.setEchoMode(Qt.QLineEdit.Normal)
        self.elTextBox.setStyleSheet("QLineEdit {font:10pt; background-color:rgb(200,75,75); color:rgb(0,0,0);}")
        self.elTextBox.setMaxLength(3)
        self.elTextBox.setFixedWidth(80)
        self.elTextBox.setFixedHeight(20)
        el_hbox = Qt.QHBoxLayout()
        el_hbox.addWidget(self.elLabel)
        el_hbox.addWidget(self.elTextBox)

        self.gotoButton = Qt.QPushButton("GoTo")
        self.gotoButton.setFixedHeight(btn_height)
        self.gotoButton.setStyleSheet("QPushButton { font:10pt; background-color:rgb(200,0,0); }")
        self.cancelButton = Qt.QPushButton("Cancel")
        self.cancelButton.setFixedHeight(btn_height)
        self.cancelButton.setStyleSheet("QPushButton { font:10pt; background-color:rgb(200,0,0); }")
        btn_hbox = Qt.QHBoxLayout()
        btn_hbox.addWidget(self.gotoButton)
        btn_hbox.addWidget(self.cancelButton)

        lbl = Qt.QLabel("Tracking Mode:")
        lbl.setAlignment(Qt.Qt.AlignRight|Qt.Qt.AlignVCenter)
        lbl.setStyleSheet("QLabel {font:10pt; color:rgb(255,0,0);}")
        lbl.setFixedWidth(100)
        lbl.setFixedHeight(lbl_height)
        self.tmRb_off = Qt.QRadioButton("OFF")
        self.tmRb_off.setChecked(True)
        self.tmRb_off.mode = 0
        self.tmRb_off.setStyleSheet("QRadioButton { font:10pt; color:rgb(200,0,0); }")
        self.tmRb_altaz = Qt.QRadioButton("ALT AZ")
        self.tmRb_altaz.setChecked(False)
        self.tmRb_altaz.mode = 1
        self.tmRb_altaz.setStyleSheet("QRadioButton { font:10pt; color:rgb(200,0,0); }")
        self.getTmButton = Qt.QPushButton("Get Tracking Mode")
        self.getTmButton.setFixedHeight(btn_height)
        self.getTmButton.setStyleSheet("QPushButton { font:10pt; background-color:rgb(200,0,0); }")
        tm_hbox = Qt.QHBoxLayout()
        tm_hbox.addStretch(1)
        tm_hbox.addWidget(lbl)
        tm_hbox.addWidget(self.tmRb_off)
        tm_hbox.addWidget(self.tmRb_altaz)

        vbox = Qt.QVBoxLayout()
        vbox.addWidget(frame_lbl)
        vbox.addLayout(az_hbox)
        vbox.addLayout(el_hbox)
        vbox.addLayout(btn_hbox)
        vbox.addWidget(self.getTmButton)
        vbox.addLayout(tm_hbox)
        self.setLayout(vbox)


    def connect_signals(self):
        self.cancelButton.clicked.connect(self.cancelButton_event)
        self.gotoButton.clicked.connect(self.gotoButton_event)
        self.tmRb_off.toggled.connect(self.set_track_mode)
        self.tmRb_altaz.toggled.connect(self.set_track_mode)
        self.getTmButton.clicked.connect(self.getTmButton_event)

    def set_track_mode(self):
        rb = self.sender()
        if rb.isChecked():
            self.parent.set_tracking_mode(rb.mode)

    def getTmButton_event(self):
        self.parent.getTrackingMode()

    def cancelButton_event(self):
        self.parent.cancel_goto()

    def gotoButton_event(self):
        self.tar_az = float(self.azTextBox.text())
        self.tar_el = float(self.elTextBox.text())
        self.parent.goto_position(self.tar_az, self.tar_el)


    def increment_target_angle(self, az_el, val):
        #Called by button control frame
        if az_el == 'az':
            self.tar_az += val
            self.update_target_azimuth()
        elif az_el == 'el':
            self.tar_el += val
            self.update_target_elevation()
        #self.callback.set_position(self.tar_az, self.tar_el, True)

    def update_target_azimuth(self):
        if self.tar_az < -180.0: self.tar_az = -180.0
        if self.tar_az >  540.0: self.tar_az = 540.0
        #self.az_compass.set_tar_az(self.tar_az)
        #self.az_lcd_fr.set_tar(self.tar_az)
        #self.azTextBox.setText(str(self.tar_az))

    def update_target_elevation(self):
        if self.tar_el < 0: self.tar_el = 0
        if self.tar_el > 180: self.tar_el = 180
        #self.el_compass.set_tar_el(self.tar_el)
        #self.el_lcd_fr.set_tar(self.tar_el)
        #self.elTextBox.setText(str(self.tar_el))
