#!/usr/bin/env python

import sys
import time
import subprocess
import os.path
import re
from glob import glob
from time import sleep

import cwiid
from cwiid import Wiimote

class Wiird:
    def __init__(self, mac_address):
        self.omg_please_stop  = False
        self.wm               = cwiid.Wiimote(mac_address)
        self.wm.rpt_mode      = cwiid.RPT_STATUS | cwiid.RPT_BTN
        self.wm.mesg_callback = self.mesg_cb

        # Light up LEDs 2 and 3 when we're connected
        self.wm.led           = 2 | 4

    # When the wiimote is powered down, this mesg callback is called,
    # and a is [(8, 1)]. I REALLY have no idea why, and not time to dig
    # in cwiid's source code ATM.  Documentation would help. :)
    def mesg_cb(self, a, b):
        if a[0] == (8, 1):
            self.omg_please_stop = True

    # List scripts in scripts.d/ directory, without their extension.
    def list_scripts(self):
        return [re.sub(r'.*/(.*)\.sh', r'\1', x) for x in glob("./scripts.d/*.sh")]

    # Check self.wm.state['buttons'] value against each sh script in the
    # scripts.d/ directory.  The script name is passed as 'handler', it
    # is uppercased to check:
    #   - wether the constant exists in cwiid
    #   - wether a button event matches
    #
    # Whenever both are true, the handler script is launched.
    def run_handler(self, handler):
        const_name = handler.upper()
        try:
            const_value = getattr(cwiid, const_name)
            if self.wm.state['buttons'] == const_value:
                self.exec_script(handler)
        except AttributeError:
            return 0

    # Main-loop, running while a wiimote is connected.
    def run(self):
        # I want to reload the list of scripts on each
        # disconnect/reconnect: it's easier to debug. :)
        scripts = self.list_scripts()

        while True:
            if 0 != self.wm.state['buttons']:
                [self.run_handler(script) for script in scripts]
            if self.omg_please_stop:
                self.omg_please_stop = False
                break
            sleep(0.1)

    # Vibrate for a while.
    def vibrate(self, duration):
        self.wm.rumble = 1
        sleep(duration)
        self.wm.rumble = 0

    # Run script if it exists in scripts.d/ directory
    def exec_script(self, script):
        filename = "./scripts.d/" + script + ".sh" 
        # FIXME
        # Stackoverflow pretends this is the prefered way to verify that
        # a file exist, I say it's ugly. Plus I should check for exec
        # rights. :p
        try:
            open(filename)
        except IOError as e:
            return 0
        subprocess.call(filename)
        self.vibrate(0.3)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: wyyrd.py <wiimote mac address>")
        exit(1)

    wiimote_mac = sys.argv[1]
    print('Put your Wiimote in discoverable mode now: press 1+2...')
    while True:
        try:
            print('Waiting for wiimote ' + wiimote_mac)
            wm = Wiird(wiimote_mac)
            print("Ready!")
            wm.run()
        except RuntimeError:
            # Never gonna give you up...
            continue
