#!/usr/bin/python
# coding: utf-8
# ***********************************************************
# 	Test Programm Triangle
#   shows designates GPIO Pins and Number of Timer Interupts
#   to check out soldering of Interface boards
# 	Designed and written by Peter K. Boxler, November 2015  
#***********************************************************
#
import RPi.GPIO as GPIO
from time import sleep
import sys,os
import spidev


import tr_defglobal


long=0.5

ir_a=0
ir_b=0
ir_c=0
ir_d=0
pb_1=0
pgm_1=0
pgm_2=0
sel_1=0
sel_2=0
sel_3=0
sel_4=0
sel_5=0

IR={12:'A', 13:'B',16:'C', 19:'D'}
ircounter=0

var=1
 
 # Callback --------------------------------------------------
def my_callback_timer(channel):
    global ircounter
    ircounter+=1

def setup_GPIO():
#   SETUP General Input/Output-Pins of Raspberry    
    GPIO.setmode(GPIO.BCM) 
    GPIO.setwarnings(False)


#   SETUP General Input/Output-Pins of Raspberry    
    GPIO.setmode(GPIO.BCM) 
    GPIO.setwarnings(False)
    GPIO.setup(tr_defglobal.PIN_PUSH, GPIO.IN, pull_up_down=GPIO.PUD_UP)   # type switch 
    GPIO.setup(tr_defglobal.PIN_RFA, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)         # RF A 
    GPIO.setup(tr_defglobal.PIN_RFB, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)         # RF B 
    GPIO.setup(tr_defglobal.PIN_RFC, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)         # RF C 
    GPIO.setup(tr_defglobal.PIN_RFD, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)         # RF D 
    GPIO.setup(tr_defglobal.PIN_PULS, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)           # n555 Interrupt pin 
    GPIO.add_event_detect(tr_defglobal.PIN_PULS, GPIO.FALLING, callback=my_callback_timer, bouncetime=300)

# setup Input Pins first - with pull down

# dip switch pins
    GPIO.setup(tr_defglobal.PIN_SEL2, GPIO.IN, pull_up_down=GPIO.PUD_UP)         # RF A 
    GPIO.setup(tr_defglobal.PIN_SEL3, GPIO.IN, pull_up_down=GPIO.PUD_UP)         # RF B 
    GPIO.setup(tr_defglobal.PIN_SEL4, GPIO.IN, pull_up_down=GPIO.PUD_UP)         # RF C 
# Input with external resistors
    GPIO.setup(tr_defglobal.PIN_PB1, GPIO.IN)
    GPIO.setup(tr_defglobal.PIN_SEL1, GPIO.IN)
    GPIO.setup(tr_defglobal.PIN_PGM1, GPIO.IN) 
    GPIO.setup(tr_defglobal.PIN_PGM2, GPIO.IN) 

# output Pins
    GPIO.setup(tr_defglobal.PIN_LED1, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(tr_defglobal.PIN_BUZ, GPIO.OUT, initial=GPIO.LOW)



def gpio_cleanup():
    GPIO.output(tr_defglobal.PIN_BUZ,GPIO.LOW)
    GPIO.output(tr_defglobal.PIN_LED1,GPIO.LOW)
    print "doing GPIO cleanup"
    GPIO.cleanup(tr_defglobal.PIN_RFA)         # type switch 
    GPIO.cleanup(tr_defglobal.PIN_RFB)         # type switch 
    GPIO.cleanup(tr_defglobal.PIN_RFC)         # type switch 
    GPIO.cleanup(tr_defglobal.PIN_RFD)         # type switch 
    GPIO.cleanup(tr_defglobal.PIN_LED1)
    GPIO.cleanup(tr_defglobal.PIN_PUSH)         # type switch 
    GPIO.cleanup(tr_defglobal.PIN_BUZ)         # buzzer  
    GPIO.cleanup(tr_defglobal.PIN_SEL1)         # type switch 
    GPIO.cleanup(tr_defglobal.PIN_PB1)         # type switch 
    GPIO.cleanup(tr_defglobal.PIN_PULS)

def get_adc(channel):
    if ((channel > 1) or (channel < 0)):
        return -1

    r = spi.xfer2([1,(2+channel)<<6,0])
    ret = ((r[1]&31) << 6) + (r[2] >> 2)
    return ret


def beep():
    GPIO.output(tr_defglobal.PIN_BUZ,GPIO.HIGH)
    sleep(0.2)
    GPIO.output(tr_defglobal.PIN_BUZ,GPIO.LOW)

def blink():
    GPIO.output(tr_defglobal.PIN_LED1,GPIO.HIGH)
    sleep(0.1)
    GPIO.output(tr_defglobal.PIN_LED1,GPIO.LOW)
    sleep(0.1)

#-------
# program starts here
#---------------------------

if __name__ == '__main__':
    sleep(0.1)
    appname=os.path.basename(__file__)
    pfad=os.path.dirname(os.path.realpath(__file__))    # pfad wo dieses script läuft
    setup_GPIO()
    i=0
    wert0=0
    wert1=0
    volts_0=0
    volts_1=0
    # setup ad Wandler
    spi = spidev.SpiDev()
    spi.open(0,0)
    title= "Pb1  Pb2  Pgm1  Pgm2  Sel1  Sel3  Sel4  Sel5  IRa  IRb  IRc  IRd  Timer  Entfern    Lumen"
    print title


# posit: do it as long not Ctlr-C 
    try:    
        while True:
            blink()
            if wert0 > 500:
                beep()
            i+=1 
            ir_b=GPIO.input(tr_defglobal.PIN_RFB)      
            ir_a=GPIO.input(tr_defglobal.PIN_RFA)       # high if NOT pressed !
            ir_b=GPIO.input(tr_defglobal.PIN_RFB)
            ir_c=GPIO.input(tr_defglobal.PIN_RFC)
            ir_d=GPIO.input(tr_defglobal.PIN_RFD)
            sel_1=GPIO.input(tr_defglobal.PIN_SEL1)
            sel_3=GPIO.input(tr_defglobal.PIN_SEL2)
            sel_4=GPIO.input(tr_defglobal.PIN_SEL3)
            sel_5=GPIO.input(tr_defglobal.PIN_SEL4)
            pb_1=GPIO.input(tr_defglobal.PIN_PB1)
            pb_2=GPIO.input(tr_defglobal.PIN_PUSH)

            pgm_1=GPIO.input(tr_defglobal.PIN_PGM1)
            pgm_2=GPIO.input(tr_defglobal.PIN_PGM2)
            sleep(0.3)
            if i>10:
                print title
                i=0
            line1= " " + '{:<1}'.format(pb_1)  + '{:>5}'.format(pb_2) +'{:>5}'.format(pgm_1) + '{:>6}'.format(pgm_2) +'{:>6}'.format(sel_1)  \
                + '{:>6}'.format(sel_3) + '{:>6}'.format(sel_4) + '{:>6}'.format(sel_5)    \
                + '{:>6}'.format(ir_d) + '{:>5}'.format(ir_c) + '{:>5}'.format(ir_b) + '{:>5}'.format(ir_a) + '{:>6}'.format(ircounter) \
                + '{:>6}'.format(wert0) + '{:>5}'.format(volts_0)  + '{:>6}'.format(wert1) + '{:>5}'.format(volts_1)
            print line1

            wert = get_adc(0)
            wert2 = get_adc(0)
            wert3 = get_adc(0)

            wert=(wert+wert2+wert3)/3
            if wert != wert0:
                wert0=wert
                volts_0 = round((wert * 3.33) / float(1024), 2)

       #     print "read:", wert, volts_0
                wert0 = wert
            
        # read Helligkeit    
            wert = get_adc(1)
            if wert != wert1:
                wert1=wert
                volts_1 = round((wert * 3.33) / float(1024), 2)


    except KeyboardInterrupt:
        pass
    # cleanup
        print "\nKeyboard Interrupt in %s" % appname
        
    finally:            # kommt nach dem Signalhandler noch hierher !!!
        print "\nFinally reached in %s" % appname

        gpio_cleanup()





    sys.exit(2)
    
    
    


          
            