import socket
import threading
import json

from message import Message

from clientside import Client

s = socket.socket()
s.settimeout(10)
s.connect(("localhost", 8005))
s.settimeout(None)

print(s.recv(8))
s.close()