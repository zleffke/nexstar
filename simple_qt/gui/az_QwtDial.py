#!/usr/bin/env python3

from PyQt5 import QtCore
from PyQt5 import Qt


import numpy as np
import sys

class overlayLabel(Qt.QLabel):
    def __init__(self, parent=None, text = "", pixelSize=20, r=255,g=255,b=255, underline=True, bold=True):
        super(overlayLabel, self).__init__(parent)
        self.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
        palette = Qt.QPalette(self.palette())
        palette.setColor(palette.Background,QtCore.Qt.transparent)
        palette.setColor(palette.Foreground,Qt.QColor(r,g,b))
        self.setPalette(palette)
        font = Qt.QFont()
        font.setBold(bold)
        font.setPixelSize(pixelSize)
        font.setUnderline(underline)
        self.setFont(font)
        self.setText(text)

class az_QwtDial(Qt.QDial):
    def __init__(self, parent=None):
        super(az_QwtDial, self).__init__(parent)
        self.parent = parent
        #self.needle = Qwt.QwtDialSimpleNeedle(Qwt.QwtDialSimpleNeedle.Ray, 1, Qt.QColor(255,0,0))
        #self.needle = Qwt.QwtDialSimpleNeedle(Qwt.QwtDialSimpleNeedle.Arrow, 1, Qt.QColor(255,0,0))
        #self.setOrigin(270)
        self.initUI()

    def initUI(self):
        #self.setFrameShadow(Qwt.QwtDial.Plain)
        #self.needle.setWidth(15)
        #self.setNeedle(self.needle)
        self.setValue(0)
        #self.setScaleTicks(5,10,15,1)
        self.setStyleSheet("Qlabel {font-size:14px;}")

        palette = Qt.QPalette()
        palette.setColor(palette.Base,QtCore.Qt.transparent)
        palette.setColor(palette.WindowText,QtCore.Qt.transparent)
        palette.setColor(palette.Text,QtCore.Qt.green)
        self.setPalette(palette)

        self.overlayDial = overlayAzQwtDial(self.parent)

        self.title_label = overlayLabel(self, "Azimuth")

        grid = Qt.QGridLayout()
        grid.setSpacing(0)
        grid.addWidget(self,0,0,1,1)
        grid.addWidget(self.overlayDial,0,0,1,1)
        grid.setRowStretch(0,1)
        self.parent.setLayout(grid)


    def set_cur_az(self, az):
        if    (az < -180)                  : az = -180
        elif ((az >= -180) and (az < 0))   : az = 360 + az
        elif ((az >= 0)    and (az <= 360)): az = az
        elif ((az > 360)   and (az <= 540)): az = az - 360
        elif  (az > 540)                   : az = 180
        self.setValue(az)

    def set_tar_az(self, az):
        if    (az < -180)                  : az = -180
        elif ((az >= -180) and (az < 0))   : az = 360 + az
        elif ((az >= 0)    and (az <= 360)): az = az
        elif ((az > 360)   and (az <= 540)): az = az - 360
        elif  (az > 540)                   : az = 180
        self.overlayDial.setValue(az)

class overlayAzQwtDial(Qt.QDial):
    def __init__(self, parent = None):
        super(overlayAzQwtDial, self).__init__(parent)
        #self.needle = Qwt.QwtDialSimpleNeedle(Qwt.QwtDialSimpleNeedle.Ray, 1, Qt.QColor(0,0,255))
        #self.needle = Qwt.QwtDialSimpleNeedle(Qwt.QwtDialSimpleNeedle.Arrow, 1, Qt.QColor(0,0,255))
        #self.setOrigin(270)
        self.initUI()

    def initUI(self):
        #self.setFrameShadow(Qwt.QwtDial.Plain)
        #self.needle.setWidth(2)
        #self.setNeedle(self.needle)
        self.setValue(0)
        #self.setScaleTicks(5,10,15,1)
        self.setStyleSheet("Qlabel {font-size:14px;}")

        palette = Qt.QPalette()
        palette.setColor(palette.Base,QtCore.Qt.transparent)
        palette.setColor(palette.WindowText,QtCore.Qt.transparent)
        palette.setColor(palette.Text,QtCore.Qt.transparent)
        self.setPalette(palette)

    def set_az(self, az):
        self.setValue(az)
