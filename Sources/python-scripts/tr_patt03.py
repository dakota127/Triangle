#!/usr/bin/env python
# coding: utf-8
#

#Import all modules
from __future__ import division
import sys, getopt, os
from time import sleep
import time, datetime
# COMMENT
import RPi.GPIO as GPIO
# ENDCOMMENT

import struct
from threading import Thread
from random import randint
import random
import tr_defglobal
from tr_sub import *
import signal
import platform
# import opc
from math import *
import color_utils
import color_function




#-----miami

def main():     # based on mymiami
    twinkle=1
    shiftcol=0
    tr_defglobal.pattern=3
    if tr_defglobal.debug: print "doing work3"

    while True:
        if  tr_defglobal.do_term: break             # break from main Loop
        if  tr_defglobal.type_switch: break             # break from main Loop

        t = time.time() - tr_defglobal.start_time

# Alle Pixel von 0 bis n_pixels bekommen neue Farbwerte  
#    print lednumber
        for pixelnummer in range(tr_defglobal.anzled):
            tr_defglobal.pixels[pixelnummer] = color_function.bright(tr_defglobal.brightness,color_function.pixel_colorx(t*0.6, tr_defglobal.coordinates[pixelnummer], pixelnummer, tr_defglobal.anzled, tr_defglobal.random_values,twinkle,shiftcol,tr_defglobal.debug))

#        
#   Hier die komplexere und optimierte Version dieser Statsments: 
#        pixels = [pixel_color(t*0.6, position, pixelnummer, n_pixels, random_values,1) for pixelnummer, position in enumerate(coordinates)]
# 
        tr_defglobal.client.put_pixels(tr_defglobal.pixels, channel=0)
        if tr_defglobal.debug: print "sleep for %f" % (5 / tr_defglobal.frameps)
        time.sleep(float(5) / tr_defglobal.frameps)
    



# *************************************************
# Program starts here
# *************************************************

if __name__ == '__main__':
    global term
    term=1
    main(1500)
#
#**************************************************************
#  That is the end
#***************************************************************
#        
