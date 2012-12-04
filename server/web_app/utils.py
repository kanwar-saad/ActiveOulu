import Queue
import threading
import time
import socket, select
import sys
from datetime import datetime, timedelta

HOST = '127.0.0.1'
PORT = 5555

def connect_to_pmb():
    try:
      sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error, msg:
      #sys.stderr.write("[ERROR] %s\n" % msg[1])
      return -1
     
    try:
      sock.connect((HOST, PORT))
    except socket.error, msg:
      #sys.stderr.write("[ERROR] %s\n" % msg[1])
      return -1

    sock.setblocking(0)
    return sock

def tx_msg_to_pmb(sock, msg):

    if (sock == -1):
        return ''
    inputready, outputready,exceptrdy = select.select([], [sock],[sock], 60)
   
    if len(exceptrdy):
        #print "exception in sending data"
        return ''
    elif len(outputready):
        #send data 
        try:
            sock.send(msg)
        except socket.error, msg:
            return ''
 
    now = datetime.now()
    retStr = ''
    while ((datetime.now() - now).seconds < 5) and (retStr == ''):
        if (sock == -1):
            return ''
        inputready, outputready,exceptrdy = select.select([sock], [],[sock], 60)
       
        if len(exceptrdy):
            #print "exception in receiving data"  
            break
        elif len(inputready):
            #recv data 
            try:
                retStr = sock.recv(1024)
            except socket.error, msg:
                return ''

    if retStr == '':
        return ''
    else:
        return retStr

class TxThread(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.setDaemon(True)
    
    def run(self):
        sock = connect_to_pmb()
        while (sock == -1) :
            sock = connect_to_pmb()

        while True:
            #grabs host from queue
            msg = self.queue.get()
    
            #process message here
            #print "Sending Message = ", msg, " ", self.getName()
            retry = 0
            
            ret = tx_msg_to_pmb(sock, msg)
            while (ret == '') and (retry < 5): 
                
                print "Error in Rx/Tx from/to pmb ... connecting again" 
                retry = retry + 1
                #sock.close()
                sock = connect_to_pmb()
                connect_retry = 0
                while (sock == -1) and (connect_retry <= 5):
                    connect_retry = connect_retry + 1
                    sock = connect_to_pmb()
                ret = tx_msg_to_pmb(sock, msg)
                
            if ret:
                print "return Message = ", ret
            else:
                print "Retries exceeded: Discarding message" 
            #signals to queue job is done
            self.queue.task_done()

class static_class:
    queue = Queue.Queue()
    tx_thread = TxThread(queue) 
 

#Fill Queue for socket thread to send message to PMB 
def tx_msg_to_worker(msg):
    # If thread is not there then create it
    s = static_class()
    if not s.tx_thread.isAlive():
        print s.tx_thread
        s.tx_thread.start()
        time.sleep(1)
        #print "Starting Socket Thread"
    
    #Fill Queue
    print "Buffer Queue Size = ", s.queue.qsize()
    s.queue.put(msg) 


