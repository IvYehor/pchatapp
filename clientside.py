import message

class Server:
    def __init__(self):
        self.socket = 0

class Client:
    def __init__(self):
        self.server = Server()
        pass

    # A method to connect to a server
    # Starts a recieve thread
    def Connect(self):
        pass

    # A method to send a message to a server
    def SendMessage(self):
        pass

    # A thread for the meassages of other users
    # Calls ReceivedDisconnect, RecievedClose, RecivedMessage
    def RecieveThread(self):
        pass

    # A method for a special "disconnect" message from server to indicate that some user disconnected
    def ReceivedDisconnect(self):
        pass

    # A method for a special "closed" message from server to indicate that the server closed
    # Calls Disconnect
    def RecievedClose(self):
        pass

    # A method for a messages
    def RecivedMessage(self):
        pass

    # A method to disconnect
    # Ends all the threads
    def Disconnect(self):
        pass