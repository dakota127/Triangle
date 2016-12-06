#!/usr/bin/env python
# coding: utf-8
#

#Import all modules
from __future__ import division
import sys
import time
import math

import tr_defglobal
from tr_sub import *
import color_utils
import color_function

numLed=25
#pixels = [ (0,0,0) ] * numLed
start_time=0



#----- raver_plaid
def main():
    global pixels, start_time
    fps = 20         # frames per second

# how many sine wave cycles are squeezed into our n_pixels
# 24 happens to create nice diagonal stripes on the wall layout
    freq_r = 20
    freq_g = 20
    freq_b = 20

# how many seconds the color sine waves take to shift through a complete cycle
    speed_r = 7
    speed_g = -13
    speed_b = 19
    count=0
    tr_defglobal.pattern=14
    if tr_defglobal.debug: print "doing work14"
    start_time = time.time()

    while True:
        if  tr_defglobal.do_term: break             # break from main Loop
        if  tr_defglobal.type_switch: break             # break from main Loop 
        t = time.time() - start_time

        tr_defglobal.pixels = []
   #     print "len0", len(tr_defglobal.pixels)
        count+=1
        for ii in range(25):
            pct = ii / 25
        # diagonal black stripes
            pct_jittered = (pct * 77) % 37
            blackstripes = color_utils.cos(pct_jittered, offset=t*0.05, period=1, minn=-1.5, maxx=1.5)
            blackstripes_offset = color_utils.cos(t, offset=0.9, period=60, minn=-0.5, maxx=3)
            blackstripes = color_utils.clamp(blackstripes + blackstripes_offset, 0, 1)
        # 3 sine waves for r, g, b which are out of sync with each other
            r = blackstripes * color_utils.remap(math.cos((t/speed_r + pct*freq_r)*math.pi*2), -1, 1, 0, 256)
            g = blackstripes * color_utils.remap(math.cos((t/speed_g + pct*freq_g)*math.pi*2), -1, 1, 0, 256)
            b = blackstripes * color_utils.remap(math.cos((t/speed_b + pct*freq_b)*math.pi*2), -1, 1, 0, 256)

            tr_defglobal.pixels.append(color_function.bright(tr_defglobal.brightness,(r, g, b)))
            
         #   tr_defglobal.pixels.append((r, g, b))
        tr_defglobal.client.put_pixels(tr_defglobal.pixels)
        time.sleep(float(0.1) / tr_defglobal.frameps)
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
