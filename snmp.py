#!/usr/bin/python
from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.proto import rfc1902
import time

def addimage(target,user,host,appnumber):
    setCommand(target, 'TYPE=BR;BUTTON=SCAN;USER="'+ user +'";FUNC=IMAGE;HOST=' + host + ';APPNUM=' + appnumber  + ';DURATION=360;BRID=;')

def addemail(target,user,host,appnumber):
    setCommand(target, 'TYPE=BR;BUTTON=SCAN;USER="'+ user +'";FUNC=EMAIL;HOST=' + host + ';APPNUM=' + appnumber  + ';DURATION=360;BRID=;')

def addfile(target,user,host,appnumber):
    setCommand(target, 'TYPE=BR;BUTTON=SCAN;USER="'+ user +'";FUNC=FILE;HOST=' + host + ';APPNUM=' + appnumber  + ';DURATION=360;BRID=;')



def setCommand(target,cmd):
  cmdGen = cmdgen.CommandGenerator()

  errorIndication, errorStatus, errorIndex, varBinds = cmdGen.setCmd(
    cmdgen.CommunityData('internal', mpModel=0),
    cmdgen.UdpTransportTarget((target, 161)),
    ('1.3.6.1.4.1.2435.2.3.9.2.11.1.1.0', rfc1902.OctetString(cmd))
 )

  # Check for errors and print out results
  if errorIndication:
      print(errorIndication)
  else:
    if errorStatus:
        print('%s at %s' % (
            errorStatus.prettyPrint(),
            errorIndex and varBinds[int(errorIndex)-1] or '?'
            )
        )

def launch(conf):
  while(1):
    #print('snmp broadcast')
    for option in conf["menu"]["option"]:
      if (option["type"].lower()=="email"):
        addemail(conf["printerip"],option["name"],conf["ip"] + ':54924','1')
      elif (option["type"].lower()=="file"):
        addfile(conf["printerip"],option["name"],conf["ip"] + ':54924','1')
      elif (option["type"].lower()=="image"):
        addimage(conf["printerip"],option["name"],conf["ip"] + ':54924','1')
    
    time.sleep(100)
