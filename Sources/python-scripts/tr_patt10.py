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

# import opc
from math import *
import color_utils
import color_function

import time,sys


twinkle=0
shiftcol=0


#----- lavalamp
def main():
    tr_defglobal.pattern=10
    if tr_defglobal.debug: print "doing work10"

    start_time = time.time()
    tr_defglobal.pixels = []

    while True:

        if  tr_defglobal.do_term: break             # break from main Loop
        if  tr_defglobal.type_switch: break             # break from main Loop
                   # function color_wheel signals termination             
        random_values = [random.random() for ii in range(tr_defglobal.anzled)]

        start_time = time.time()
        for z in range(2000):
            if  tr_defglobal.do_term: break             # break from main Loop
            if  tr_defglobal.type_switch: break             # break from main Loop

            t = time.time() - start_time
            tr_defglobal.pixels = [color_function.pixel_colorx(t*0.6, coord, ii, tr_defglobal.anzled, random_values,0,tr_defglobal.shiftcol,tr_defglobal.debug) for ii, coord in enumerate(tr_defglobal.coordinates)]
            tr_defglobal.client.put_pixels(tr_defglobal.pixels)
            time.sleep(float(1) / tr_defglobal.frameps)
        
                # folgendes vereinfacht von nachstehend.... bxp
        #for pixelnummer in range(tr_defglobal.anzled):
   
          #  tr_defglobal.pixels[pixelnummer] = color_function.bright(tr_defglobal.brightness,color_function.pixel_colorx(t*0.6, tr_defglobal.coordinates[pixelnummer], pixelnummer, tr_defglobal.anzled, tr_defglobal.random_values,twinkle,shiftcol,tr_defglobal.debug))


    switchoff()
    
    sleep(0.1)




# *************************************************
# Program starts here
# *************************************************

if __name__ == '__main__':
    global term
    term=1
    main()
#
#**************************************************************
#  That is the end
#***************************************************************
#        
