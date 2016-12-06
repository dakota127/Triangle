#!/usr/bin/python
# coding: utf-8
#-------------------------------------------------------
#  Global Variables für Triangle --------------------
#------------------------------------------------------
#
debug=0                 # 0= no debug output, 1= debug output
debugg=0                # Big debug, more details
charplate=1             # use charplate with 1
appname=" "             # application name (script)
do_term=0               # term signal in mainloop
lcd=0
msg_line=list()         # lines to be displayed 16x2 Char 
msg_line_old=""
msg_name="Triangle"
type_switch=0

#--------------------------------------------
# Definitions for GPIO Pins Triangle
PIN_RFA=12      # IN 32
PIN_RFB=25      # IN 22  
PIN_RFC=16      # IN 36
PIN_RFD=23      # IN 16
PIN_PULS=05     # IN 29
PIN_SEL2=04      # IN 07 DIP Switch 2
PIN_SEL3=17     # IN 11 DIP Switch 3
PIN_SEL4=27     # IN 13 DIP Switch 4
PIN_BUZ=18      # OUT 12 Buzzer
PIN_PUSH=7      # IN 26 auf triangle Board  (durch iswitchpi Python bei start verwendet, sonst frei
# Deckplatte
PIN_PB1=26      # IN 37 with R, Kabel 5
PIN_SEL1=22     # IN 15 with R, Kabel 4
PIN_PGM1=19     # IN 35 with R, Kabel 2
PIN_PGM2=13     # IN 33 with R, Kabel 3
PIN_LED1=21     # OUT 40 Led, Kabel 7

# used in iswitchpi
#PINFROMTOPI=20
#------------------------------------------
# Kabel 1 ext. Led from iSwitchPi
# Kabel 8 Pushbutton from iSwitchPi
# Kabel 9 GND
#------------------------------------------

BLACK=1                 # return from button_pressed
REDSHORT=2              # return from button_pressed
REDLONG=3               # return from button_pressed
SETUP=4                 # return from button_pressed
but={1:'Black', 2:'Red-short', 3:'Red-long', 4:'Setup'}
brightness_default=100          # max 100
brightness=brightness_default
brightness_old=brightness
brightness_change=0 # going down
frameps=20
frameps_old=frameps
frameps_change=0  # going down
pattern=0                       
pattern_old=pattern
entf=0
light=100           
entf_old=entf
entf_watch=""
prog_run=1
check_enf=1             # check proximity sensor
waitbutton_1 = 0.8      # wait time in sec for button
iteration_pattern=1     # iteration counter for drawPatt functions
pattern_type=0      # what sort of pattern to do after start
anzled = 25
strip=0
BLACKCOL=[0,0,0]            # Black Color
WHITECOL=[255,255,255]      # white color
REDCOL=[255,0,0]      # white color

BOTTOM=-1                   # constants
TOP=-1
UP=1
DOWN=0
FULL=-2
UPDOWN={1:'UP', 0:'DOWN'}

brightrange=[20,40,60,80,100]
set_led_parm=[0,0,BLACKCOL,100]
set_led_parm_black=[0,0,BLACKCOL,100]
pixels = [ (0,0,0) ] * anzled
random_values = float(0) * anzled

gamma  = 2                  # gamma correction
gamma_a = bytearray(256)
g_maxin =   255.0           # max values
g_maxout  = 255.0

anz_type=5                  # number of mainloops
killfile="tr_killed.txt"    # killfile name
debugfile =""
type_description={1:'Images', 2:'Pattern 1',  3:'Pattern 2', 4:'Text', 5:'Undef'}
images_found={0:'Local', 1:'USB'}
savecollist=list()          # list of pixels to light up
coordinates =list()
lednumber =list()
neighbors=list()
ledgroup=list()
triacorner=list()
cornergroup=([],[],[])
client=0
start_time=0
ircounter=0
last_time=0
spibus=0
twinkle=0
shiftcol=0
tol=100     # tolerance für Entfernung
display_time=0
ticks_display=0
ticks_display_max=10
ticks=0 # interrupt counter
exitapp=False


#Config-Variables (read from configfile tr_config.ini)
startpattern=15
displaytime=60
brightness=100
brightness_default=100
speed=100
colorset=1


configval = [
    "filename",'/home/pi/triangle/tr_config.ini',
    "abschnitt", 'triangle',
    "startpattern",'15', 
    "displaytime",'60', 
    "brightness", '100',
    "speed",'100',
    "colorset", '1'
    ]



pixpatt = [
            [ # unten nach oben
            0,1,2,3,4,5,6,7,8,     \
            9,10,11,12,13,14,15,    \
            16,17,18,19,20,         \
            21,22,23,               \
            24                      \
            ],
            [   # links nach rechts
            0,1,15,14,16,17,23,22,24,  \
            2,3,13,12,18,19,21,    \
            4,5,11,10,20,         \
            6,7,9,               \
            8                      \
            ],
            [  # rechts nach links
            8,7,9,10,20,19,21,22,24,   \
            6,5,11,12,18,17,23,    \
            4,3,13,14,16,         \
            2,1,15,               \
            0                      
            ]
    ]
# -------------------------------------------------------------------