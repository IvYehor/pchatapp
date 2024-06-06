from clientgui import ClientGUI
from clientside import *
from clientsocket import SocketClient
from message import Message
from clientmock import MockClient
import logging

class ClientApp:
    def __init__(self, client, logger):
        self.client = client
        self.gui = ClientGUI(self.on_connect, self.on_send, self.on_disconnect, self.on_refresh, logger)
        self.logger = logger

    def on_connect(self, e):
        try:
            port = int(self.gui.getPort())
        except ValueError:
            return
        s = self.client.Connect(self.gui.getIP(), port, self.gui.getName())
        if s[0]:
            self.gui.setServerName(s[1])
            self.gui.setMessages(s[2])
            self.gui.setUsers(s[3])

    def on_send(self, e):
        m = self.client.SendMessage(self.gui.getMsg())
        if m is None:
            return
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


if __name__ == "__main__":
    l = logging.getLogger()
    l.setLevel(logging.DEBUG)

    fh = logging.FileHandler('clientapp.log')
    sh = logging.StreamHandler()

    formatter = logging.Formatter('In %(funcName)s line %(lineno)d at %(asctime)s: %(message)s')

    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    sh.setLevel(logging.ERROR)
    sh.setFormatter(formatter)

    l.addHandler(fh)
    l.addHandler(sh)

    c = ClientApp(SocketClient(l), l)
    c.run()
