from __future__ import print_function
import base64, HTMLParser, httplib, json, sys, urllib, zlib
import urllib, csv
import subprocess, time, Image, socket

import datetime
from datetime import datetime
from datetime import timedelta
import time

from unidecode import unidecode


from Adafruit_Thermal import *

#import settings
#from utils import Printer

#printer = Printer("/dev/ttyAMA0", 19200, timeout=5)
printer = Adafruit_Thermal("/dev/ttyAMA0", 19200, timeout=5)



def main():

    #printer.printImage(Image.open('gfx/40in20out_positions.bmp'), True)
    printer.feed(1)
    printer.boldOn()
    #printer.print("      " +time.strftime("%m/%d/%Y") + " " + time.strftime("%I:%M:%S"))
    printer.boldOff()
    printer.feed(1)
    url = "http://www.40in20out.com/subscribers/messages.asp?id=test"
    webpage = urllib.urlopen(url)
    datareader = csv.reader(webpage)
    data = []


    for index, row in enumerate(datareader):
        if index == 1:
            continue
        if row:
            data.append(row)

    for row in data:
        msgnum = row[0]
        data_row = {
                    'type': row[1],
                    'timestamp': row[2],
                    'message': row[3],
                    }
        print_row(row)

    printer.feed(3)

def print_row(data_row):
    '''just prints a row of data'''
    cType = '%(type)s' % data_row
    cTimestamp = '%(timestamp)s' % data_row
    cMessage = '%(message)s' % data_row
    line1 = cTimestamp + ": " + cMessage
    #line2 = "           " + cLast.rjust(4) + cNet.rjust(5) 

    #if data_row['position'] != '0':
    #printer.print(' '+'{:<31}'.format(line1))
    printer.print(line1)
    printer.feed(1)



if __name__ == "__main__":
    main()

