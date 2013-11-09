#!/usr/bin/python

from socket import *
import sys,os
import select
from subprocess import call


def launch(conf):
  address = ('',54925)
  server_socket = socket(AF_INET, SOCK_DGRAM)
  server_socket.bind(address)
  print "Listening"

  while(1):
    recv_data, addr = server_socket.recvfrom(2048)
    #print recv_data
    response_array = recv_data.split(";")
    user = response_array[2].split("=")[1].replace('\"','')
    function = response_array[3].split("=")[1]
    print "Event recieved: scan " + function + " for " + user
    for option in conf["menu"]["option"]:
      if ((option["type"].lower()==function.lower()) and (option["name"]==user)):
        print "Starting " + option["script"]
        call([os.path.dirname(os.path.realpath(__file__)) + os.sep + option["script"], option["type"], option["name"], option["config"]])    

    recv_data, addr = server_socket.recvfrom(2048)

