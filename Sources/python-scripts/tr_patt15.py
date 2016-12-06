#!/usr/bin/python
# coding: utf-8
#----------------------------------------------------------

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

pixpatt = [
            [ # unten nach oben
            [0,1,2,3,4,5,6,7,8,],     \
            [9,10,11,12,13,14,15],    \
            [16,17,18,19,20],         \
            [21,22,23],               \
            [24]                      \
            ],
            [   # links nach rechts
            [0,1,15,14,16,17,23,22,24],  \
            [2,3,13,12,18,19,21],    \
            [4,5,11,10,20],         \
            [6,7,9],               \
            [8]                      \
            ],
            [  # rechts nach links
            [8,7,9,10,20,19,21,22,24],   \
            [6,5,11,12,18,17,23],    \
            [4,3,13,14,16],         \
            [2,1,15],               \
            [0]                      
            ]
    ]



#  from lines2
def main():
    tr_defglobal.pattern=15

#    tr_defglobal.msg_line[1]=" - Muster 15 - "
 #   showmsg( tr_defglobal.msg_line)   # display ready message
    if tr_defglobal.debug: print "doing work15"

    x=len(pixpatt)
    while True:
        if  tr_defglobal.do_term: break             # break from main Loop
        if  tr_defglobal.type_switch: 
            switchoff()
            break             # break from main Loop

        y=randint(0,x-1)
        colo= (randint(0,255),randint(0,255),randint(0,255))    
        for i in pixpatt[y]:
            for j in i:             # fülle einen Zeile  
                tr_defglobal.pixels[j] =   color_function.bright(tr_defglobal.brightness, colo)
 #               if tr_defglobal.debug: print "Pixel: %d" % j
            tr_defglobal.client.put_pixels(tr_defglobal.pixels)
            time.sleep(float(10) / tr_defglobal.frameps)
      #  switchoff()
    sleep(0.1)




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
