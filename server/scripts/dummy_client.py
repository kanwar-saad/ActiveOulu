#!/usr/bin/env python
 
 
import socket, select
import sys
from datetime import *

HOST = '127.0.0.1'
PORT = 5555
 
try:
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error, msg:
  sys.stderr.write("[ERROR] %s\n" % msg[1])
  sys.exit(1)
 
try:
  sock.connect((HOST, PORT))
except socket.error, msg:
  sys.stderr.write("[ERROR] %s\n" % msg[1])
  sys.exit(2)

sock.setblocking(0)


while (1):

    msg = raw_input("Message to server : ")
    inputready, outputready,exceptrdy = select.select([], [sock],[sock], 60)
   
    if len(exceptrdy):
        print "exception in sending data"
        break
    elif len(outputready):
        #send data 
        sock.send(msg)
 
    now = datetime.now()
    retStr = ''
    while ((datetime.now() - now).seconds < 5) and (retStr == ''):
        inputready, outputready,exceptrdy = select.select([sock], [],[sock], 60)
       
        if len(exceptrdy):
            print "exception in receiving data"  
            break
        elif len(inputready):
            #recv data 
            retStr = sock.recv(1024)
            print "inside recv loop"
    

    if retStr == '':
        print "error in receiving data"
    else:
        print "return Value = ", retStr



sock.close()
sys.exit(0)
