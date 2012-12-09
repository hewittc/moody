#!/usr/bin/python
#
# Copyright (C) 2012 Christopher Hewitt
#
# Permission is hereby granted, free of charge, to any person obtaining a 
# copy of this software and associated documentation files (the "Software"), 
# to deal in the Software without restriction, including without limitation 
# the rights to use, copy, modify, merge, publish, distribute, sublicense, 
# and/or sell copies of the Software, and to permit persons to whom the 
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in 
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL 
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING 
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER 
# DEALINGS IN THE SOFTWARE.

import pygtk
pygtk.require("2.0")
import gtk
import sys
import socket
import getopt

class Moody:

    def __init__(self, host, port, lamp):
        self.host = host
        self.port = port
        self.lamp = lamp

        self.connect()

        color_selector = gtk.ColorSelection()
        color_selector.connect("color_changed", self.color_changed)
 
        window = gtk.Window()
        window.set_title("Moody: Moodlamp Color Selector")
        window.connect("delete_event", gtk.main_quit)
        window.set_border_width(10)
        window.add(color_selector)
        window.show_all()

        gtk.quit_add(gtk.main_level(), self.exit)
        gtk.main()

    def exit(self):
        self.disconnect()

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.socket.connect((host, port))
        except socket.error as msg:
            print("Unable to connect to %s:%s! %s") % (host, port, msg)
            self.disconnect()
            sys.exit(1)

    def disconnect(self):
        if self.socket is not None:
            self.socket.close()
            self.socket = None

    def color_changed(self, color_selector):
        color = color_selector.get_current_color()

        red = to_hex(color.red / 256)
        green = to_hex(color.green / 256)
        blue = to_hex(color.blue / 256)

        self.set_color(red, green, blue)

    def set_color(self, red, green, blue):
        if self.socket is not None:
            cmd = "003 %s %s %s %s\r\n" % (lamp, red, green, blue)
            self.socket.sendall(cmd)
        
def print_usage():
    print("Usage: %s [OPTION...]") % (sys.argv[0])
    print("`moody' is a simple moodlamp color changing interface for `mld'.\n")
    print("  -h HOST, --host HOST\tconnect to `mld' at HOST\t(default: %s)") % (host)
    print("  -p PORT, --port PORT\tconnect to `mld' at PORT\t(default: %s)") % (port)
    print("  -l LAMP, --lamp LAMP\tLAMP to control [0 for all]\t(default: %s)\n") % (lamp)
    print("  -?, --help\t\tthis usage information")

def to_hex(val):
    h = hex(val)[2:]
    if val < 0x10:
        h = "0" + h
    return h

if __name__ == "__main__":

    host = "127.0.0.1"
    port = 2324
    lamp = 0

    try:
        opts, args = getopt.getopt(sys.argv[1:], "h:p:l:d?", ["host=", "port=", "lamp=", "debug", "help"])
    except getopt.GetoptError:
        print_usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--host"):
            host = arg
        elif opt in ("-p", "--port"):
            port = int(arg)
        elif opt in ("-l", "--lamp"):
            lamp = int(arg)
        elif opt in ("-?", "--help"):
            print_usage()
            sys.exit(1)

    moody = Moody(host, port, lamp)

# vim: autoindent tabstop=4 shiftwidth=4 expandtab softtabstop=4 filetype=python
