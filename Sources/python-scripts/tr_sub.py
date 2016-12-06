#!/usr/bin/python
# coding: utf-8
#----------------------------------------------------------
#
#   Su Functions Triangle


import tr_defglobal
import time, datetime
from time import sleep
import os, datetime
from math import *
import spidev





#------- Funktion showmsg ---------------------------------
#        Display 2 Lines of text on CharPlate 16x2
def showmsg(output):
    if tr_defglobal.charplate:
        tr_defglobal.lcd.clear()
        tr_defglobal.lcd.message(output[0] + "\n"  + output[1])
    else: return()
# -------------------------------------------------------

# ***** Function blink-led **************************
def blink_led(GPIO,pin,anzahl):  # blink led 3 mal bei start und bei shutdown
        for i in range(anzahl):
            GPIO.output(pin, True)
            sleep(0.1)
            GPIO.output(pin, False)
            sleep(0.1)
#-------------------------
#---------------------------------------------
def switchoff():
 #   global tr_defglobal.pixels
    blackled=[(0,0,0)] * tr_defglobal.anzled
    tr_defglobal.client.put_pixels(blackled)

#----------------------------------------------

def wheel(pos):
#    Generate rainbow colors across 0-255 positions.
    if pos>255: return(-1,0)
    if pos < 85:
        return (0,(pos * 3, 255 - pos * 3, 0))
    elif pos < 170:
        pos -= 85
        return (0,(255 - pos * 3, 0, pos * 3))
    else:
        pos -= 170
        return (0,(0, pos * 3, 255 - pos * 3))


#---------------------------------------------

def brightness(prozent, colors):
    return (float(colors[0]*prozent/100), float(colors[1]*prozent/100), float(colors[2]*prozent/100 ))
    
#----------------------------------------------

# ***** Function do_test() **************************

def do_test2():
    sleep(0.2)
    col1=[(220,171,160)] * tr_defglobal.anzled
    col2=[(164,202,255)] * tr_defglobal.anzled
    col3=[(183,204,111)] * tr_defglobal.anzled

    blackled=[(0,0,0)] * tr_defglobal.anzled
 
    tr_defglobal.client.put_pixels(col1)
    sleep(2)
    tr_defglobal.client.put_pixels(blackled)
    sleep(2)
    tr_defglobal.client.put_pixels(col2)
    sleep(2)
    tr_defglobal.client.put_pixels(blackled)
    sleep(2)
    tr_defglobal.client.put_pixels(col3)
    sleep(2)
    tr_defglobal.client.put_pixels(blackled)


    sleep(2)




# ***** Class Debug to File **************************
class DebugToFileClass:
    """
        File-like object
        All print statements used for debugging can be redirected to this file
    """
    def __init__(self, filename, appname, tag=None, overwrite=True):
        self.filename = filename
        self.appname = appname
        self.tag = tag
        if os.path.exists(self.filename):
            if overwrite:
                os.remove(self.filename)
            now = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
            self.write("Logging started at %s ----" % now)
        else:
            # This will generate an error
            pass

    def write(self, msg):
        try:
            f = open(self.filename,'a')
            f.writelines(datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S') + ': ' + self.appname + ': ' + self.tag + ': ' + msg.strip() + '\n')
            f.flush()
            f.close()
        except:
            pass


# OLD OLD
# Channel must be an integer 0-7
def ReadChannel(channel):
  adc = tr_defglobal.spibus.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data

#  --------------------------------
# Function to read SPI data from MCP3008 chip
# Channel must be an integer 0-7

def get_adc(channel):
    if ((channel > 1) or (channel < 0)):
        return -1

    r = tr_defglobal.spibus.xfer2([1,(2+channel)<<6,0])
    ret = ((r[1]&31) << 6) + (r[2] >> 2)

    return ret



# Function to convert data to voltage level,
# rounded to specified number of decimal places.
def ConvertVolts(data,places):
    volts = round((data * 3.33) / float(1024), 2)
#    volts = (data * 5.1) / float(1023)
    volts = round(volts,places)
    return volts

# Function to calculate temperature from
# TMP36 data, rounded to specified
# number of decimal places.
def Convertentf(data,places):

  # ADC Value
  # (approx)  Volts  Distanz
  #    
  #  180    0.9     80 cm
  #  240    1.1     60 cm
  #  350    1.7     40 cm
  #  580    2.75    15 cm

  entf = ((data * 580)/float(580))-50
  entf = round(entf,places)
  return entf

def readentf():
    analogvalue1 = get_adc(0)
    analogvalue2 = get_adc(0)
    analogvalue3 = get_adc(0)
    
    wert=(analogvalue1+analogvalue2+analogvalue3)/3
 #   analogvalue1 = ReadChannel(0)
    volt = ConvertVolts(wert,2)
#    entfernung=Convertentf(analogvalue1,2)
 #   return(entfernung)
    return (wert)   

def readlight():
    analogvalue1 = get_adc(1)
    analogvalue2 = get_adc(1)
    analogvalue3 = get_adc(1)
    
    wert=(analogvalue1+analogvalue2+analogvalue3)/3
 #   analogvalue1 = ReadChannel(0)
    volt = ConvertVolts(wert,2)
#    entfernung=Convertentf(analogvalue1,2)
 #   return(entfernung)
    return (wert)   
