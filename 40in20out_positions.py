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

#MODIFY THIS TUPLE TO CHANGE THE ORDER
order = (
     'FIXED INCOME', 'EQUITIES',
     'FX', 'METALS', 'ENERGY',
     'GRAINS', 'SOFTS', 'LIVESTOCK',
     )

def main():

    printer.printImage(Image.open('40in20out_positions.bmp'), True)
    printer.feed(1)
    printer.boldOn()
    printer.print("      " +time.strftime("%m/%d/%Y") + " " + time.strftime("%I:%M:%S"))
    printer.boldOff()
    printer.feed(1)
    url = "http://www.40in20out.com/subscribers/positions.asp?id=test"
    webpage = urllib.urlopen(url)
    datareader = csv.reader(webpage)
    data = []


    for index, row in enumerate(datareader):
        if index == 1:
            continue
        if row:
            data.append(row)

    #order data to a dict per sector
    data_dict = {}

    for row in data:
        sector = row[2]
        data_row = {
                    'symbol': row[0],
                    'description': row[1],
                    'position': row[3],
                    'days': row[4],
                    'p_init': row[5],
                    'last': row[6],
                    'net': row[7],
                    'ote': row[8],
                    'rewrsk': row[9],
                }
        if data_dict.get(sector):
            data_dict[sector].append(data_row)
        else:
            data_dict[sector] = [data_row]

    print_all(data_dict)
    printer.feed(3)

def print_row(data_row):
    '''just prints a row of data'''
    nPos = '%(position)s' % data_row
    #nPos.ljust(6, ' ')
    #full_string = '%(symbol)s %(position)s %(last)s %(net)s %(ote)s' % data_row
    cSymb = '%(symbol)s' % data_row
    #cSymb.rstrip()
    #cSymb.ljust(6, ' ')
    cLast = '%(last)s' % data_row
    cLast.rstrip()
    #cLast.ljust(12, ' ')
    cP_init = '%(p_init)s' % data_row
    #cP_init.ljust(12, ' ')
    cNet = '%(net)s' % data_row
    cNet.rstrip()
    #cNet.ljust(12, ' ')
    cDays = '%(days)s' % data_row
    #cDays.ljust(4, ' ')
    cOte = "%(ote)s" % data_row
    cOte.rstrip()
    #cOte.ljust(12, ' ')
    cRR = "%(rewrsk)s" % data_row
    #cRR.ljust(6, ' ')
    cDesc = "%(description)s" % data_row
    #cDesc.ljust(12, ' ')
    #line1 = cSymb + ' ' + cLast + cNet
    #TODO: review this order
    #line2 = nPos + "(" + cDays + ")" + cP_init + cOte
    line1 = nPos.rjust(4,' ') + " " + cSymb.rjust(6) +  cP_init.rjust(4) + "   " + cOte.rjust(4)
    line2 = "           " + cLast.rjust(4) + cNet.rjust(5) 

    if data_row['position'] != '0':
       #printer.print(' '+'{:<31}'.format(line1))
       printer.print(line1)
       printer.feed(1)
       printer.print(line2)
       printer.feed(1)


def print_all(data):
    for key in order:
        item = data.get(key)
        if not item:
            continue
        #sector
        #printer.feed(1)
        printer.inverseOn()
        #printer.print(key.upper())
        printer.print(' '+ '{:<31}'.format(key.upper()))
        printer.inverseOff()
        printer.feed(1)

        for row in item:
            print_row(row)
            #printer.feed(1)

if __name__ == "__main__":
    main()

