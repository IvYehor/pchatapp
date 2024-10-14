import socket
import threading
import json
import logging

import protocol

from message import Message

from clientside import Client

class SocketClient(Client):
    def __init__(self, logger):
        super().__init__()
        self.socket = None
        self.name = ""
        self.logger = logger

    def Recv_(self):
        if self.socket is None:
            self.logger.error("Socket is None")
            return None
        
        try:
            header = self.socket.recv(8).decode('utf-8')
        except socket.timeout:
            self.logger.error("Header recieve timout")
            return None
        except socket.error:
            self.logger.error("Header recieve other socket error")
            return None
        except Exception:
            self.logger.error("Header recieve other error")
            return None
        
        if not header:
            self.logger.error("Lost connection (recieved nothing in header)")
            return None
        
        try:
            datastr = self.socket.recv(int(header)).decode("utf-8")
        except socket.timeout as e:
            self.logger.error("Data recieve timeout", exc_info=e)
            return None
        except socket.error:
            self.logger.error("Data recieve other socket error")
            return None
        except Exception:
            self.logger.error("Data recieve other error")
            return None
        
        if not datastr:
            self.logger.error("Lost connection (recieved nothing in data)")
            return None
        
        return datastr
    
    def Send_(self, msg):
        if self.socket is None:
            self.logger.error("Socket is None")
            return 1
        
        try:
            self.socket.send(protocol.get_header(msg))
        except socket.timeout:
            self.logger.error("Header send timeout")
            self.Disconnect()
            return 1
        except socket.error:
            self.logger.error("Header send other socket error")
            self.Disconnect()
            return 1
        except Exception:
            self.logger.error("Header send other socket error")
            self.Disconnect()
            return 1
        
        try:
            self.socket.send(msg.encode("utf-8"))
        except socket.timeout:
            self.logger.error("Header send timeout")
            self.Disconnect()
            return 1
        except socket.error:
            self.logger.error("Header send other socket error")
            self.Disconnect()
            return 1
        except Exception:
            self.logger.error("Header send other error")
            self.Disconnect()
            return 1
        
        return 0

    def Connect(self, ip, port, name):
        self.logger.info("Connecting...")

        if self.socket is not None:
            self.logger.error("Already connected")
            return (False,)
        
        try:
            self.socket = socket.socket()
        except socket.error:
            self.logger.error("Couldn't create scoket object (socket error)")
            return (False,)
        except Exception:
            self.logger.error("Couldn't create scoket object (other error)")
            return (False,)
        
        self.socket.settimeout(10)
        try:
            self.socket.connect((ip, port))
        except socket.error:
            self.logger.error("Couldn't connect")
            self.socket.close()
            return (False,)
        except Exception:
            self.logger.error("Couldn't connect")
            return (False,)
        self.socket.settimeout(None)


        if self.Send_(name):
            self.logger.error("Couldn't send name")
            return (False,)
        self.name = str(name)

        r = self.Recv_()
        if r is None:
            return (False,)
        try:
            data = json.loads(r)
        except json.JSONDecodeError:
            self.logger.error("Couldn't parse json")
            return (False,)
        except Exception:
            self.logger.error("Couldn't parse json (other error)")
            return (False,)

        return True, data[0], (Message(msg[0], msg[1], msg[2]) for msg in data[1]), data[2]

    def SendMessage(self, msg):
        self.logger.info("Sending message...")

        if self.Send_("message"):
            self.logger.error("Couldn't send request")
            return None
        
        if self.Send_(msg):
            self.logger.error("Couldn't send message")
            return None
        
        return Message(self.name, msg, (1,1,1))
    
    def Refresh(self):
        self.logger.info("Refreshing...")
        
        if self.Send_("refresh"):
            self.logger.error("Couldn't send request")
            return (False,)
        
        r = self.Recv_()
        if r is None:
            self.logger.error("Couldn't recieve data")
            return (False,)
        try:
            data = json.loads(r)
        except Exception:
            self.logger.error("Json parse error")
            return (False,)
        
        if data is None:
            self.logger.error("Json data is None")
            self.Disconnect()
            return (False,)
        
        self.logger.info("Recieved")
        self.logger.debug(data)
        
        return True, data[0], (Message(msg[0], msg[1], msg[2]) for msg in data[1]), data[2]

    def Disconnect(self):
        self.logger.error("Disconnecting...")
        try:
            self.socket.close()
        except socket.error:
            self.logger.error("Socket close error")
        except Exception:
            self.logger.error("Socket close other error")
        finally:
            self.socket = None
        
