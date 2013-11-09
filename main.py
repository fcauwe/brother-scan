#!/usr/bin/env python

# (C) 2013 Francois Cauwe


#Global libs
import sys, time, threading
import subprocess
import Queue

#Private libs
import listen
import snmp
import XmlDict

conf=dict()

def load_config():
#    logger.info("Loading Config...")
    global conf
    conf=XmlDict.loadXml("global.xml")

def launch_snmp():
#    logger.info("Snmp service...")
    global conf
    snmp.launch(conf)

def launch_listen():
#    logger.info("Loading Listening service...")
    global conf
    listen.launch(conf)



 
def main():
    #logging.config.fileConfig("config/logger.conf")
    #global logger
    #logger=logging.getLogger("main")
  
    # Loading global configuration
    load_config()
  
    # Start Snmp
    snmpThread = threading.Thread(target=launch_snmp)
    snmpThread.start()

    # Start Snmp
    listenThread = threading.Thread(target=launch_listen)
    listenThread.start()



    # Wait for closing
    snmpThread.join()
    listenThread.join()

if __name__ == '__main__':
    main()

