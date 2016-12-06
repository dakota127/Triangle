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

pixpatt3=[12,11,5,4,3,13,18,19,10,6,2,14,16,17,23,22,21,20,9,8,0,15,24]
pixpatt4=[0,1,15,14,16,17,22,23,24,21,19,20,10,9,8,7,6,5,4,3,2,13,12,18,11]
pixpatt5=[8,7,9,10,20,19,21,22,24,23,17,16,14,15,1,0,2,3,4,5,6,11,12,18,13]



#----- Chase horizontal , Original, go through all pixels

#----- Chase horizontal , Original, go through all pixels
def main():
    tr_defglobal.pattern=6
    if tr_defglobal.debug: print "doing work6"
    wheelpos=1
    while True:
        if  tr_defglobal.do_term: break             # break from main Loop
        if  tr_defglobal.type_switch: break             # break from main Loop
        wheelpos+=1
        colo= (randint(0,255),randint(0,255),randint(0,255))    
        ra=randint(1,20)
        if ra>10:
            for i in pixpatt4:
                colo=wheel(wheelpos)
                tr_defglobal.pixels[i] = color_function.bright(tr_defglobal.brightness,(colo[1][0],colo[1][1],colo[1][2]))  
                tr_defglobal.client.put_pixels(tr_defglobal.pixels)
                time.sleep(float(1) / tr_defglobal.frameps)
                wheelpos+=10
                if wheelpos>254: wheelpos=randint(50,250)
            for i in reversed(pixpatt4):
                tr_defglobal.pixels[i] = tr_defglobal.BLACKCOL
                tr_defglobal.client.put_pixels(tr_defglobal.pixels)
                time.sleep(float(1) / tr_defglobal.frameps)
        else:
            for i in pixpatt5:
                colo=wheel(wheelpos)
                tr_defglobal.pixels[i] = color_function.bright(tr_defglobal.brightness,(colo[1][0],colo[1][1],colo[1][2]))
                tr_defglobal.client.put_pixels(tr_defglobal.pixels)
                time.sleep(float(1) / tr_defglobal.frameps)
                wheelpos+=10
                if wheelpos>254: wheelpos=randint(50,250)
                
            for i in reversed(pixpatt5):
                tr_defglobal.pixels[i] = tr_defglobal.BLACKCOL
                tr_defglobal.client.put_pixels(tr_defglobal.pixels)
                time.sleep(float(1) / tr_defglobal.frameps)


        colo= (randint(0,255),randint(0,255),randint(0,255))    
        if  tr_defglobal.do_term: break             # break from main Loop
        if  tr_defglobal.type_switch: break             # break from main Loop

        for i in pixpatt3:
            tr_defglobal.pixels[i] = color_function.bright(tr_defglobal.brightness,colo)
            tr_defglobal.client.put_pixels(tr_defglobal.pixels)
            time.sleep(float(1) / tr_defglobal.frameps)
        for i in reversed(pixpatt3):
            tr_defglobal.pixels[i] = tr_defglobal.BLACKCOL
            tr_defglobal.client.put_pixels(tr_defglobal.pixels)
            time.sleep(float(1) / tr_defglobal.frameps)


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
