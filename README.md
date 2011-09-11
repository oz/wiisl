About
=====

Wiird is a weird and evil python script I wrote -- hey it's my first!

Wiird, weird... get it? Very bad pun, meh.

It's currently running on an old Eee-pc at AF83's offices. The recycled
hardware is running shell-fm in the evenings, and is hooked up to a
decent sound system.  Therefore, wiird is my sunday afternoon hack to
have a remote for it.

The code is rough, sorry about that, but at least it works for me.
Criticism is encouraged, pull-requests warmly welcomed. Anyway, HTH.

Installing
==========

Clone the Git depot at https://github.com/oz/wiird

You need the following to run the `wiird.py` script:

 * Python, well duh. I only checked the code against python 2.6.7.
 * The `cwiid` lib, and more importantly its python bindings. I used
   version `0.6.00+svn201-3` which is available in debian-ish boxen
   through `aptitude install python-cwiid`.

YMMV.

Running
=======

Run `./wiird.py <WIIMOTE MAC ADDRESS>`

Hit the 1 and 2 buttons of your wiimote for wiird to connect to it. The
LEDs 2 and 3 are lit up when the device is ready.

Configuring
===========

wiird comes with a set of preconfigured scripts that are run crudely
when the appropriate event is detected on the Wiimote.

Those sit in the `scripts.d/` directory, and follow a naming losely
based on cwiid's [events constant names](https://github.com/abstrakraft/cwiid/blob/master/python/cwiidmodule.c).

For instance the `scripts.d/btn_a.sh` script is run when the `BTN_A`
event is detected. It corresponds to a push on the 'A' button of your
wiimote.
