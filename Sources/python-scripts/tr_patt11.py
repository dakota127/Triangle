
#Import all modules
#from __future__ import division
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

import  time,sys

numLed=25


black_white = [(0, 0, 0), (2, 2, 2)]
rgb_bright = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
red_pixels = [(1, 0, 0)] * numLed
green_pixels = [(0, 1, 0)] * numLed
blue_pixels = [(0, 0, 1)] * numLed
arrays = [red_pixels, green_pixels, blue_pixels]
frame = 0
start_time, start_frame = time.time(), frame



#----- speedest
def main():
    global arrays
    frame = 0
    start_time, start_frame = time.time(), frame

    tr_defglobal.pattern=11
    if tr_defglobal.debug: print "doing work11"
    start_time = time.time()

    while True:

        if  tr_defglobal.do_term: break             # break from main Loop
        if  tr_defglobal.type_switch: break             # break from main Loop
                   # function color_wheel signals termination             

        for pixels, bright in zip(arrays, rgb_bright):
            dim = pixels[0]
            for i in range(tr_defglobal.anzled):
                pixels[i] = bright
      #          pixels[0] = black_white[(frame % 10)/5]
       #         pixels[1] = black_white[(frame % 100)/50]
        #        pixels[2] = black_white[(frame % 1000)/500]
                tr_defglobal.client.put_pixels(pixels)
                pixels[i] = dim
                frame += 1
                if frame % 100 == 0:
                    now = time.time()
                    if now - start_time >= 1.0:
                        fps = (frame - start_frame) / (now - start_time)
                        sys.stdout.write('%7.1f fps\r' % fps)
                        sys.stdout.flush()
                        start_time, start_frame = now, frame
            pixels[0] = pixels[1] = pixels[2] = dim
 

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
