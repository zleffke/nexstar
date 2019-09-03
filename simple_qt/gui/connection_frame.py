#!/usr/bin/env python3
#-- coding: utf-8 --

from PyQt5 import QtCore
from PyQt5 import Qt

from PyQt5.QtCore import pyqtSignal

class connection_frame(Qt.QFrame):
    def __init__(self, parent=None):
        super(connection_frame, self).__init__()
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.setFrameShape(Qt.QFrame.StyledPanel)
        self.init_widgets()
        self.connect_signals()

    def init_widgets(self):
        lbl_width = 45
        val_width = 125
        lbl_height = 12

        #Device
        devLabel = Qt.QLabel("Device:")
        devLabel.setAlignment(Qt.Qt.AlignRight|Qt.Qt.AlignVCenter)
        devLabel.setStyleSheet("QLabel {font:10pt; color:rgb(255,0,0);}")
        devLabel.setFixedWidth(lbl_width)
        self.devTextBox = Qt.QLineEdit()
        self.devTextBox.setText("/dev/ttyUSB0")
        self.devTextBox.setEchoMode(Qt.QLineEdit.Normal)
        self.devTextBox.setStyleSheet("QLineEdit {font:10pt; background-color:rgb(200,75,75); color:rgb(0,0,0);}")
        self.devTextBox.setFixedWidth(val_width)
        self.devTextBox.setFixedHeight(20)
        dev_hbox = Qt.QHBoxLayout()
        dev_hbox.addWidget(devLabel)
        dev_hbox.addWidget(self.devTextBox)

        #Connection Button & Connection Status
        self.connect_button = Qt.QPushButton("Connect")
        self.connect_button.setStyleSheet("QPushButton {font:10pt; background-color:rgb(200,0,0);}")
        self.connect_button.setFixedHeight(20)
        self.connect_button.setFixedWidth(100)

        btn_hbox = Qt.QHBoxLayout()
        btn_hbox.addStretch(1)
        btn_hbox.addWidget(self.connect_button)
        btn_hbox.addStretch(1)

        status_lbl = Qt.QLabel('Status:')
        status_lbl.setAlignment(Qt.Qt.AlignRight|Qt.Qt.AlignVCenter)
        status_lbl.setStyleSheet("QLabel {font:10pt; color:rgb(255,0,0);}")
        status_lbl.setFixedHeight(lbl_height)
        status_lbl.setFixedWidth(lbl_width)
        self.conn_status_lbl = Qt.QLabel('Disconnected')
        self.conn_status_lbl.setAlignment(Qt.Qt.AlignLeft|Qt.Qt.AlignVCenter)
        self.conn_status_lbl.setStyleSheet("QLabel {font:10pt; font-weight:bold; color:rgb(255,0,0);}")
        self.conn_status_lbl.setFixedWidth(val_width)
        self.conn_status_lbl.setFixedHeight(lbl_height)

        status_hbox = Qt.QHBoxLayout()
        status_hbox.addWidget(status_lbl)
        status_hbox.addWidget(self.conn_status_lbl)

        vbox = Qt.QVBoxLayout()
        vbox.addLayout(dev_hbox)
        vbox.addLayout(status_hbox)
        vbox.addLayout(btn_hbox)
        vbox.addStretch(1)
        self.setLayout(vbox)


    def connect_signals(self):
        pass

    def connect_button_event(self):
        if self.connected == False:
            #print self.utc_ts() + "Connecting to Daemon..."
            self.connected = self.callback.connect(self.ip, self.port,self)
        elif self.connected == True:
            #print self.utc_ts() + "Disconnecting from Daemon..."
            self.connected = self.callback.disconnect()
            #self.set_daemon_state('IDLE')
        self.update_connection_state()

    def update_connection_state(self):
        if self.connected == True:
            self.connect_button.setText('Disconnect')
            self.conn_status_lbl.setText('CONNECTED')
            self.conn_status_lbl.setStyleSheet("QLabel {font-weight:bold; color:rgb(0,255,0);}")
            #self.update_timer.start()
        elif self.connected == False:
            self.connect_button.setText('Connect')
            self.conn_status_lbl.setText('DISCONNECTED')
            self.conn_status_lbl.setStyleSheet("QLabel {font-weight:bold; color:rgb(255,0,0);}")
            #self.update_timer.stop()
