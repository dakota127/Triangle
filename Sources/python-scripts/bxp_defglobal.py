#!/usr/bin/python
# coding: utf-8
#-------------------------------------------------------
#  Global Variables für Triangle --------------------
#------------------------------------------------------
#
debug=0                 # 0= no debug output, 1= debug output
debugg=0                # Big debug, more details
lcd_attached=1             # use charplate with 1
appname=" "             # application name (script)
do_term=0               # term signal in mainloop
lcd=0
msg_line=list()         # lines to be displayed 16x2 Char 
msg_line_old=""
msg_name="Triangle"
BLACKCOL=[0,0,0]            # Black Color
WHITECOL=[255,255,255]      # white color
REDCOL=[255,0,0]      # white color

killfile="tr_killed.txt"    # killfile name
debugfile =""
start_time=0
