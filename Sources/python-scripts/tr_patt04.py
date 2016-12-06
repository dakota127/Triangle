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

# list alle pixels von innen nach aussen
# für alle 3 Seiten des Dreiecks
pixpatt2 = [
            [ # unten nach oben
            [4,12,18,22,24],     \
            [5,11,19,21,3,13,17,23],    \
            [6,10,20,2,14,16],         \
            [7,9,1,15],               \
            [0,8]                      \
            ],
            [   # links nach rechts
            [16,12,11,7,8],  \
            [17,18,10,9,14,13,5,6],    \
            [23,19,20,15,3,4],         \
            [1,2,22,21],               \
            [0,24]                      \
            ],
            [  # rechts nach links
            [20,12,13,1,0],   \
            [19,18,14,15,10,11,3,2],    \
            [9,5,4,21,17,16],         \
            [7,6,22,23],               \
            [24,8]                      
            ]
    ]



#----- Chase horizontal , Original, go through all pixels
def main():
    tr_defglobal.pattern=4

    if tr_defglobal.debug: print "doing work4"

    x=len(pixpatt2)
    while True:
        if  tr_defglobal.do_term: break             # break from main Loop
        if  tr_defglobal.type_switch: break             # break from main Loop

        y=randint(0,x-1)
        colo= (randint(128,200),randint(128,200),randint(128,200))    
        for i in pixpatt2[y]:
            for j in i:  
               
     #           pixels[j] = (color[x][0],color[x][1],color[x][2])
                tr_defglobal.pixels[j] =   color_function.bright(tr_defglobal.brightness, colo)

 #               if tr_defglobal.debug: print "Pixel: %d" % j
            tr_defglobal.client.put_pixels(tr_defglobal.pixels)
            time.sleep(float(4) / tr_defglobal.frameps)
    switchoff()
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
