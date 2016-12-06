#!/usr/bin/python
# coding: utf-8
#----------------------------------------------------------
#   Test Read a config file
#------------------------------------------------------


import os, sys

from ConfigParser import SafeConfigParser

#-------------------------------------------------
#   function to read configfile
#   all parameters are passen in directory values
#   entries filename and section are removed later
#   so only config-entry key remain
#-------------------------------------------------
def configread(values,debug):
    found=0
    options=list()
    retvalues=list()
    if debug:
        print
        print "Function: configread"
        print "configread:values-1: ",values   
        for z in range(0,(len(values)-1),2):
            print values[z],values[z+1]
            
    filename=values[1]
    section=values[3]
    values.pop(0)
    values.pop(0)
    values.pop(0)
    values.pop(0)


    if debug:
        print "configread:values-2: ",values    
        print "configread:section: ", section
    parser = SafeConfigParser()
    parser.read(filename)

  
    if parser.has_section(section):
        if debug:
            print "configread:configfile ok"  
        pass 
    else:
        if debug:
            print "configread:configfile not ok, no section %s found" % section  

        return(9)
#    for name, value in parser.items("test"):
    for i in range(0,(len(values)-1),2):

        if parser.has_option(section, values[i]):
            if debug:
                print parser.get(section,values[i])
            retvalues.append(values[i])
            retvalues.append(parser.get(section,values[i]))
        else:
            retvalues.append(values[i])
            retvalues.append(values[i+1])
    if debug:
        print "configread:retvalues: ", retvalues
        print "Function: configread ending"

    return(retvalues)

# *************************************************
# Program starts here, let's roll
# *************************************************

if __name__ == '__main__':
    debug=1
    url=""
    username=""
    password="" 
    abc=""    
    appname=""
    dirname=""
  
    configval=[
      "filename",'config.ini',
        "abschnitt", 'test',
        "url",'defaulturl', 
        "username",'usernamedefault', 
        "password", 'passworddefault',
        "abc",'default'
        ]

        
    
    appname=os.path.basename(__file__)
    dirname = os.path.dirname(os.path.abspath( __file__ ))
    print (dirname + '/'+ appname)
    
    print configval
    
    ret=configread(configval,debug)
    print "from configfile: " 
    for z in range(0,(len(ret)-1),2):
        if debug:
            print ret[z], ret[z+1]
        if ret[z]=="url": url=ret[z+1]
        if ret[z]=="username": username=ret[z+1]
        if ret[z]=="password": password=ret[z+1]
        if ret[z]=="abc": abc=ret[z+1]

        
    print "url: %s username: %s password: %s, abc %s" % (url, username, password,abc)
    
    
    