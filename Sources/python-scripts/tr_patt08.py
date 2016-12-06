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

pixpatt = [
            [ # unten nach oben
            [0,1,2,3,4,5,6,7,8],     \
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

shiftpatt = [
            [
            [22],
            [24],
            [17,18,19],
            [23,22,21],
            
            [14,13,12,11,10],
            [16,17,18,19,20],
            
            [1,2,3,4,5,6,7],
            [15,14,13,12,11,10,9]
            ]
            ]
posonwheel=0

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

def shiftlines():
   # print "len ", len(shiftpatt[0])
    for i in range(0,len(shiftpatt[0]),2):
        
    #    print (shiftpatt[0][i])
   #     print (shiftpatt[0][i+1])
        
        for j in range (len(shiftpatt[0][i])):

#            if debug:
 #               print "schiebe zeile %d pixel %d" % (i, (i*ledproline)+j)
            tr_defglobal.pixels[shiftpatt[0][i+1][j]]=tr_defglobal.pixels[shiftpatt[0][i][j]]
  #          print "shift von %d  nach %d" % (shiftpatt[0][i][j],shiftpatt[0][i+1][j])
	
	tr_defglobal.client.put_pixels(tr_defglobal.pixels)


#----- rainbow1
def main():
    global posonwheel
    tr_defglobal.pattern=8
    if tr_defglobal.debug: print "doing work8"
    posonwheel=0
    while True:

        if  tr_defglobal.do_term: break             # break from main Loop
        if  tr_defglobal.type_switch: break             # break from main Loop
                   # function color_wheel signals termination             
        shiftlines()

        time.sleep(0.05)
#        colo=color_wheel_r (debug,posonwheel, 50)     # get rgb values
        colo=wheel (posonwheel)     # get rgb values

        if tr_defglobal.debug: print colo
        if colo[0] < 0:                        # loop terminates, all colors done
            posonwheel=0   
            colo=wheel (posonwheel)     # get rgb values

        for i in pixpatt[0][0]:
            tr_defglobal.pixels [i]= color_function.bright(tr_defglobal.brightness,(colo[1][0],colo[1][1],colo[1][2])) 
            pass     
        tr_defglobal.client.put_pixels(tr_defglobal.pixels)
        posonwheel+=5
        if posonwheel>256: posonwheel=0
        if tr_defglobal.debug: print "Position5: %d" % posonwheel

        time.sleep(float(5) / tr_defglobal.frameps)

    switchoff()
    
    sleep(0.02)




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
