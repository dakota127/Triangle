#!/usr/bin/python
# coding: utf-8
#----------------------------------------------------------
#
#   Test Programm für bxp_charout
#
#----------------------------------------------------------

from time import sleep, strftime
from datetime import datetime

import bxp_defglobal
from bxp_charout import *
import os, sys
debug=0
counter=0
# *************************************************
# Program starts here, let's roll
# *************************************************

if __name__ == '__main__':

    bxp_defglobal.appname=os.path.basename(__file__)
#
    bxp_defglobal.lcd_attached=1
    ret=charout_init()
    if ret>0:
        print "No testing, no display found"
        sys.exit(2)
    bxp_defglobal.msg_line.append ("CharOut Testing")
    
    bxp_defglobal.msg_line.append ("                ")
    charout_write (bxp_defglobal.msg_line[0],debug)
    sleep(2)
    while True:
        try:
            counter+=1
            bxp_defglobal.lcd.clear()
            ipaddr = run_cmd(cmd)
 #           ipaddr2 ="IP " + '{:<10s}'.format(ipaddr)
            ipaddr2=ipaddr[0:12] 
            
            bxp_defglobal.msg_line=datetime.now().strftime('%b %d  %H:%M:%S\n') + "\n" + '%s' % (ipaddr2)
            charout_write (bxp_defglobal.msg_line,debug)
        #    print "zeile: ", bxp_defglobal.msg_line
       #     bxp_defglobal.lcd.message(datetime.now().strftime('%b %d  %H:%M:%S\n'))
       #     bxp_defglobal.lcd.message('IP %s' % (ipaddr))
            if counter > 5:
                bxp_defglobal.lcd.backlight(False)
                sleep(1)
                bxp_defglobal.lcd.clear()
                sleep(0.1)
                bxp_defglobal.lcd.backlight(True)
                copunter=0

            sleep(1)
        except KeyboardInterrupt:
    # aufräumem
            charout_off()
            sys.exit(0)     #  Abschlussvearbeitung

