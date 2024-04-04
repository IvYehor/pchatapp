import message

class Server:
    def __init__(self):
        self.clients = []

    # Starts client accept thread
    def Start(self):
        pass

    # Accepts client connections and starts separate client threads
    def AcceptClientthread(self):
        pass

    # Receives messages from clients, sends the messages to all the other clients, calls RecivedMessage and RecievedDisconnect
    def ClientThread(self):
        pass

    # Called when client send a messages
    # Server sends the message to all the other clients
    def RecivedMessage(self):
        pass

    # Called when client sends a special "disconnect" message to a server when it wants to disconnect
    # Server sends a special message to all the other clients that this client disconnected
    def RecievedDisconnect(self):
        pass

    # Sends a special message to client that means that the server closed
    # Stops all the threads
    def Stop(self):
        pass

class Client:
    def __init__(self):
        self.socket = 0
