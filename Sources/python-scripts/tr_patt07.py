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
from colorwheel import *
import colorsys


triangleled=list()
triangle = [
    [[0,1,2,3,4,5,6,7,8],[15,14,13,12,11,10,9],[16,17,18,19,20],[23,22,21],[24]],
    [[36,28,27,19,18,10,9,1,0],[29,21,20,12,11,3,2],[22,14,13,5,4],[15,7,6],[64]],
    [[36,28,29,21,22,14,15,7,64],[27,19,20,12,13,5,6],[18,10,11,3,4],[9,1,2],[0]]
]

#------------------------
# alle led des dreieckes in Liste fassen - für später random
def ledliste():
    global triangleled
    for tria in range (len(triangle[0])):
        for led in range(len(triangle[0][tria])):
            triangleled.append(triangle[0][tria][led])
        
    if tr_defglobal.debug:
        print "Alle Led: %s \nLed-anzahl %d" % (triangleled, len(triangleled))
# nun haben wir liste aller led's im dreieck
#---------------------------------


#----- from random1
def main():
    tr_defglobal.pattern=7
    if tr_defglobal.debug: print "doing work5"
    ledliste()
    while True:
        if  tr_defglobal.do_term: break             # break from main Loop
        if  tr_defglobal.type_switch: break             # break from main Loop

        ledact1=random.choice(triangleled)
        ledact2=random.choice(triangleled)
        colact=random.randint(0,1500)
        colo=color_wheel_r (0,colact,50)     # get rgb values
        
        saturation = 0.6
        bright = 0.6
        hue=random.random()
        what=random.choice(triangleled)

        r, g, b = map(lambda x:color_utils.remap(x,0.0,1.0,0,255), colorsys.hsv_to_rgb(hue, saturation, bright))
    #    print r,g,b
        tr_defglobal.pixels [ledact1]= r,b,g     


#        tr_defglobal.pixels [ledact1]= color_function.bright(tr_defglobal.brightness, (colo[1][0],colo[1][1],colo[1][2]) )     
        tr_defglobal.pixels[ledact2]=(0,0,0)

        tr_defglobal.client.put_pixels(tr_defglobal.pixels)

        time.sleep(float(5) / tr_defglobal.frameps)

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
