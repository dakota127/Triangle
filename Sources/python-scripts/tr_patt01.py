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
    tr_defglobal.pattern=1
    if tr_defglobal.debug: print "doing work01"
    ledliste()
    oldcorner=1
    corners=(1,2,3)
    
    tr_defglobal.pixels = [ (0,0,0) ] * tr_defglobal.anzled

    
    saturation = 1
    bright = 0.8
    hue=1
    schlaf=0.4

    
    while True:
        if  tr_defglobal.do_term: break             # break from main Loop
        if  tr_defglobal.type_switch: break             # break from main Loop

        what=random.randint(1,150)
        if what >0: newcorner=1
        if what >90: newcorner=2
        if what >120: newcorner=3

  #      print "what, newcorner und gruppe", what ,newcorner, tr_defglobal.cornergroup[newcorner-1]
        
        ledact1=random.choice(tr_defglobal.cornergroup[newcorner-1])
   #     print "led, corner", ledact1, tr_defglobal.triacorner[ledact1][0]
      #  ledact1=random.choice(triangleled)
        ledact3=random.choice(triangleled)
        ledact4=random.choice(triangleled)

        saturation = 0.4
        bright = 0.6
        hue=random.random()
        
        nachb=tr_defglobal.neighbors[ledact1]
        
        
        if tr_defglobal.debug:
            print "led und neighbors: " ,(ledact1, nachb)

    # light up a random led
        r, g, b = map(lambda x:color_utils.remap(x,0.0,1.0,0,255), colorsys.hsv_to_rgb(hue, saturation, bright))
        tr_defglobal.pixels [ledact1]= r,b,g   
        
        
        # light up neighbors        
        saturation2=saturation-0.2
        r, g, b = map(lambda x:color_utils.remap(x,0.0,1.0,0,255), colorsys.hsv_to_rgb(hue, saturation2, bright))
        for z in  nachb:
 #           tr_defglobal.pixels [z]= r,b,g    
            tr_defglobal.pixels [z] =  color_function.bright(tr_defglobal.brightness, (r,b,g))
        tr_defglobal.pixels[ledact3]=(0,0,0)
        tr_defglobal.pixels[ledact4]=(0,0,0)

        
    # ok send the data
        tr_defglobal.client.put_pixels(tr_defglobal.pixels)

        oldcorner=tr_defglobal.triacorner[ledact1][0]       # save cuurent corner

        time.sleep(float(20) / tr_defglobal.frameps)

# Ende do while ----------------------
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
