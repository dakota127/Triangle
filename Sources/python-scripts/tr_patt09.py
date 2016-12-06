
#Import all modules
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
import colorsys
import color_function

import time,sys

import itertools


snake_length =10
snake_head = 0
snake_head_i=[0,8,24]
hue = 0
saturation = 0
value = 0
anzpixel=48  # snake braucht das....

pixpatt = [
            
            [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24],  
            [8,7,9,10,20,19,21,22,24,23,17,18,12,11,5,6,4,3,13,14,16,15,1,2,0], 
            [24,22,23,17,16,14,15,1,0,2,3,13,12,18,19,21,20,10,11,5,4,6,7,9,8]

    ]

def snake(start):
    global snake_length, snake_head, hue, tick
    if tr_defglobal.debug: print "doing snake %d head: %d" % (start,snake_head)
    for tick in range(40):
     #   for tick in itertools.count():
    
        tr_defglobal.pixels = []

  #      if tr_defglobal.debug: print "Tick: %d" % tick

        for index in pixpatt[start]:
   #         if tr_defglobal.debug: print "index: %d" % index
            if  tr_defglobal.type_switch: break             # break from main Loop

            snake_pos = snake_head - index
            hue = 0
            saturation = 0
            value = 0
            if snake_pos >= 0 and snake_pos < snake_length:
                hue = (5.0/6.0) * snake_pos / snake_length
                saturation = 1
                value = 1
            r, g, b = map(lambda x:color_utils.remap(x,0.0,1.0,0,255), colorsys.hsv_to_rgb(hue, saturation, value))
    #        tr_defglobal.pixels.append((r, g, b)) 
            tr_defglobal.pixels.append( color_function.bright(tr_defglobal.brightness,((r, g, b)))) 
    #        if tr_defglobal.debug: print "outputting"

            tr_defglobal.client.put_pixels(tr_defglobal.pixels)
        time.sleep(float(1) / tr_defglobal.frameps)
        snake_head += 1
        if snake_head + snake_length > anzpixel:
            snake_head = 0
     #   time.sleep(0.5)

#----- snake1
def main():
    global snake_length, snake_head, hue
    tr_defglobal.pattern=9

    if tr_defglobal.debug: print "doing work9"
    numLEDs = len(tr_defglobal.coordinates)

    while True:

        if  tr_defglobal.do_term: break             # break from main Loop
        if  tr_defglobal.type_switch: break             # break from main Loop
                   # function color_wheel signals termination             
  
        for z in range(3):
            if  tr_defglobal.type_switch: break             # break from main Loop
 #   for tick in itertools.count():
            tr_defglobal.pixels = []
            tr_defglobal.client.put_pixels(tr_defglobal.pixels)

            for r in range(3):
                if  tr_defglobal.type_switch: break             # break from main Loop
                snake_head=snake_head_i[z]

                snake(z)

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
