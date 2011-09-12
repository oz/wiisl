About
=====

Wiisl is a weird and evil python script I wrote -- hey it's my first!

Wiisl, weasel or whistle... get it? Very bad pun, meh. Call it Wii
Script Launcher if you prefer.

It's currently running on an old Eee-pc at AF83's offices. The recycled
hardware is running shell-fm in the evenings, and is hooked up to a
decent sound system.  Therefore, wiisl is my sunday afternoon hack to
have a remote for it.

The code is rough, sorry about that, but at least it works for me.
Criticism is encouraged, pull-requests warmly welcomed. Anyway, HTH.

Installing
==========

Clone the Git depot at https://github.com/oz/wiisl

You need the following to run the `wiisl.py` script:

 * Python, well duh. I only checked the code against python 2.6.7.
 * The `cwiid` lib, and more importantly its python bindings. I used
   version `0.6.00+svn201-3` which is available in debian-ish boxen
   through `aptitude install python-cwiid`.

YMMV.

Running
=======

Run `./wiisl.py <WIIMOTE MAC ADDRESS>`

Hit the 1 and 2 buttons of your wiimote for wiisl to connect to it. The
LEDs 2 and 3 are lit up when the device is ready.

Configuring
===========

wiisl comes with a set of preconfigured scripts that are run crudely
when the appropriate event is detected on the Wiimote.

Those sit in the `scripts.d/` directory, and follow a naming losely
based on cwiid's [events constant names](https://github.com/abstrakraft/cwiid/blob/master/python/cwiidmodule.c).

For instance the `scripts.d/btn_a.sh` script is run when the `BTN_A`
event is detected. It corresponds to a push on the 'A' button of your
wiimote.

License
=======

This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <http://unlicense.org/>
