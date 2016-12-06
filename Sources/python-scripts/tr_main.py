#!/usr/bin/python
# coding: utf-8
#----------------------------------------------------------
#
#   Triangle Main Program
#
#   Drives the 25 Led Triangle
#
#   Based on Micah Scott's  16 Led triangle and several Python scripts that
#   came with it.
#   
#   This version by Peter K. Boxler 2015. 
#
#   User-Interface :
#       Adafruit CharPlate 16x2 several pushbuttons und toggle-switches
#       
# sudo python tr_main.py -l ../layouts/triangle25.json -o 0
#-----------------------------------------------------------
#
#Import all modules
import sys, getopt, os
from time import sleep
import time, datetime
# COMMENT
import RPi.GPIO as GPIO
from threading import Thread
# ENDCOMMENT

import struct
from threading import Thread
from random import randint
import random
import tr_defglobal
import bxp_defglobal
from bxp_charout import *
from bxp_configfile import configread

from tr_sub import *
import signal
import platform
import opc                  # from Master-openpixelcontrol
#                           https://github.com/zestyping/openpixelcontrol
#                           https://github.com/mens-amplio/opc-client-framework/
from math import *
import optparse
try:
    import json
except ImportError:
    import simplejson as json
import color_utils
import color_function
import spidev

# including pattern subprograms
import tr_patt01
import tr_patt02
import tr_patt03
import tr_patt04
import tr_patt05
import tr_patt06
import tr_patt07
import tr_patt08
import tr_patt09
import tr_patt10
import tr_patt11
import tr_patt12
import tr_patt13
import tr_patt14
import tr_patt15
anzpatt=15

# Configurable values
image_folder_usb = "/media/usb1/images"          # path to pictures on usb stick
image_folder = "images"          # path to pictures local
pfad=" "
fullname=" "            	             	
onoff={1:'ON', 0:'OFF'}

#                                                           2: from text input


bxp_defglobal.msg_line.append ("Triangle - Init")
bxp_defglobal.msg_line.append ("                ")


color =[
    [156, 145, 100],
    [10, 255, 40],
    [10,120, 170]
]


# ------ Function Definitions -----------------------------
#
#----------------------------------------------------------
# get and parse commandline args
def argu():
    parser = optparse.OptionParser()
    parser.add_option('-l', '--layout', dest='layout',
                    action='store', type='string',
                    help='layout file')
    parser.add_option('-s', '--server', dest='server', default='127.0.0.1:7890',
                    action='store', type='string',
                    help='ip and port of server')
    parser.add_option('-f', '--fps', dest='fps', default=20,
                    action='store', type='int',
                    help='frames per second')

    parser.add_option('-d', '--dbg', dest='debug', default=0,
                    action='store', type='int',
                    help='debug')
    parser.add_option('-o', '--out', dest='charplat', default=1,
                    action='store', type='int',
                    help='charplate')

    options, args = parser.parse_args()
    tr_defglobal.charplate=options.charplat
    tr_defglobal.debug=options.debug
    if not options.layout:
        parser.print_help()
        print
        print 'ERROR: you must specify a layout file using --layout'
        print
        sys.exit(1)
    return(options)


#-- Function to handle kill Signal ---------------------
def sigterm_handler(signum = None, frame=None):
    tr_defglobal.d.write(msg="Signal received" '{:>4}'.format(signum) )
    # Raises SystemExit(0):
    if tr_defglobal.debug: print "Signal received " , signum 
    killit=open(tr_defglobal.killfile,"w")  # write killfile, so we know this was done
    killit.close()
    if tr_defglobal.debug: print "Exiting in Signalhandler.. " , signum 
    sys.exit(0)
#----------------------------------------------------------

#------- Funktion get values from configfile
#----------------------------------------------------------
def getconfig(values):
    if tr_defglobal.debug:
        print "Configvalues: ", values
    
    ret=configread(values,tr_defglobal.debug)
    if ret==9:
        return(ret)

    if tr_defglobal.debug:
        print "from configfile: " 
        for z in range(0,(len(ret)-1),2):
            print ret[z], ret[z+1]
            
    tr_defglobal.startpattern=int(ret[1])
    tr_defglobal.displaytime=int(ret[3])
    tr_defglobal.brightness=int(ret[5])
    tr_defglobal.brightness_default=tr_defglobal.brightness
    tr_defglobal.speed=int(ret[7])
    tr_defglobal.colorset=int(ret[9])
    
    if tr_defglobal.debug:
        print "From Configfile: startpattern: %s displaytime: %s brightness: %s speed: %s colorset %s" %   \
        (tr_defglobal.startpattern,tr_defglobal.displaytime,tr_defglobal.brightness,tr_defglobal.speed,tr_defglobal.colorset)
    
    tr_defglobal.frameps=int((20.0/100)*tr_defglobal.speed)
    
    return()



#------- Funktion initpgm ---------------------------------
#       Initialize stuff
def initpgm():
    global pfad,fullname
    
    tr_defglobal.exitapp=False             # signals quitiing of programm

    bxp_defglobal.lcd_attached=tr_defglobal.charplate
    ret=charout_init()
    if ret>0:
        print "No LCD display found"



 #  Signal Handler aktivieren
    for sig in [signal.SIGTERM]:
        signal.signal (sig, sigterm_handler)
 
    if tr_defglobal.debug: 
        print "Signal Handler aktiviert"
    pass
    switchoff()     # all pixels off
        
#   SETUP General Input/Output-Pins of Raspberry    
    GPIO.setmode(GPIO.BCM) 
    GPIO.setwarnings(False)
    GPIO.setup(tr_defglobal.PIN_PUSH, GPIO.IN, pull_up_down=GPIO.PUD_UP)           # pushbutton an board 
    GPIO.setup(tr_defglobal.PIN_PB1, GPIO.IN, pull_up_down=GPIO.PUD_UP)           # pushbutton an front 

    GPIO.setup(tr_defglobal.PIN_RFA, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)         # RF A 
    GPIO.setup(tr_defglobal.PIN_RFB, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)         # RF B 
    GPIO.setup(tr_defglobal.PIN_RFC, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)         # RF C 
    GPIO.setup(tr_defglobal.PIN_RFD, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)         # RF D 
    GPIO.setup(tr_defglobal.PIN_PULS, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)           # n555 Interrupt pin 
    GPIO.setup(tr_defglobal.PIN_SEL2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)           # n555 Interrupt pin 
    GPIO.setup(tr_defglobal.PIN_SEL3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)           # n555 Interrupt pin 
    GPIO.setup(tr_defglobal.PIN_SEL4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)           # n555 Interrupt pin 

# output Pins
    GPIO.setup(tr_defglobal.PIN_LED1, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(tr_defglobal.PIN_BUZ, GPIO.OUT, initial=GPIO.LOW)

    GPIO.add_event_detect(tr_defglobal.PIN_PUSH, GPIO.FALLING, callback=my_callback_switch, bouncetime=300)
    GPIO.add_event_detect(tr_defglobal.PIN_PB1, GPIO.FALLING, callback=my_callback_switch, bouncetime=300)

    GPIO.add_event_detect(tr_defglobal.PIN_RFA, GPIO.RISING, callback=my_callback_rf, bouncetime=200)
    GPIO.add_event_detect(tr_defglobal.PIN_RFB, GPIO.RISING, callback=my_callback_rf, bouncetime=200)
    GPIO.add_event_detect(tr_defglobal.PIN_RFC, GPIO.RISING, callback=my_callback_rf, bouncetime=200)
    GPIO.add_event_detect(tr_defglobal.PIN_RFD, GPIO.RISING, callback=my_callback_rf, bouncetime=200)

# Clear 16x2 lcd-display and show greeting, pause 1 sec
    charout_write (bxp_defglobal.msg_line[0],tr_defglobal.debug)
    sleep(1)              # for testing
        
    if os.path.exists(tr_defglobal.killfile):         # remove killfile
        os.remove(tr_defglobal.killfile)
        if tr_defglobal.debug: print "killfile removed" 
        
    if platform.system() == 'Linux':
        tr_defglobal.debug_file = pfad + '/tr_log.log'
    elif platform.system() == 'Windows':
        tr_defglobal.debug_file = 'H:\\Daemon\\tr_log.log'
    else:
        tr_defglobal.debug_file = 'tr_log.log'
    if tr_defglobal.debug: print "debugfile ", tr_defglobal.debug_file
    tr_defglobal.d = DebugToFileClass(tag='TEST', filename=tr_defglobal.debug_file, appname=tr_defglobal.appname, overwrite=True)
#    tr_defglobal.d.write(msg='Hello World')
    tr_defglobal.random_values = [random.random() for ii in range(tr_defglobal.anzled)]

    start_time = time.time()
    a=list(enumerate(tr_defglobal.coordinates))
    if tr_defglobal.debug: 
        print "random values "
        for j in range (len(tr_defglobal.random_values)):
            print "%d   %f" % (j, tr_defglobal.random_values[j])
        print

        print "coordinates "
        for j in range (len(a)):
            print "%d   %s" % (a[j][0], a[j][1])
        print "neighbors "
        for j in range (len(tr_defglobal.neighbors)):
            print tr_defglobal.neighbors[j]
        print
        print "group "
        for j in range (len(tr_defglobal.ledgroup)):
            print tr_defglobal.ledgroup[j]
        print    
        print "corner "
        for j in range (len(tr_defglobal.triacorner)):
            print tr_defglobal.triacorner[j]
        print    
    
 #   print tr_defglobal.triacorner
    for z in range (tr_defglobal.anzled):
        corn=tr_defglobal.triacorner[z][0]
        tr_defglobal.cornergroup[corn-1].append(z)
        
 #   print "cornergroup", tr_defglobal.cornergroup
        
    tr_defglobal.start_time = time.time()
    tr_defglobal.display_time = time.time()
 #  get values from configfile   
    getconfig(tr_defglobal.configval)

    tr_defglobal.pattern_old=99   # initvalue
    
# Open SPI bus
    tr_defglobal.spibus = spidev.SpiDev()
    tr_defglobal.spibus.open(0,0)

#   check DipSwitch 2
    if not GPIO.input(tr_defglobal.PIN_SEL2):
        tr_defglobal.check_entf=0
        if tr_defglobal.debug: print "Keine Entfernung messen" 

#----------------------------------------------------------


#------- Funktion initpgm ---------------------------------
#       Initialize eventhandeler interrupt
#       do this only after init
def initpgm2():
    global pfad,fullname
#    GPIO.add_event_detect(tr_defglobal.PIN_PULS, GPIO.RISING, callback=my_callback_timer, bouncetime=1)
    return
#----------------------------------------------------------

#----------------------------------------------------------
def dirstring():        # second line of display
    if tr_defglobal.direction_flag==1:
            ab='{:^5}'.format(str(tr_defglobal.waitdraw) + tr_defglobal.direction[tr_defglobal.direction_flag])
    else:
        ab='{:^5}'.format( tr_defglobal.direction[tr_defglobal.direction_flag] + str(tr_defglobal.waitdraw) )
    return (ab)
#----------------------------------------------------------


#----------------------------------------------------------
def bright(prozent, colors):
    return (float(colors[0]*prozent/100), float(colors[1]*prozent/100), float(colors[2]*prozent/100 ))
    
#----------------------------------------------------------

def beep():
    GPIO.output(tr_defglobal.PIN_BUZ,GPIO.HIGH)
    sleep(0.2)
    GPIO.output(tr_defglobal.PIN_BUZ,GPIO.LOW)

#------------------------------------------------------
# Helligkeit messen ---------------------------------------
def get_light():
    # read value from Sharp sensor
    tr_defglobal.light=readlight()
    if tr_defglobal.debug: print "Helligkeit: ", tr_defglobal.light
    
    if tr_defglobal.light > 530:
        tr_defglobal.brightness=30
    if tr_defglobal.light > 410:
        tr_defglobal.brightness=50

    if tr_defglobal.light < 450:
        tr_defglobal.brightness=tr_defglobal.brightness_default
     
    return


#------------------------------------------------------
# entfernung messen ---------------------------------------
def get_entf():
    # read value from Sharp sensor
    tr_defglobal.entf=readentf()
    if tr_defglobal.debug: print "Entfernung: ", tr_defglobal.entf
    if (tr_defglobal.entf > tr_defglobal.entf_old+tr_defglobal.tol) or (tr_defglobal.entf < tr_defglobal.entf_old-tr_defglobal.tol):
        print "entfernung change grösser tol"
        pass
    else: tr_defglobal.entf=tr_defglobal.entf_old
 #   print tr_defglobal.entf
    
    # check distance of object
#    print tr_defglobal.entf
    if tr_defglobal.entf>350: tr_defglobal.entf_watch="--"
    if tr_defglobal.entf>500: 
        tr_defglobal.entf_watch="=="
        beep()
    if len(tr_defglobal.entf_watch)>0:
        if tr_defglobal.entf<250: tr_defglobal.entf_watch=""
        
        elif tr_defglobal.entf<350: tr_defglobal.entf_watch="--"
        
    if tr_defglobal.debug: print (tr_defglobal.pattern_type, tr_defglobal.pattern_old ,tr_defglobal.frameps, \
        tr_defglobal.frameps_old,tr_defglobal.entf,tr_defglobal.entf_old)  

    return


# Callback -------------------------------------------------
# small pushbutton on triangle board
def my_callback_switch(channel):
    if tr_defglobal.debug: print "Pin Falling: %d" % channel
    sleep(0.01)  # confirm the movement by waiting 1 sec 
    if not GPIO.input(channel): # and check again the input
        if tr_defglobal.debug: print("ok, pin %d ist tief!" % channel)
        tr_defglobal.type_switch=1
        tr_defglobal.pattern_type=tr_defglobal.pattern_type+1
        if tr_defglobal.pattern_type>anzpatt:
            tr_defglobal.pattern_type=1
#----------------------------------------------------------


 # Callback Timer Interrrupt from iswitchpi---------------------------------------
 # runs in a separate thread
def my_callback_timer(channel):
    tr_defglobal.ircounter+=1
 #   if tr_defglobal.debug:
 #       print "TimerPulse arrived......"

    t = time.time() - tr_defglobal.last_time
    tr_defglobal.last_time = time.time()
    tr_defglobal.ticks+=1           # increment interrupt counter
    tr_defglobal.ticks_display+=1   # increment interrupt counter

#   check if display needs to be switched of
#   do this after a number of ticks
    if tr_defglobal.ticks_display > tr_defglobal.ticks_display_max:  
        tr_defglobal.ticks_display=0
    # check time display is on
        t_display = time.time() - tr_defglobal.display_time
        if t_display > tr_defglobal.displaytime:
            bxp_defglobal.lcd.backlight(False)
            bxp_defglobal.msg_line[0]=""
            bxp_defglobal.msg_line[1]=""
            msg= bxp_defglobal.msg_line[0] + "\n" + bxp_defglobal.msg_line[1]
            charout_write( msg,tr_defglobal.debug)   # display ready message

    
    if (tr_defglobal.check_entf==1): 
        get_entf()    
    get_light()
# check if values have changed
    tr_defglobal.display_time = time.time()
    update_display();

    return(0)
#----------------------------------------------------------

def timertick():
    if tr_defglobal.debug: print "-->Thread timertick started..."

    GPIO.add_event_detect(tr_defglobal.PIN_PULS, GPIO.RISING, callback=my_callback_timer, bouncetime=1)


    while not tr_defglobal.exitapp:
        sleep(0.2)
 #       print "In timertick"
    
#   exitapp is True -> remove eventdetct and kill thread    
    GPIO.remove_event_detect(tr_defglobal.PIN_PULS);

    if tr_defglobal.debug: print "-->Thread timertick terminating..."
    sys.exit(0)

        
# Update Display
#-----------------------------------------------------------
def update_display():
    if (tr_defglobal.pattern_type != tr_defglobal.pattern_old) or (tr_defglobal.frameps != tr_defglobal.frameps_old) or  \
        (tr_defglobal.entf != tr_defglobal.entf_old):
        # one ore more values have changed
        tr_defglobal.pattern_old=tr_defglobal.pattern_type
        tr_defglobal.frameps_old=tr_defglobal.frameps
        tr_defglobal.entf_old=tr_defglobal.entf

        speed=(tr_defglobal.frameps/20.0) *100.0
        speed=int(speed)
        
        bxp_defglobal.lcd.backlight(True)

    # format  display lines 16x2
        bxp_defglobal.msg_line[0]='{:<9}'.format(tr_defglobal.msg_name) \
        + '{:>1d}'.format(tr_defglobal.prog_run) \
        + '{:>3d}'.format(tr_defglobal.pattern_type) \
        + '{:>3s}'.format(tr_defglobal.entf_watch) 

        bxp_defglobal.msg_line[1]='{:>3d}'.format(tr_defglobal.brightness) + "%"  \
        + '{:>4d}'.format(speed) + "%"

        
        msg= bxp_defglobal.msg_line[0] + "\n" + bxp_defglobal.msg_line[1]
        if tr_defglobal.debug: print "message: -%s %s-" % ( bxp_defglobal.msg_line[0],bxp_defglobal.msg_line[1])
        charout_write( msg,tr_defglobal.debug)   # display ready message
        bxp_defglobal.msg_line_old=bxp_defglobal.msg_line[1]
        if tr_defglobal.debug:print "Display Update Line 2"
    return();

# Callback RF-----------------------------------------------------
def my_callback_rf(channel):
    if tr_defglobal.debug: print "RF Rising : %d" % channel
    sleep(0.05)  # confirm the movement by waiting 1 sec 
    if GPIO.input(channel): # and check again the input
        if tr_defglobal.debug: print("ok, pin %d ist hoch!" % channel)
    else: return()
    
    if channel == tr_defglobal.PIN_RFD:
        if tr_defglobal.debug: print "next pattern"
    
        tr_defglobal.type_switch=1
        tr_defglobal.pattern_type=tr_defglobal.pattern_type+1
        if tr_defglobal.pattern_type>anzpatt:
            tr_defglobal.pattern_type=1

    if channel == tr_defglobal.PIN_RFC:
        if tr_defglobal.brightness_change:      # going up
            tr_defglobal.brightness += 10            
        else:
            tr_defglobal.brightness -= 10            
        
        if tr_defglobal.brightness ==10:
            tr_defglobal.brightness_change=1
        if tr_defglobal.brightness ==100:
            tr_defglobal.brightness_change=0
            
        if tr_defglobal.debug: print ("adjusting brightness to: %d" %  tr_defglobal.brightness)  

    if channel == tr_defglobal.PIN_RFA:
        if tr_defglobal.frameps_change:     # going up
            tr_defglobal.frameps += 2            
        else:
            tr_defglobal.frameps -= 2            
        
        if tr_defglobal.frameps < 3:
            tr_defglobal.frameps_change=1
        if tr_defglobal.frameps > 25:
            tr_defglobal.frameps_change=0
            
        
        if tr_defglobal.debug: print ("adjusting fps to: %d" %  tr_defglobal.frameps)  
    
    bxp_defglobal.lcd.backlight(True)   # switch on display   
    tr_defglobal.display_time = time.time()
    update_display()

#----------------------------------------------------------


#-------------------------------------------------------------------------------
# parse layout file
def parsefile(file):
    if tr_defglobal.debug: print "parsing layout file: %s" % file

    for item in json.load(open(file)):
        if 'point' in item:
            tr_defglobal.coordinates.append(tuple(item['point']))
        if 'led' in item:
            tr_defglobal.lednumber.append(item['led'])
        if 'neighbors' in item:
            tr_defglobal.neighbors.append(tuple(item['neighbors']))
        if 'group' in item:
            tr_defglobal.ledgroup.append(tuple(item['group']))
        if 'corner' in item:
            tr_defglobal.triacorner.append(item['corner'])
    

    if tr_defglobal.debug: print "lednumbers: ", tr_defglobal.lednumber

    return(0)
#----------------------------------------------------------


# ----- Function cleaup ----------------------------------------
def tr_cleanup():
    if tr_defglobal.debug: print "\Doing cleanup in %s" % tr_defglobal.appname
    tr_defglobal.d.write(msg='Cleanup started')
    switchoff()
    
    if tr_defglobal.charplate:
        bxp_defglobal.lcd.backlight(True)   # switch on display   
        charout_write ( "Terminating...",tr_defglobal.debug)   # display end
        sleep(2)
        bxp_defglobal.lcd.clear()
        bxp_defglobal.lcd.backlight(False)
    GPIO.output(tr_defglobal.PIN_BUZ,GPIO.LOW)
    GPIO.output(tr_defglobal.PIN_LED1,GPIO.LOW)

    GPIO.cleanup(tr_defglobal.PIN_PUSH)
    GPIO.cleanup(tr_defglobal.PIN_RFA)
    GPIO.cleanup(tr_defglobal.PIN_LED1)
    GPIO.cleanup(tr_defglobal.PIN_BUZ)         # buzzer  
    tr_defglobal.d.write(msg='Cleanup ended')
    return(0)
#----------------------------------------------------------


# *************************************************
# Program starts here, let's roll
# *************************************************

if __name__ == '__main__':

    tr_defglobal.appname=os.path.basename(__file__)
#
    options=argu()
    tr_defglobal.frameps=options.fps
    pfad=os.path.dirname(os.path.realpath(__file__))    # pfad wo dieses script läuft
    
    tr_defglobal.killfile =  pfad + "/" + tr_defglobal.killfile    # set correct path
    if tr_defglobal.debug: 
        print "Appname: %s" % tr_defglobal.appname
        print "Current dir: %s" % pfad
        print "Killfile: %s" % tr_defglobal.killfile
        print "FPS: ", tr_defglobal.frameps

    parsefile(options.layout)
    
    tr_defglobal.client = opc.Client('localhost:7890')
    
    # create and Start Threads
    timer_thread = Thread(target = timertick)
               
    initpgm()                   # init stuff
    tr_defglobal.last_time = time.time()
 #   print ("frameps: %d" %  tr_defglobal.frameps)  
 #   print ("brightness: %d" %   tr_defglobal.brightness)
    do_test2()
    sleep(1)
    initpgm2()                   # init stuff
    timer_thread.start()        # thread for timer pulses

#    bxp_defglobal.msg_line[0]='{:<8s}'.format(tr_defglobal.msg_name)
 #   charout_write ( bxp_defglobal.msg_line[0],tr_defglobal.debug)   # display ready message

    tr_defglobal.pattern_type=tr_defglobal.startpattern
#    

# posit: do it as long not Ctlr-C 
    try:    
        tr_defglobal.prog_run=1          # run programm 1
        while True:
            if  tr_defglobal.do_term: break             # break from main Loop
            if tr_defglobal.debug: print "Loop in Main, type %d"  % tr_defglobal.pattern_type
            if tr_defglobal.entf > 500: 
                beep()

            #
#                                       # what kind of Pattern ?
            if tr_defglobal.pattern_type==1:   
                tr_patt01.main()            # work is done in main_loop_type1()
                if tr_defglobal.debug:
                    print "Returning from work1, switch: %d, term: %d" % (tr_defglobal.type_switch,tr_defglobal.do_term)
                tr_defglobal.type_switch=0                        # return from mainloop if Ctrl-C on Keyboard
####

            if tr_defglobal.pattern_type==2:   
                tr_patt02.main()            # work is done in main_loop_type1()
                if tr_defglobal.debug:
                    print "Returning from work2, switch: %d, term: %d" % (tr_defglobal.type_switch,tr_defglobal.do_term)
                tr_defglobal.type_switch=0                        # return from mainloop if Ctrl-C on Keyboard
####
            if tr_defglobal.pattern_type==3:   
                tr_patt03.main()            # work is done in main_loop_type2()
                if tr_defglobal.debug:
                    print "Returning from work3, switch: %d, term: %d" % (tr_defglobal.type_switch,tr_defglobal.do_term)
                
                tr_defglobal.type_switch=0                       # return from mainloop if Ctrl-C on Keyboard
###
            if tr_defglobal.pattern_type==4:   
                tr_patt04.main()                 # work is done in main_loop_type2()
                if tr_defglobal.debug:
                    print "Returning from work4, switch: %d, term: %d" % (tr_defglobal.type_switch,tr_defglobal.do_term)
                
                tr_defglobal.type_switch=0                       # return from mainloop if Ctrl-C on Keyboard
###
            if tr_defglobal.pattern_type==5:   
                tr_patt05.main()                 # work is done in main_loop_type2()
                if tr_defglobal.debug:
                    print "Returning from work4, switch: %d, term: %d" % (tr_defglobal.type_switch,tr_defglobal.do_term)
                
                tr_defglobal.type_switch=0                       # return from mainloop if Ctrl-C on Keyboard
###
            if tr_defglobal.pattern_type==6:   
                tr_patt06.main()                 # work is done in main_loop_type2()
                if tr_defglobal.debug:
                    print "Returning from work4, switch: %d, term: %d" % (tr_defglobal.type_switch,tr_defglobal.do_term)
                
                tr_defglobal.type_switch=0                       # return from mainloop if Ctrl-C on Keyboard
###
            if tr_defglobal.pattern_type==7:   
                tr_patt07.main()                 # work is done in main_loop_type2()
                if tr_defglobal.debug:
                    print "Returning from work4, switch: %d, term: %d" % (tr_defglobal.type_switch,tr_defglobal.do_term)
                
                tr_defglobal.type_switch=0                       # return from mainloop if Ctrl-C on Keyboard
###
            if tr_defglobal.pattern_type==8:   
                tr_patt08.main()                 # work is done in main_loop_type2()
                if tr_defglobal.debug:
                    print "Returning from work4, switch: %d, term: %d" % (tr_defglobal.type_switch,tr_defglobal.do_term)
                
                tr_defglobal.type_switch=0                       # return from mainloop if Ctrl-C on Keyboard
###
            if tr_defglobal.pattern_type==9:   
                tr_patt09.main()                 # work is done in main_loop_type2()
                if tr_defglobal.debug:
                    print "Returning from work4, switch: %d, term: %d" % (tr_defglobal.type_switch,tr_defglobal.do_term)
                
                tr_defglobal.type_switch=0                       # return from mainloop if Ctrl-C on Keyboard

###
            if tr_defglobal.pattern_type==10:   
                tr_patt10.main()                 # work is done in main_loop_type2()
                if tr_defglobal.debug:
                    print "Returning from work4, switch: %d, term: %d" % (tr_defglobal.type_switch,tr_defglobal.do_term)
                
                tr_defglobal.type_switch=0                       # return from mainloop if Ctrl-C on Keyboard
###
            if tr_defglobal.pattern_type==11:   
                tr_patt11.main()                 # work is done in main_loop_type2()
                if tr_defglobal.debug:
                    print "Returning from work4, switch: %d, term: %d" % (tr_defglobal.type_switch,tr_defglobal.do_term)
                
                tr_defglobal.type_switch=0                       # return from mainloop if Ctrl-C on Keyboard
###
            if tr_defglobal.pattern_type==12:   
                tr_patt12.main()                 # work is done in main_loop_type2()
                if tr_defglobal.debug:
                    print "Returning from work4, switch: %d, term: %d" % (tr_defglobal.type_switch,tr_defglobal.do_term)
                
                tr_defglobal.type_switch=0                       # return from mainloop if Ctrl-C on Keyboard
###
            if tr_defglobal.pattern_type==13:   
                tr_patt13.main()                 # work is done in main_loop_type2()
                if tr_defglobal.debug:
                    print "Returning from work4, switch: %d, term: %d" % (tr_defglobal.type_switch,tr_defglobal.do_term)
                
                tr_defglobal.type_switch=0                       # return from mainloop if Ctrl-C on Keyboard
###
            if tr_defglobal.pattern_type==14:   
                tr_patt14.main()                 # work is done in main_loop_type2()
                if tr_defglobal.debug:
                    print "Returning from work4, switch: %d, term: %d" % (tr_defglobal.type_switch,tr_defglobal.do_term)
                
                tr_defglobal.type_switch=0                       # return from mainloop if Ctrl-C on Keyboard
###
            if tr_defglobal.pattern_type==15:   
                tr_patt15.main()                 # work is done in main_loop_type2()
                if tr_defglobal.debug:
                    print "Returning from work4, switch: %d, term: %d" % (tr_defglobal.type_switch,tr_defglobal.do_term)
                
                tr_defglobal.type_switch=0                       # return from mainloop if Ctrl-C on Keyboard

            sleep(1)
#
#                                       # what kind of Light Painting ?
#
    except KeyboardInterrupt:
        pass
    # cleanup
        if tr_defglobal.debug: print "\nKeyboard Interrupt in %s" % tr_defglobal.appname
        tr_defglobal.d.write(msg='Keyboard Interrupt')

        tr_defglobal.do_term=1
        switchoff()
  #      tr_cleanup()
    finally:
    # write file - so we know this part was done properly
        if tr_defglobal.debug: print "\nFinally reached in %s" % tr_defglobal.appname
        tr_defglobal.d.write(msg='Finally reached')
        tr_defglobal.exitapp=True             # signals quitiing of programm

        killit=open(tr_defglobal.killfile,"w")  # write killfile, so we know this was done
        killit.close()
        tr_cleanup()

#  Clean-Up and terminate
    exitapp = True                  # signal exit to the other threads, they will terminate themselfs 

    print "Program %s terminated...." % tr_defglobal.appname
    switchoff()

    tr_defglobal.d.write(msg='Exiting...')
    sleep(0.1)

    sys.exit(0)
    
#**************************************************************
#  That is the end
#***************************************************************
#
