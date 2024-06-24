import logging.config
import socket
import threading
import queue
import json
from message import Message
import time
import logging
import os

import protocol

from serverside import *
from serversocket import *
from serversocketinterface import ServerSocketInt

# error return None
# no error return anything else

class SocketServer(Server):
    def __init__(self, logger, server_sock : ServerSocketInt):
        super().__init__()
        # socket, name
        self.messages = []
        
        self.taskqueue = queue.Queue()
        self.messagequeue = queue.Queue()
        
        self.server_sock = server_sock
        self.socketMutex = threading.Lock()
        
        self.servname = "Chat room 1"
        self.port = 8001
        
        self.logger = logger
    
    # Starts client accept thread
    def Start(self):
        self.uithread = threading.Thread(target=self.UI)
        self.uithread.start()
        self.processthread = threading.Thread(target=self.ProcessCommands)
        self.processthread.start()
        self.uithread.join()
        self.processthread.join()
        
    def log(self, msg):
        self.logger.info(msg)
        self.messagequeue.put(msg)

    def UI(self):
        while True:
            inp = input("What to do:")
            if inp in ["start", "close"]:
                print("Queuing:" + inp)
                self.taskqueue.put(inp)
            elif inp == "print":
                print("is msgs empty: " + str(self.messagequeue.empty()))
                while not self.messagequeue.empty():
                    print(self.messagequeue.get())
            elif inp == "setname":
                self.servname = input("New name:")
            elif inp == "setport":
                self.port = int(input("New port:"))
            elif inp == "exit":
                os._exit(1)
            else:
                print("No such command")

    def Send_(self, addr, msg):
        if self.server_sock.isSocketNone():
            return None
        if self.server_sock.Send(addr, protocol.get_header(msg)) is None:
            return None
        if self.server_sock.Send(addr, msg.encode("utf-8")) is None:
            return None
        return True
    
    def Recv_(self, addr):
        header = self.server_sock.Recv(addr, 8)
        if header is None:
            return None
        return self.server_sock.Recv(addr, int(header))

    def ProcessCommands(self):
        while True:
            cmd = self.taskqueue.get(block=True)
            if cmd == "start":
                with self.socketMutex:
                    if not self.server_sock.Start("0.0.0.0", self.port):
                        self.log("Could not start at 0.0.0.0:" + str(self.port) + " " + self.servname)
                        continue
                
                self.log("Starting at 0.0.0.0:" + str(self.port) + " " + self.servname)

                self.acceptthread = threading.Thread(target=self.AcceptClientthread)
                self.acceptthread.start()

            elif cmd == "close":
                self.server_sock.Close()
    

    # Accepts client connections and starts separate client threads
    def AcceptClientthread(self):
        self.log("started accepting, socket")
        while True:
            self.AcceptClient()
            
    
    def AcceptClient(self):
        (conn, addr) = self.server_sock.Accept()
 
        h = self.server_sock.RecvCL(conn, 8)
        if h is None:
            self.log("Couldn't recieve client name")
            return 
        
        clname = self.server_sock.RecvCL(conn, int(h))
        if clname is None:
            self.log("Couldn't recieve client name")
            return 

        self.server_sock.AddClient(addr, conn, clname, threading.Thread(target=self.ClientThread, args=(addr,)))

        data = self.servname, self.messages, self.server_sock.getClientNames()
        jdata = json.dumps(data)
        
        
        if self.Send_(addr, jdata) is None:
            self.logger.error("Couldn't send data to client")
            self.server_sock.CloseClient(addr)        
            return

        self.log("New user: " + str(addr) + " " + clname)
        self.log("Sending to new user: " + str(jdata))

        self.server_sock.getClientThread(addr).start()

    # Receives messages from clients, sends the messages to all the other clients, calls RecivedMessage and RecievedDisconnect
    def ClientThread(self, addr):
        while True:
            if self.ClientProcessRequests(addr) is None:
                return

    def ClientProcessRequests(self, addr):
        req = self.Recv_(addr)
        
        if req is None:
            self.server_sock.CloseClient(addr)
            self.log("Client " + str(addr) + " closed")
            return None
        if req == 'refresh':
            data = self.servname, self.messages, self.server_sock.getClientNames()
            jdata = json.dumps(data)
            self.Send_(addr, jdata)
        elif req == 'message':
            msg = self.Recv_(addr)
            if msg is None:
                self.server_sock.CloseClient(addr)
                self.log("Client " + str(addr) + " closed")
                return None
            self.messages.append((self.server_sock.getClientName(addr), msg, (1,1,1)))
            self.log("New message from user " + self.server_sock.getClientName(addr) + ": " + msg)
        else:
            self.server_sock.CloseClient(addr)
            self.log("Invalid response from client")
            self.log("Client " + str(addr) + " closed")
            return None
        return True

if __name__ == "__main__":
    l = logging.getLogger()
    l.setLevel(logging.DEBUG)

    fh = logging.FileHandler('serverapp.log')

    formatter = logging.Formatter('In %(threadName)s, %(funcName)s line %(lineno)d at %(asctime)s: %(message)s')

    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)

    l.addHandler(fh)

    serv = SocketServer(l, ServerSocket(l))
    serv.Start()
