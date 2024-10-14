import socket
import threading
import queue
import json
import logging
from serversocketinterface import ServerSocketInt

class MockServerSocket(ServerSocketInt):
    def __init__(self, recvclresult=[True], sendresult=[True], recvresult=[True]):
        self.recvclresult = recvclresult
        self.sendresult = sendresult
        self.recvresult = recvresult
        self.recvci = 0
        self.sendi = 0
        self.recvi = 0

    def isSocketNone(self):
        return None
        # or None

    def Start(self, address, port):
        return True
        # or None

    def Close(self):
        return True

    def Accept(self):
        return ("connection", "client address 1")

    def AddClient(self, addr, conn, name, thread):
        pass

    def CloseClient(self, addr):
        pass

    def Send(self, addr, msg):
        r = self.sendresult[self.sendi]
        self.sendi+=1
        self.sendi%=len(self.sendresult)
        return r
        # or None
    
    def Recv(self, addr, howmuch):
        r = self.recvresult[self.recvi]
        self.recvi+=1
        self.recvi%=len(self.recvresult)
        return r
        # message or None

    def RecvCL(self, client, howmuch):
        r = self.recvclresult[self.recvci]
        self.recvci+=1
        self.recvci%=len(self.recvclresult)
        return r
        # message or None
    
    def getClientNames(self):
        return ("Bob", "Alice")
    def getClientName(self, addr):
        return "Bob"
    def getClientThread(self, addr):
        return threading.Thread(target=lambda arg:None, args=(None,))
    

