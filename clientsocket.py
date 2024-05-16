import socket
import threading
import json

import protocol

from message import Message

from clientside import Client

class SocketClient(Client):
    def __init__(self):
        super().__init__()
        self.socket = None
        self.name = ""

    def Recv_(self):
        if self.socket is None:
            return None
        header = self.socket.recv(8).decode('utf-8')
        if not header:
            return None
        datastr = self.socket.recv(int(header)).decode("utf-8")
        if not datastr:
            return None
        return datastr
    
    def Send_(self, msg):
        if self.socket is None:
            return 1
        self.socket.send(protocol.get_header(msg))
        self.socket.send(msg.encode("utf-8"))
        return 0

    def Connect(self, ip, port, name):
        self.socket = socket.socket()

        self.socket.settimeout(10)
        err = self.socket.connect_ex((ip, port))
        self.socket.settimeout(None)

        if err:
            return (False)

        self.Send_(name)
        self.name = str(name)

        data = json.loads(self.Recv_())
        print(data)


        return True, data[0], (Message(msg[0], msg[1], msg[2]) for msg in data[1]), data[2]

    def SendMessage(self, msg):
        print("Sending message...")
        if self.Send_("message"):
            return None
        if self.Send_(msg):
            return None
        return Message(self.name, msg, (1,1,1))
    
    def Refresh(self):
        if self.Send_("refresh"):
            self.Disconnect()
            return (False)
        data = json.loads(self.Recv_())
        if data is None:
            self.Disconnect()
            return (False)
        
        print("Recieved")
        print(data)
        
        return True, data[0], (Message(msg[0], msg[1], msg[2]) for msg in data[1]), data[2]

    def Disconnect(self):
        self.socket.close()
        self.socket = None
        print("Disconnecting")
