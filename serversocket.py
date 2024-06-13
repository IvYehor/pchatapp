import socket
import threading
import queue
import json
import logging

class ServerSocket:
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
            return 1
        self.socket.listen()
        return 0

    def Close(self):
        self.socket.close()
        self.socket = None

    def Accept():
        return self.socket.accept()

    def AddClient(self, addr, conn, name, thread):
        self.clients[addr] = Client(conn, name, thread)

    def CloseClient(self, addr):
        #the thread should be ended separately
        self.clients[addr].conn.close()
        self.clients.pop(addr)

    def Send(self, addr):
        if self.clients[addr] is None:
            return 1
        self

class ClientData:
    def __init__(self, conn, name, thread):
        self.conn = conn
        self.name = name
        self.thread = thread
