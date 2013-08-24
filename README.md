Google Voice Click2Call
=======================

What
----
Initiate a Click2Call with your Google Voice account, from the command line. Your phone will ring, and when you answer, you will be connected to the number you specify (using the `t:` argument; see _Usage_ below).

Installation
------------
This script will try to write in `cookies.txt`, so make sure this file exists and is writable, or that the user running the script (apache, http, nobody?) has the necessary permissions to create that file.

It also needs _simplejson_: `sudo easy_install simplejson` (or modify the simplejson import to just __import json__, if you use Python 2.6+), and _Mechanize_: `sudo easy_install mechanize`

And evidently, you will need a valid username and password that has access to Google Voice.

`GV_USERNAME` is the (@gmail.com) email address, `GV_PASSWORD` is pretty self-explanatory, and you will want to define a `GV_CALLBACK_NUMBER` phone number (that starts with +1), which is the default phone number that will be called first during the Click2Call handshake.  
If you don't define a default `GV_CALLBACK_NUMBER`, make sure you call this script with a `f:...` argument, to define the callback number to use. That number needs to already be defined in your Google Voice settings.

Usage
-----
`python google-voice-click2call.py f:+15145551212 t:14181234567`

`f:` defines the callback number (your own number). It is optional if you define a default `GV_CALLBACK_NUMBER` in the script. It should always start with __1+__  
`t:` defines the number you want to call (the third-party number). This argument is mandatory.
