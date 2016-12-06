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


# color function

def pixel_color(t, coord, ii, n_pixels):
    """Compute the color of a given pixel.

    t: time in seconds since the program started.
    ii: which pixel this is, starting at 0
    coord: the (x, y, z) position of the pixel as a tuple
    n_pixels: the total number of pixels

    Returns an (r, g, b) tuple in the range 0-255

    """
    # make moving stripes for x, y, and z
    x, y, z = coord
    r = color_utils.cos(x, offset=t / 4, period=1, minn=0, maxx=0.7)
    g = color_utils.cos(y, offset=t / 4, period=1, minn=0, maxx=0.7)
    b = color_utils.cos(z, offset=t / 4, period=1, minn=0, maxx=0.7)
    r, g, b = color_utils.contrast((r, g, b), 0.5, 2)

    # make a moving white dot showing the order of the pixels in the layout file
    spark_ii = (t*80) % n_pixels
    spark_rad = 8
    spark_val = max(0, (spark_rad - color_utils.mod_dist(ii, spark_ii, n_pixels)) / spark_rad)
    spark_val = min(1, spark_val*2)
    r += spark_val
    g += spark_val
    b += spark_val

    # apply gamma curve
    # only do this on live leds, not in the simulator
    #r, g, b = color_utils.gamma((r, g, b), 2.2)

    return (r*256, g*256, b*256)


#----- spatial_stripes

def main():
    tr_defglobal.pattern=5
    if tr_defglobal.debug: print "doing work5"
    n_pixels = len(tr_defglobal.coordinates)
    start_time = time.time()
    while True:
        if  tr_defglobal.do_term: break             # break from main Loop
        if  tr_defglobal.type_switch: break             # break from main Loop


        t = time.time() - start_time
        tr_defglobal.pixels = [color_function.bright(tr_defglobal.brightness,pixel_color(t, coord, ii, n_pixels)) for ii, coord in enumerate(tr_defglobal.coordinates)]

 #       tr_defglobal.pixels = [pixel_color(t, coord, ii, n_pixels) for ii, coord in enumerate(tr_defglobal.coordinates)]
        tr_defglobal.client.put_pixels(tr_defglobal.pixels)
        time.sleep(float(8) / tr_defglobal.frameps)

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
