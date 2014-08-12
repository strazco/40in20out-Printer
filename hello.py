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

#global tapEnable
#global holdEnable
#global buttonState
#global prevButtonState
#global tapTime
#global prevTime
#global holdTime

ledPin       = 18
buttonPin    = 23
holdTime     = 2     # Duration for button hold (shutdown)
tapTime      = 0.01  # Debounce time for button taps
nextInterval = 0.0   # Time of next recurring operation
dailyFlag    = False # Set after daily trigger occurs
lastId       = '1'   # State information passed to/from interval script
printer      = Adafruit_Thermal("/dev/ttyAMA0", 19200, timeout=5)

is_printing = False


# Called when button is briefly tapped.  Invokes time/temperature script.
def tap():
  GPIO.output(ledPin, GPIO.HIGH)  # LED on while working
  subprocess.call(["python", "40in20out_positions.py"])  
  #global is_printing
  #if is_printing == False:
  #  is_printing = True
  #  subprocess.call(["python", "40in20out_positions.py"])
  #  is_printing = False
  #else:
  #  #sleep(5)
  #  tap()
  # lastId = '1'
  # time.sleep(5)
  # interval()
  GPIO.output(ledPin, GPIO.LOW)


def main():
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

    # Show IP address (if network is available)
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 0))
        printer.print('IP address is ' + s.getsockname()[0])
        ip = s.getsockname()[0]
        printer.feed(3)
    except:
        printer.boldOn()
        printer.println('Network is unreachable.')
        printer.boldOff()
        printer.print('Connect display and keyboard\n'
        'for network troubleshooting.')
        printer.feed(3)

if __name__ == "__main__":
    main()
