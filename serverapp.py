import socket
import threading
import queue
import json
from message import Message
import time

import protocol

from serverside import *

class SocketServer(Server):
    def __init__(self):
        super().__init__()
        # socket, name
        self.clients = {}
        self.messages = []
        self.taskqueue = queue.Queue()
        self.messagequeue = queue.Queue()
        self.socket = None
        self.socketMutex = threading.Lock()
        self.servname = "Chat room 1"
        self.port = 8001

    def Send_(self, client, msg):
        if self.socket is None:
            return 1
        client.send(protocol.get_header(msg))
        client.send(msg.encode("utf-8"))
        return 0
    
    def Recv_(self, client):
        if client is None:
            return None
        header = client.recv(8).decode('utf-8')
        if not header:
            return None
        datastr = client.recv(int(header)).decode("utf-8")
        if not datastr:
            return None
        return datastr

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
            else:
                print("No such command")

    def ProcessCommands(self):
        while True:
            cmd = self.taskqueue.get(block=True)
            if cmd == "start":
                with self.socketMutex:
                    self.socket = socket.socket()
                    self.socket.bind(("0.0.0.0", self.port))
                    self.socket.listen()
                self.messagequeue.put("Starting at 0.0.0.0:" + str(self.port))
                self.acceptthread = threading.Thread(target=self.AcceptClientthread)
                self.acceptthread.start()
            elif cmd == "close":
                self.socket.close()
    # Starts client accept thread
    def Start(self):
        self.uithread = threading.Thread(target=self.UI)
        self.uithread.start()
        self.processthread = threading.Thread(target=self.ProcessCommands)
        self.processthread.start()
        self.uithread.join()
        self.processthread.join()
        

    # Accepts client connections and starts separate client threads
    def AcceptClientthread(self):
        self.messagequeue.put("started accepting, socket:" + str(self.socket))
        while True:
            #with self.socketMutex:
            #self.socket.settimeout(1)
            (conn, addr) = self.socket.accept()
            #self.socket.settimeout(None)

            clname = self.Recv_(conn)
            self.clients[addr] = (conn, clname, threading.Thread(target=self.ClientThread, args=(addr,)))

            data = self.servname, self.messages, list([cl[1] for addr, cl in self.clients.items()])
            jdata = json.dumps(data)
            self.Send_(conn, jdata)
            
            self.messagequeue.put("New user: " + str(addr) + " " + clname)
            self.messagequeue.put("Sending to new user: " + str(jdata))

            self.clients[addr][2].start()
            
    # Receives messages from clients, sends the messages to all the other clients, calls RecivedMessage and RecievedDisconnect
    def ClientThread(self, addr):
        while True:
            req = self.Recv_(self.clients[addr][0])
            if req is None:
                self.clients[addr][0].close()
                self.messagequeue.put("Client " + str(addr) + " " + self.clients[addr][1] + " closed")
                self.clients.pop(addr)
                return
            if req == 'refresh':
                data = self.servname, self.messages, list([cl[1] for addr, cl in self.clients.items()])
                jdata = json.dumps(data)
                self.Send_(self.clients[addr][0], jdata)
            elif req == 'message':
                msg = self.Recv_(self.clients[addr][0])
                self.messages.append((self.clients[addr][1], msg, (1,1,1)))
                self.messagequeue.put("New message from user " + self.clients[addr][1] + ": " + msg)



serv = SocketServer()
serv.Start()