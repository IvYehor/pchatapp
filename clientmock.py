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