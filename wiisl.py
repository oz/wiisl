#!/usr/bin/env python

import sys
import time
import subprocess
import os, sys
import getopt
import re
from glob import glob
from time import sleep
from getopt import getopt

import cwiid
from cwiid import Wiimote

class Wiisl:
    def __init__(self, mac_address):
        self.omg_please_stop  = False
        self.wm               = cwiid.Wiimote(mac_address)
        self.wm.rpt_mode      = cwiid.RPT_STATUS | cwiid.RPT_BTN
        self.wm.mesg_callback = self.mesg_cb

        # Light up LEDs 2 and 3 when we're connected
        self.wm.led           = 2 | 4
        self.last_activity    = time.time()
        self._timeout         = 60
        self.script_dir       = "./scripts.d"

    def set_timeout(self, seconds):
        """Set inactivity timeout in seconds"""
        self._timeout = seconds

    def set_script_dir(self, path):
        """Set script dir path."""
        self.script_dir = path

    def mesg_cb(self, a, b):
        """When the wiimote is powered down, this mesg callback is
        called, and a is [(8, 1)]. I REALLY have no idea why, and not
        time to dig in cwiid's source code ATM.  Documentation would
        help. :)"""
        if a[0] == (8, 1):
            self.omg_please_stop = True

    def list_scripts(self):
        """List scripts in scripts.d/ directory, without their
        extension."""
        glob_exp = self.script_dir + "/*.sh"
        return [re.sub(r'.*/(.*)\.sh', r'\1', x) for x in glob(glob_exp)]

    def run_handler(self, handler):
        """Check self.wm.state['buttons'] value against each sh script
        in the scripts.d/ directory.  The script name is passed as
        'handler', it is uppercased to check:
          - wether the constant exists in cwiid
          - wether a button event matches

        Whenever both are true, the handler script is launched."""
        self.last_activity = time.time()
        const_name = handler.upper()
        try:
            const_value = getattr(cwiid, const_name)
            if self.wm.state['buttons'] == const_value:
                self.exec_script(handler)
        except AttributeError:
            return 0

    def run(self):
        """Main-loop, running while a wiimote is connected."""
        # I want to reload the list of scripts on each
        # disconnect/reconnect: it's easier to debug. :)
        scripts = self.list_scripts()
        while True:
            if 0 != self.wm.state['buttons']:
                [self.run_handler(script) for script in scripts]
            if self.omg_please_stop:
                self.omg_please_stop = False
                break
            # On timeout, close wiimote connection
            if self.inactive():
                self.wm.close()
                sleep(5)
                break
            sleep(0.1)

    def inactive(self):
        """Return True if no event was received for more that
        self._timeout seconds."""
        return time.time() - self.last_activity > self._timeout

    def vibrate(self, duration):
        """Vibrate for a while."""
        self.wm.rumble = 1
        sleep(duration)
        self.wm.rumble = 0

    def exec_script(self, script):
        """Run script if it exists in scripts.d/ directory"""
        filename = os.path.join(self.script_dir, script + ".sh")
        # http://docs.python.org/library/os.html#os.X_OK
        if os.access(filename, os.X_OK):
            with open(filename):
                subprocess.call(filename)
                self.vibrate(0.1)

if __name__ == "__main__":
    script_dir = "./scripts.d"
    opts, args = getopt(sys.argv[1:], 'hs:')

    def usage():
        sys.stderr.write("Usage: wyyrd.py [-s <script dir>] <wiimote mac address>\n")
        exit(1)

    if len(sys.argv) < 2:
        usage()

    for o, a in opts:
        if o == '-s':
            script_dir = a
        else:
            usage()

    wiimote_mac = args[0]
    print('Put your Wiimote in discoverable mode now: press 1+2...')
    while True:
        try:
            print('Waiting for wiimote ' + wiimote_mac)
            wm = Wiisl(wiimote_mac)
            wm.set_timeout(90)
            wm.set_script_dir(script_dir)
            wm.vibrate(0.1)
            print("Ready!")
            wm.run()
        except RuntimeError:
            # Never gonna give you up...
            continue
