#!/usr/bin/env python3

import socket
import os
import string
import sys
import time
import argparse
import datetime
import json
import subprocess
from binascii import *
from gui.nexstar_gui import *
#from track_gui import *
#from nexstar import *

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
    #print(chr(27) + "[2J")
    subprocess.run(["reset"])
    print(sys.path)
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

    #create nexstar object
    #ns = NexstarHandController(cfg['nexstar']['dev'])


    app = Qt.QApplication(sys.argv)
    app.setStyle('Windows')
    win = MainWindow(cfg)
    #win.set_callback(track)

    #win.setGpredictCallback(gpred)

    sys.exit(app.exec_())
    #ns.close()
    sys.exit()
