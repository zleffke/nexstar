#!/usr/bin/env python3
#version 2.1

import socket
import os
import string
import sys
import time
import argparse
import datetime
import json
from binascii import *
#from track_gui import *
from nexstar import *

if __name__ == '__main__':
    """ Main entry point to start the service. """
    startup_ts = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    #--------START Command Line argument parser------------------------------------------------------
    parser = argparse.ArgumentParser(description="VTGS Tracking Client",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    cwd = os.getcwd()
    cfg_fp_default = '/'.join([cwd, 'config'])
    cfg = parser.add_argument_group('Configuration File')
    cfg.add_argument('--cfg_path',
                       dest='cfg_path',
                       type=str,
                       default='/'.join([os.getcwd(), 'config']),
                       help="Daemon Configuration File Path",
                       action="store")
    cfg.add_argument('--cfg_file',
                       dest='cfg_file',
                       type=str,
                       default="config.json",
                       help="Daemon Configuration File",
                       action="store")
    args = parser.parse_args()
#--------END Command Line argument parser------------------------------------------------------
    print(chr(27) + "[2J")
    fp_cfg = '/'.join([args.cfg_path,args.cfg_file])
    print (fp_cfg)
    if not os.path.isfile(fp_cfg) == True:
        print('ERROR: Invalid Configuration File: {:s}'.format(fp_cfg))
        sys.exit()
    print('Importing configuration File: {:s}'.format(fp_cfg))
    with open(fp_cfg, 'r') as json_data:
        cfg = json.load(json_data)
        json_data.close()

    #configure main log configs
    log_name = '.'.join([cfg['main']['name'],'main'])
    log_path = '/'.join([cfg['main']['log']['path'],startup_ts])
    cfg['main']['log'].update({
        'name':log_name,
        'startup_ts':startup_ts,
        'path':log_path
    })
    if not os.path.exists(cfg['main']['log']['path']):
        os.makedirs(cfg['main']['log']['path'])

    for key in cfg['thread_enable'].keys():
        #cfg[key].update({'log':{}})
        log_name =  '.'.join([cfg['main']['name'],cfg[key]['name']])
        cfg[key].update({
            'main_log':cfg['main']['log']['name']
        })
        cfg[key]['log'].update({
            'path':cfg['main']['log']['path'],
            'name':log_name,
            'startup_ts':startup_ts,
        })

    print (json.dumps(cfg, indent=4))
    #sys.exit()
    #track = vtp(options.ip, port, options.uid, options.ssid, 2.0)
    ns = NexstarHandController(cfg['nexstar']['dev'])
    #track = vtp(cfg)


    #print("Model: {}".format(ns.getModel()))

    [last_az,last_el] = ns.getPosition()
    print("Current Az: {:f}".format(last_az))
    print("Current El: {:f}".format(last_el))
    az_err = 1.0
    el_err = 1.0
    time.sleep(1)
    print("Slewing to 0,0")
    ns.gotoPosition(0,0)

    #while ((abs(az_err)>=0.01) and (abs(el_err)>=0.01)):
    while ns.getGotoInProgress():
        [cur_az,cur_el] = ns.getPosition()
        print("Current Az/El: {:f}/{:f}".format(cur_az,cur_el))
        az_err = cur_az - last_az
        el_err = cur_el - last_el
        print("  Error Az/El: {:f}/{:f}".format(az_err,el_err))
        last_az = cur_az
        last_el = cur_el
        #print(ns.getGotoInProgress())

    #dev_ver = ns.getDeviceVersion(0)
    #print(dev_ver)

    status_report(ns)

    print("Home!!!...")

    print("slewing...")
    count = 0
    now = datetime.datetime.utcnow()
    stop_time = now + datetime.timedelta(seconds=5)
    ns.slew_fixed(NexstarDeviceId.AZM_RA_MOTOR,9)
    while (stop_time - now).total_seconds() > 0:
        #ns.slew_fixed(NexstarDeviceId.AZM_RA_MOTOR,9)
        [cur_az,cur_el] = ns.getPosition()
        now = datetime.datetime.utcnow()
        print("{:s} | Current Az/El: {:f}/{:f}".format(now.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),cur_az,cur_el))

    ns.slew_fixed(NexstarDeviceId.AZM_RA_MOTOR,0)

    [cur_az,cur_el] = ns.getPosition()
    print("Current Az/El: {:f}/{:f}".format(cur_az,cur_el))

    ns.close()

    sys.exit()

    #app = QtGui.QApplication(sys.argv)
    #win = MainWindow(cfg)
    #win.set_callback(track)

    #win.setGpredictCallback(gpred)

    sys.exit(app.exec_())
    sys.exit()
