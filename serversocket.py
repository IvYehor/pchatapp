import socket
import threading
import queue
import json
import logging
import serversocketinterface

class ServerSocket(serversocketinterface.ServerSocketInt):
    def __init__(self, l):
        self.socket = None
        self.clients = {}
        self.l = l

    def isSocketNone(self):
        return self.socket is None

    def Start(self, address, port):
        self.socket = socket.socket()
        try:
            self.socket.bind((address, port))
        except socket.error:
            self.logger.error("Couldn't bind to " + str(("0.0.0.0", self.port)))
            return None
        self.socket.listen()
        return True

    def Close(self):
        self.socket.close()
        self.socket = None
        return True

    def Accept(self):
        return self.socket.accept()

    def AddClient(self, addr, conn, name, thread):
        self.clients[addr] = ClientData(conn, name, thread)

    def CloseClient(self, addr):
        #the thread should be ended separately
        self.clients[addr].conn.close()
        self.clients.pop(addr)

    def Send(self, addr, msg):
        if self.clients[addr] is None:
            return None
        try:
            self.clients[addr].conn.send(msg)
        except socket.error:
            return None
        return True
    
    def Recv(self, addr, howmuch):
        if self.clients[addr] is None:
            return None
        
        try:
            msg = self.clients[addr].conn.recv(howmuch).decode("utf-8")
        except socket.error:
            return None
        
        if not msg:
            return None
        else:
            return msg

    def RecvCL(self, client, howmuch):
        if client is None:
            return None
        msg = client.recv(howmuch).decode("utf-8")
        
        if not msg:
            return None
        else:
            return msg
    
    def getClientNames(self):
        return list([cl.name for addr, cl in self.clients.items()])
    def getClientName(self, addr):
        return self.clients[addr].name
    def getClientThread(self, addr):
        return self.clients[addr].thread
    

class ClientData:
    def __init__(self, conn, name, thread):
        self.conn = conn
        self.name = name
        self.thread = thread
