from __future__ import print_function
import base64, HTMLParser, httplib, json, sys, urllib, zlib
import urllib, csv
import subprocess, time, Image, socket

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


printer   = Adafruit_Thermal("/dev/ttyAMA0", 19200, timeout=5)


#create a list of messages that have been printed
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
        message_timestamp = text[text.find('timestamp="')+11:text.find('timestamp="')+30]
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
#while True will run forever
while True:
    #Tell 'em we're checking messages!
    #print('Checking Messages...')
    #print('')
    #call get_messages() and save messages as found_messages
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
    time.sleep(10)
