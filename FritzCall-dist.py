#!/usr/bin/env python

#
# Enable Monitor in Fritzbox by #96*5* on any phone connected to FritzBox
#

import socket
import time
import PySimpleGUI as sg
from fritzconnection.lib.fritzphonebook import FritzPhonebook

# TCP connection settings.
TCP_IP = '192.168.1.1'
TCP_PORT = 1012
BUFFER_SIZE = 1024
PASS='please_give_the_fritzbox_pw_for_phonebook'
data = "No call yet"

# Specifiy the Layout
sg.theme('DarkAmber')
# Set some generic layout options
sg.SetOptions(autoclose_time = 15, window_location = (100,100))

# connect to the FritzBox
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))

# get Adress data of the Fritzbox if available
fp = FritzPhonebook(address=TCP_IP, password=PASS)
for phonebook_id in fp.phonebook_ids:
    contacts = fp.get_all_numbers(phonebook_id)

while True:
    data = s.recv(BUFFER_SIZE)

    # Split the string to an array to handle number and case separately
    calldata = data.decode().split(';')

    # was this a call? Or something else (then ignore)
    if 'CALL' in calldata[1] or 'RING' in calldata[1]:

        # do we have a number?
        if 'CALL' in calldata[1]:
            number = calldata[5]
            direction = "Ausgehend Anruf"
        else:
            if calldata[3] == '':
                number = "Unknown"
            else:
                number = calldata[3]

            direction = "Eingehend Anruf"

        print( number, "|", calldata, "|", data ) 
        # is the number known to us (in Fritz Box Adress Book?)
        if number in contacts:
            sg.Popup(direction, number, contacts.get(number, "none"), keep_on_top = True, no_titlebar = True, grab_anywhere = True, auto_close = False )
        else:
            sg.Popup(direction, number, keep_on_top = True, no_titlebar = True, grab_anywhere = True, auto_close = False )

    # just to be sure...            
    time.sleep(0.05)
    calldata = "Null"

# clean up
window.close()
s.close()
