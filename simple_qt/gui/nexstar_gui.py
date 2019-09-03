#!/usr/bin/env python3
#version 2.1

from PyQt5 import Qt
from PyQt5 import QtCore
import numpy as np
import sys
import time
import datetime

#from nexstar import *
sys.path.insert(1, '/home/zleffke/github/zleffke/nexstar_module/')

from nexstar import *

from gui.control_button_frame import *
from gui.lcd_feedback_frame import *
from gui.slew_frame import *
from gui.feedback_frame import *
from gui.connection_frame import *
from gui.goto_frame import *
from gui.sync_frame import *
from gui.gpredict_frame import *


class main_widget(Qt.QWidget):
    def __init__(self):
        super(main_widget, self).__init__()
        self.initUI()

    def initUI(self):
        self.grid = Qt.QGridLayout()
        #self.setLayout(self.grid)

class MainWindow(Qt.QMainWindow):
    def __init__(self, cfg):
        #Qt.QMainWindow.__init__(self)
        super(MainWindow, self).__init__()
        self.setWindowTitle('Simple Nexstar Control GUI v0.1.0')
        self.resize(550, 300)
        #self.setMinimumWidth(800)
        #self.setMaximumWidth(900)
        #self.setContentsMargins(0,0,0,0)
        self.main_window = main_widget()
        self.setCentralWidget(self.main_window)

        self.cfg    = cfg

        #self.statusBar().showMessage("| Disconnected | Manual | Current Az: 000.0 | Current El: 000.0 |")

        self.init_variables()
        self.init_ui()
        self.init_nexstar()

        self.darken()
        #self.setFocus()

    def init_nexstar(self):
        try:
            self.ns     = NexstarHandController(self.cfg['nexstar']['dev'])
        except Exception as e:
            print("Problem Opening Serial Port: {:s}".format(self.cfg['nexstar']['dev']))
            print(e)
            sys.exit()

        try:
            [self.cur_az, self.cur_el] = self.ns.getPosition()
            #[self.cur_ra, self.cur_dec] = self.ns.getPosition(NexstarCoordinateMode.RA_DEC)
            self.model = self.ns.getModel()
            self.fb_fr.update_model(self.model)
            self.gtip = self.ns.getGotoInProgress()
        except Exception as e:
            print(e)
            print('trying again...')
            self.model = self.ns.getModel()
            self.fb_fr.update_model(self.model)

        try:
            print("Setting Location: {:f},{:f}".format(self.cfg['geolocation']['latitude'],
                                                       self.cfg['geolocation']['longitude']))
            self.ns.setLocation(self.cfg['geolocation']['latitude'],
                                self.cfg['geolocation']['longitude'])

            [lat, lon] = self.ns.getLocation()
            print(lat, lon)
        except Exception as e:
            print(e)




        # try:
        #     print("Setting Time:")
        #     ts = datetime.datetime.now(datetime.timezone.utc)
        #     self.ns.setTime(ts, 0)
        #     print("Set Time to:", ts)
        #     print("Checking Time:")
        #     ts1 = self.ns.getTime()
        #     print(ts1)
        # except Exception as e:
        #     print(e)
        #     print(sys.exc_info())

    def init_variables(self):
        self.connected = False      #TCP/IP Connection to Daemon
        self.daemon_state = 'IDLE'

        #Nexstar variables
        self.gtip = False
        self.cur_az = 0
        self.cur_el = 0
        self.model = 0
        #self.cur_ra = 0
        #self.cur_dec = 0
        #self.cur_az_rate = 0
        #self.tar_az = 0
        #self.cur_el = 0
        #self.cur_el_rate = 0
        #self.tar_el = 0

        self.home_az = 0
        self.home_el = 0
        self.tar_az = self.home_az
        self.tar_el = self.home_el

        self.callback    = None   #Callback accessor for tracking control
        self.update_rate = self.cfg['update_rate'] * 1000    #Feedback Query Auto Update Interval in milliseconds

    def init_ui(self):
        self.init_frames()
        self.init_timers()
        self.connect_signals()
        self.show()

    def init_timers(self):
        self.update_timer = QtCore.QTimer(self)
        self.update_timer.setInterval(self.update_rate)
        #self.update_timer.start(self.update_rate)

    def connect_signals(self):
        self.update_timer.timeout.connect(self.auto_query_timeout)
        self.update_timer.start()

    def auto_query_timeout(self):
        [self.cur_az, self.cur_el] = self.ns.getPosition()
        #[self.cur_ra, self.cur_dec] = self.ns.getPosition(coordinateMode=NexstarCoordinateMode.RA_DEC)
        self.track_mode = self.ns.getTrackingMode()
        self.gtip = self.ns.getGotoInProgress()

        self.fb_fr.update_az_el(self.cur_az, self.cur_el)
        #self.fb_fr.update_ra_dec(self.cur_ra, self.cur_dec)
        self.fb_fr.update_track_mode(self.track_mode)
        self.fb_fr.update_gtip(self.gtip)

    ##### SLEW OPERATIONS ############
    def slew_up_left(self, az_speed, el_speed):
        print("Slew Up/Left, Az Speed: {:d}, El Speed: {:d}".format(az_speed, el_speed))
        self.ns.slew_fixed(NexstarDeviceId.AZM_RA_MOTOR,-1*az_speed)
        self.ns.slew_fixed(NexstarDeviceId.ALT_DEC_MOTOR,el_speed)

    def slew_up(self, el_speed):
        print("Slew Up, El Speed: {:d}".format(el_speed))
        self.ns.slew_fixed(NexstarDeviceId.ALT_DEC_MOTOR,el_speed)

    def slew_up_right(self, az_speed, el_speed):
        print("Slew Up/Right, Az Speed: {:d}, El Speed: {:d}".format(az_speed, el_speed))
        self.ns.slew_fixed(NexstarDeviceId.AZM_RA_MOTOR,az_speed)
        self.ns.slew_fixed(NexstarDeviceId.ALT_DEC_MOTOR,el_speed)

    def slew_left(self, az_speed):
        print("Slew Left, Az Speed: {:d}".format(az_speed))
        self.ns.slew_fixed(NexstarDeviceId.AZM_RA_MOTOR,-1*az_speed)

    def slew_stop(self):
        print("Slew Stop")
        self.ns.slew_fixed(NexstarDeviceId.AZM_RA_MOTOR,0)
        self.ns.slew_fixed(NexstarDeviceId.ALT_DEC_MOTOR,0)

    def slew_right(self, az_speed):
        print("Slew Right, Az Speed: {:d}".format(az_speed))
        self.ns.slew_fixed(NexstarDeviceId.AZM_RA_MOTOR,az_speed)

    def slew_down_left(self, az_speed, el_speed):
        print("Slew Down/Left, Az Speed: {:d}, El Speed: {:d}".format(az_speed, el_speed))
        self.ns.slew_fixed(NexstarDeviceId.AZM_RA_MOTOR,-1*az_speed)
        self.ns.slew_fixed(NexstarDeviceId.ALT_DEC_MOTOR,-1*el_speed)

    def slew_down(self, el_speed):
        print("Slew Down, El Speed: {:d}".format(el_speed))
        self.ns.slew_fixed(NexstarDeviceId.ALT_DEC_MOTOR,-1*el_speed)

    def slew_down_right(self, az_speed, el_speed):
        print("Slew Down/Right, Az Speed: {:d}, El Speed: {:d}".format(az_speed, el_speed))
        self.ns.slew_fixed(NexstarDeviceId.AZM_RA_MOTOR,az_speed)
        self.ns.slew_fixed(NexstarDeviceId.ALT_DEC_MOTOR,-1*el_speed)

    ##### GOTO OPERATIONS ############
    def cancel_goto(self):
        self.ns.cancelGoto()

    def goto_position(self, az, el):
        print("Goto Az/El: {:f}/{:f}".format(self.tar_az, self.tar_el))
        self.ns.gotoPosition(az,el)

    def getTrackingMode(self):
        status_report(self.ns)
        align = self.ns.getAlignmentComplete()
        tm = self.ns.getTrackingMode()
        print("Get Tracking Mode:", align, tm)

    def set_tracking_mode(self, mode):
        if mode == 0:
            self.ns.setTrackingMode(NexstarTrackingMode.OFF)
            print("set tracking mode to OFF")
        elif mode == 1:
            self.ns.setTrackingMode(NexstarTrackingMode.ALT_AZ)
            print("set tracking mode to ALT AZ")

    def sync(self, az, el):
        print("Sync Scope - {:f}/{:f}".format(az,el))

        self.ns.sync(az, el)

    def init_frames(self):
        self.goto_fr = goto_frame(self)
        self.goto_fr.setFrameShape(Qt.QFrame.StyledPanel)

        self.sync_fr = sync_frame(self)

        self.pred_fr = gpredict_frame(self.cfg['gpredict'], self)

        self.slew_fr = slew_frame(self)
        self.slew_fr.setFrameShape(Qt.QFrame.StyledPanel)

        self.fb_fr = feedback_frame(self)
        self.fb_fr.setFrameShape(Qt.QFrame.StyledPanel)

        vbox1 = Qt.QVBoxLayout()
        #vbox1.addWidget(self.conn_fr)
        #vbox1.addStretch(1)
        vbox1.addWidget(self.pred_fr)
        vbox1.addWidget(self.fb_fr)
        vbox1.addWidget(self.sync_fr)
        vbox1.addStretch(1)

        vbox2 = Qt.QVBoxLayout()
        vbox2.addWidget(self.goto_fr)
        vbox2.addWidget(self.slew_fr)
        vbox2.addStretch(1)

        #vbox3 = Qt.QVBoxLayout()
        #vbox3.addWidget(self.fb_fr)
        #vbox3.addStretch(1)

        hbox1 = Qt.QHBoxLayout()
        hbox1.addLayout(vbox1)
        hbox1.addLayout(vbox2)
        #hbox1.addLayout(vbox3)
        #self.main_grid = Qt.QGridLayout()
        #self.main_grid.addLayout(vbox1,0,0,4,2)
        #self.main_grid.addWidget(self.slew_fr   ,0,2,1,3)
        #self.main_grid.addWidget(self.az_lcd_fr ,1,2,1,3)
        #self.main_grid.addWidget(self.az_ctrl_fr,2,2,1,3)
        #self.main_grid.addWidget(self.fb_fr     ,0,5,1,3)
        #self.main_grid.addWidget(self.el_lcd_fr ,1,5,1,3)
        #self.main_grid.addWidget(self.el_ctrl_fr,2,5,1,3)
        #self.main_grid.setRowStretch(0,1)
        #self.main_grid.setColumnStretch(2,1)
        #self.main_grid.setColumnStretch(5,1)
        #self.main_window.setLayout(self.main_grid)

        self.main_window.setLayout(hbox1)

    def set_callback(self, callback):
        self.callback = callback

    def closeEvent(self, *args, **kwargs):

        print("Closing GUI")
        self.update_timer.stop()
        self.ns.close()

    def darken(self):
        palette = Qt.QPalette()
        palette.setColor(Qt.QPalette.Background,QtCore.Qt.black)
        palette.setColor(Qt.QPalette.WindowText,QtCore.Qt.black)
        palette.setColor(Qt.QPalette.Text,QtCore.Qt.green)
        self.setPalette(palette)

    def utc_ts(self):
        return str(date.utcnow()) + " UTC | GUI | "
