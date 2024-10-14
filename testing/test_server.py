import pytest
from unittest.mock import MagicMock
from serverapp import *
from mockserversocket import *

class Logger:
    def __init__(self):
        self.msgs = []
    def info(self, msg):
        self.msgs.append(msg)
    def error(self, msg):
        self.msgs.append(msg)




def test_start1():
    ss = MagicMock()
    ss.Accept.return_value = 'fff'

    l = Logger()
    serv = SocketServer(l, ss)
    serv.AcceptClient()
    assert l.msgs == ["Couldn't recieve client name"]



def test_start2():
    
    l = Logger()
    serv = SocketServer(l, MockServerSocket(recvclresult=[1, "Bob"], sendresult=[True]))
    serv.AcceptClient()
    assert l.msgs == ['New user: client address 1 Bob', 'Sending to new user: ["Chat room 1", [], ["Bob", "Alice"]]']




def test_requests1():
    l = Logger()
    serv = SocketServer(l, MockServerSocket(sendresult=[True], recvresult=[None]))
    
    assert serv.ClientProcessRequests("addr") is None
    assert l.msgs == ['Client addr closed']

def test_requests2():
    l = Logger()
    serv = SocketServer(l, MockServerSocket(sendresult=[True], recvresult=[6, "refresh"]))
    
    assert serv.ClientProcessRequests("addr") == True
    assert l.msgs == []

def test_requests3():
    l = Logger()
    ss = MagicMock()
    #ss.Recv.return_value = [7, "message", 10, "Hi there!"]
    ss.Recv.side_effect = []
    serv = SocketServer(l, MockServerSocket(sendresult=[True], recvresult=[7, "message", 10, "Hi there!"]))
    
    assert serv.messages
    assert serv.ClientProcessRequests("addr") is True
    ss.Recv.assert_called_once_with()
    assert l.msgs == ['New message from user Bob: Hi there!']

def test_requests4():
    l = Logger()
    serv = SocketServer(l, MockServerSocket(sendresult=[True], recvresult=[12, "wrongrequest"]))
    
    assert serv.ClientProcessRequests("addr") is True
    assert l.msgs == []