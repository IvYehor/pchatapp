from clientgui import ClientGUI
from clientside import *
from message import Message

class MockClient(Client):
    def __init__(self):
        super().__init__()
    
    def Connect(self, ip):
        print("Connecting to server " + ip + "...")
        return True, "Server ABC", (Message("User1", "message1", (1,1,1)), Message("User2", "Message 2", (1,2,3))), ("User1", "User2")

    def SendMessage(self, msg):
        print("Sending message...")
        return Message("User1", msg, (1,1,1))
    
    def Refresh(self):
        return True, "Server ABC", (Message("User1", "message1", (1,1,1)), Message("User2", "Message 2", (1,2,3))), ("User1", "User2")
    def RecieveThread(self):
        pass

    def ReceivedDisconnect(self):
        pass

    def RecievedClose(self):
        pass

    def RecivedMessage(self):
        pass

    def Disconnect(self):
        print("Disconnecting")

class ClientApp:
    def __init__(self, client):
        self.client = client
        self.gui = ClientGUI(self.on_connect, self.on_send, self.on_disconnect, self.on_refresh)

    def on_connect(self, e):
        s = self.client.Connect(self.gui.getIP())
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

    def on_disconnect(self, e):
        self.client.Disconnect()
        self.gui.setServerName("")
        self.gui.setMessages([])
        self.gui.setUsers([])
    def run(self):
        self.gui.run()

c = ClientApp(MockClient())
c.run()
