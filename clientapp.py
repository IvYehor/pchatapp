from clientgui import ClientGUI
from clientside import *
from clientsocket import SocketClient
from message import Message
from clientmock import MockClient


class ClientApp:
    def __init__(self, client):
        self.client = client
        self.gui = ClientGUI(self.on_connect, self.on_send, self.on_disconnect, self.on_refresh)

    def on_connect(self, e):
        s = self.client.Connect(self.gui.getIP(), int(self.gui.getPort()), self.gui.getName())
        if s[0]:
            self.gui.setServerName(s[1])
            self.gui.setMessages(s[2])
            self.gui.setUsers(s[3])

    def on_send(self, e):
        m = self.client.SendMessage(self.gui.getMsg())
        self.gui.addMessage(m)

    def on_refresh(self, e):
        s = self.client.Refresh()
        if s[0]:
            self.gui.setServerName(s[1])
            self.gui.setMessages(s[2])
            self.gui.setUsers(s[3])
        else:
            self.gui.setServerName("")
            self.gui.setMessages([])
            self.gui.setUsers([])

    def on_disconnect(self, e):
        self.client.Disconnect()
        self.gui.setServerName("")
        self.gui.setMessages([])
        self.gui.setUsers([])
    def run(self):
        self.gui.run()

c = ClientApp(SocketClient())
c.run()
