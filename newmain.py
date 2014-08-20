#!/usr/bin/python

# Main script for Adafruit Internet of Things Printer 2.  Monitors button
# for taps and holds, performs periodic actions (Twitter polling by default)
# and daily actions (Sudoku and weather by default).
# Written by Adafruit Industries.  MIT license.
#
# MUST BE RUN AS ROOT (due to GPIO access)
#
# Required software includes Adafruit_Thermal, Python Imaging and PySerial
# libraries. Other libraries used are part of stock Python install.
#
# Resources:
# http://www.adafruit.com/products/597 Mini Thermal Receipt Printer
# http://www.adafruit.com/products/600 Printer starter pack

from __future__ import print_function
import RPi.GPIO as GPIO
import subprocess, time, Image, socket
from Adafruit_Thermal import *

import base64, HTMLParser, httplib, json, sys, urllib, zlib
import urllib, csv
import datetime
from datetime import datetime
from datetime import timedelta

from unidecode import unidecode
from Adafruit_Thermal import *

#import necessary libraries
import urllib
from urllib import *
#import urllib.request
import time



ledPin       = 18
buttonPin    = 23
holdTime     = 2     # Duration for button hold (shutdown)
tapTime      = 0.01  # Debounce time for button taps
nextInterval = 0.0   # Time of next recurring operation
dailyFlag    = False # Set after daily trigger occurs
lastId       = '1'   # State information passed to/from interval script
printer      = Adafruit_Thermal("/dev/ttyAMA0", 19200, timeout=5)






printed_messages = []
#create a function to find the messages
def get_messages():
    #open 40in20out
    f = urllib.urlopen('http://www.40in20out.com/subscribers/messages.xml')
    #get text from /sub/messages2
    text = str(f.read().decode('utf-8'))
    #create a list for all the messages on the site
    messages = []
    #run this loop while there are still more messages left to parse
    while text.find('messages') != -1:
        #parse the messages to find message_number, message_timestamp, message_type, and message_action
        message_number = text[text.find('messages msgnum="')+17:text.find('messages msgnum="')+23]
        text = text[text.find('messages msgnum="'):]
        #message_timestamp = text[text.find('timestamp="')+11:text.find('timestamp="')+30]
        message_timestamp = text[text.find('timestamp="')+11:text.find('timestamp="')+21] + " " + text[text.find('timestamp="')+22:text.find('timestamp="')+30]
        text = text[text.find('timestamp="'):]
        message_type = text[text.find('type="')+6:text.find('type="')+7]
        text = text[text.find('type="'):]
        message_action = text[text.find('action="')+8:text.find('"/>')]
        text = text[text.find('action="'):]
        #add the message to the messages list
        message = message_number, message_timestamp, message_type, message_action
        messages.append(message)
    #return the list of messages, this list will contain all the messages from /messages2.xml
    return messages
    




# Called when button is briefly tapped.  Invokes time/temperature script.
def tap():
  GPIO.output(ledPin, GPIO.HIGH)  # LED on while working
  subprocess.call(["python", "40in20out_positions.py"])
  GPIO.output(ledPin, GPIO.LOW)


# Called when button is held down.  Prints image, invokes shutdown process.
def hold():
  GPIO.output(ledPin, GPIO.HIGH)
  printer.printImage(Image.open('goodbye40in20out.png'), True)
  printer.feed(3)
  subprocess.call("sync")
  subprocess.call(["shutdown", "-h", "now"])
  GPIO.output(ledPin, GPIO.LOW)


# Called at periodic intervals (30 seconds by default).
# Invokes twitter script.
def interval():
  GPIO.output(ledPin, GPIO.HIGH)
  p = subprocess.Popen(["python", "40in20out.py", str(lastId)],
    stdout=subprocess.PIPE)
  GPIO.output(ledPin, GPIO.LOW)
  return p.communicate()[0] # Script pipes back lastId, returned to main


# Called once per day (6:30am by default).
# Invokes weather forecast and sudoku-gfx scripts.
def daily():
  GPIO.output(ledPin, GPIO.HIGH)
  subprocess.call(["python", "40in20out_positions.py"])
  #subprocess.call(["python", "forecast.py"])
  ## subprocess.call(["python", "sudoku-gfx.py"])
  GPIO.output(ledPin, GPIO.LOW)


# Initialization

# Use Broadcom pin numbers (not Raspberry Pi pin numbers) for GPIO
GPIO.setmode(GPIO.BCM)

# Enable LED and button (w/pull-up on latter)
GPIO.setup(ledPin, GPIO.OUT)
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# LED on while working
GPIO.output(ledPin, GPIO.HIGH)

# Processor load is heavy at startup; wait a moment to avoid
# stalling during greeting.
# time.sleep(30)

# Print greeting image
printer.feed(1)
printer.printImage(Image.open('40in20out_logo.bmp'), True)
printer.feed(1)
printer.print("40in20out")
printer.feed(1)
printer.print("Presented by...")
printer.feed(1)
printer.printImage(Image.open('totemasset_logo.bmp'), True)
printer.feed(2)
GPIO.output(ledPin, GPIO.LOW)

# Show IP address (if network is available)
try:
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(('8.8.8.8', 0))
	printer.print('My IP address is ' + s.getsockname()[0])
        ip = s.getsockname()[0]
	printer.feed(3)
except:
	printer.boldOn()
	printer.println('Network is unreachable.')
	printer.boldOff()
	printer.print('Connect display and keyboard\n'
	  'for network troubleshooting.')
	printer.feed(3)
	exit(0)



# Poll initial button state and time
prevButtonState = GPIO.input(buttonPin)
prevTime        = time.time()
tapEnable       = False
holdEnable      = False

# Main loop
while(True):



    found_messages = get_messages()
    #if all the found_messages have been printed, print no new messages
    #requires sorting
    found_messages.sort()
    printed_messages.sort()    
    #if found_messages == printed_messages:
    #    print('No New Messages')
    #enumerate through found_messages
    for i in found_messages:
        #if the message (i) has allready been printed, pass
        if i in printed_messages: pass
        #if the message (i) hasn't allready been printed, print the message
        else:
            #print("Message #:", i[0])
            #print("Message Timestamp:", i[1])
            #print("Message Type:", i[2])
            #print("Message Action:", i[3])
            #print('')
            #print("Message #:", i[0])
            print(i[1])
            #print("Message Type:", i[2])
            print(i[2])
            print(i[3])
            print('')
            
            if i[2] == "T":
                #printer.doubleWidthOn()
                #printer.inverseOn()
                printer.printImage(Image.open('40in20out_trade.bmp'), True)
                printer.feed(1)
                printer.inverseOn()
                printer.print ('{:<32}'.format(i[1]))
                #printer.print(i[1])
                printer.inverseOff()
                printer.feed(1)
                printer.boldOn()
                printer.print(i[3])
                printer.boldOff()
                #printer.doubleWidthOff()
                printer.feed(3)

            if i[2] == "2":
                #printer.doubleWidthOn()
                #printer.inverseOn()
                printer.printImage(Image.open('40in20out_2min.bmp'), True)
                printer.feed(1)
                printer.inverseOn()
                printer.print ('{:<32}'.format(i[1]))                
                #printer.print(i[1])
                printer.inverseOff()
                printer.feed(1)
                printer.print(i[3])
                #printer.doubleWidthOff()
                printer.feed(3)
                
            if i[2] == "A":
                #printer.doubleWidthOn()
                #printer.inverseOn()
                printer.printImage(Image.open('40in20out_alert.bmp'), True)
                printer.feed(1)
                printer.inverseOn()
                printer.print ('{:<32}'.format('         *** ALERT ***'))
                printer.inverseOff()
                printer.feed(1)
                printer.boldOn()
                printer.print(i[1])
                printer.boldOff()
                printer.feed(1)
                printer.print(i[3])
                printer.feed(1)
                printer.inverseOn()
                printer.print ('{:<32}'.format('         *** ALERT ***'))
                #printer.print('        *** ALERT ***         ')
                printer.inverseOff()
                printer.feed(1)
                printer.feed(3)
                
            if i[2] == "I":
                #printer.doubleWidthOn()
                #printer.inverseOn()
                printer.printImage(Image.open('40in20out_info.bmp'), True)
                printer.feed(1)
                printer.inverseOn()
                printer.print ('{:<32}'.format(i[1]))
                #printer.print(i[1])
                printer.inverseOff()
                printer.feed(1)
                printer.boldOn()
                printer.print(i[3])
                printer.boldOff()
                #printer.doubleWidthOff()
                printer.feed(3)
                
            #now that the message has been printed, add it to printed_messages list
            printed_messages.append(i)
    #wait 10 seconds before checking for more messages
    time.sleep(1)


  # Poll current button state and time
  buttonState = GPIO.input(buttonPin)
  t           = time.time()

  # Has button state changed?
  if buttonState != prevButtonState:
    prevButtonState = buttonState   # Yes, save new state/time
    prevTime        = t
  else:                             # Button state unchanged
    if (t - prevTime) >= holdTime:  # Button held more than 'holdTime'?
      # Yes it has.  Is the hold action as-yet untriggered?
      if holdEnable == True:        # Yep!
        hold()                      # Perform hold action (usu. shutdown)
        holdEnable = False          # 1 shot...don't repeat hold action
        tapEnable  = False          # Don't do tap action on release
    elif (t - prevTime) >= tapTime: # Not holdTime.  tapTime elapsed?
      # Yes.  Debounced press or release...
      if buttonState == True:       # Button released?
        if tapEnable == True:       # Ignore if prior hold()
          tap()                     # Tap triggered (button released)
          tapEnable  = False        # Disable tap and hold
          holdEnable = False
      else:                         # Button pressed
        tapEnable  = True           # Enable tap and hold actions
        holdEnable = True

  # LED blinks while idle, for a brief interval every 2 seconds.
  # Pin 18 is PWM-capable and a "sleep throb" would be nice, but
  # the PWM-related library is a hassle for average users to install
  # right now.  Might return to this later when it's more accessible.
  if ((int(t) & 1) == 0) and ((t - int(t)) < 0.15):
    GPIO.output(ledPin, GPIO.HIGH)
  else:
    GPIO.output(ledPin, GPIO.LOW)

  # Once per day (currently set for 6:30am local time, or when script
  # is first run, if after 6:30am), run forecast and sudoku scripts.
  l = time.localtime()
  if (60 * l.tm_hour + l.tm_min) > (60 * 6 + 30):
    if dailyFlag == False:
      daily()
      dailyFlag = True
  else:
    dailyFlag = False  # Reset daily trigger

  # Every 30 seconds, run Twitter scripts.  'lastId' is passed around
  # to preserve state between invocations.  Probably simpler to do an
  # import thing.
  if t > nextInterval:
    nextInterval = t + 15.0
    result = interval()
    if result is not None:
      lastId = result.rstrip('\r\n')

