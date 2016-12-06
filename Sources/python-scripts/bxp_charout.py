#!/usr/bin/python
# coding: utf-8
#----------------------------------------------------------
#
#   Su Functions 16x2 LCD Display Output
#
#----------------------------------------------------------



from Adafruit_CharLCD_b import Adafruit_CharLCD
# use _b for use of backlight, siehe Notizen Adafruit_CharLCD_b  !!!! -----------

from Adafruit_MCP230xx import MCP230XX_GPIO

from subprocess import *
from time import sleep, strftime
from datetime import datetime

import bxp_defglobal
import os, sys

cmd = "ip addr show eth0 | grep inet | awk '{print $2}' | cut -d/ -f1"

bus = 1         # Note you need to change the bus number to 0 if running on a revision 1 Raspberry Pi.
address = 0x20  # I2C address of the MCP230xx chip.
gpio_count = 8  # Number of GPIOs exposed by the MCP230xx chip, should be 8 or 16 depending on chip.


def run_cmd(cmd):
    p = Popen(cmd, shell=True, stdout=PIPE)
    output = p.communicate()[0]
    return output


#------- Funktion Initchar ---------------------------------
#        Display 2 Lines of text on CharPlate 16x2
# Create MCP230xx GPIO adapter.
def charout_init():

    if not bxp_defglobal.lcd_attached:
        print "---> No LCD Attached...."
        return(99)
        
    mcp = MCP230XX_GPIO(bus, address, gpio_count)

# Create LCD, passing in MCP GPIO adapter.
    bxp_defglobal.lcd = Adafruit_CharLCD(pin_rs=1, pin_e=2, pins_db=[3,4,5,6], GPIO=mcp, pin_b=7)
    bxp_defglobal.lcd.begin(16, 1)
    bxp_defglobal.lcd.backlight(True)
    return(0)


#------- Funktion showmsg ---------------------------------
#        Display 2 Lines of text on CharPlate 16x2
def charout_write(output,debug):
    if bxp_defglobal.lcd_attached==1:
        bxp_defglobal.lcd.clear()
        string=output[0:31]                 # only output 32 chars
        if debug:
            print "\nbxp_charout: %d %s" % (len(string), string)
        bxp_defglobal.lcd.message(string)
    else: return()
# -------------------------------------------------------

def charout_off():
    bxp_defglobal.lcd.clear()
    bxp_defglobal.lcd.backlight(False)



# *************************************************
# Program starts here, let's roll
# *************************************************

if __name__ == '__main__':

    bxp_defglobal.appname=os.path.basename(__file__)
#
    charout_init()
    bxp_defglobal.lcd.message("CharOut Testing")
    sleep(2)
    while True:
        try:
            bxp_defglobal.lcd.clear()
            ipaddr = run_cmd(cmd)
            
    # first version of output
            bxp_defglobal.msg_line=datetime.now().strftime('%b %d  %H:%M:%S\n') + "\n" + 'IP %s' % (ipaddr)
            charout_write (bxp_defglobal.msg_line)
    # second version of output
            sleep(1)
            bxp_defglobal.lcd.clear()
            bxp_defglobal.lcd.message(datetime.now().strftime('%b %d  %H:%M:%S\n'))
            bxp_defglobal.lcd.message('IP %s' % (ipaddr))
            for z in range(16):
                bxp_defglobal.lcd.DisplayLeft()
                sleep(0.1)
            sleep(1)
        except KeyboardInterrupt:
    # aufräumem
            charout_off()
            sys.exit(0)     #  Abschlussvearbeitung

