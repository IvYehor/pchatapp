from abc import ABC, abstractmethod

class ServerSocketInt(ABC):
    
    @abstractmethod
    def isSocketNone(self):
        pass

    @abstractmethod
    def Start(self, address, port):
        pass

    @abstractmethod
    def Close(self):
        pass

    @abstractmethod
    def Accept(self):
        pass

    @abstractmethod
    def AddClient(self, addr, conn, name, thread):
        pass

    @abstractmethod
    def CloseClient(self, addr):
        pass

    @abstractmethod
    def Send(self, addr, msg):
        pass
    
    @abstractmethod
    def Recv(self, addr, howmuch):
        pass

    @abstractmethod
    def RecvCL(self, client, howmuch):
        pass

    @abstractmethod
    def getClientNames(self):
        pass

    @abstractmethod
    def getClientName(self, addr):
        pass

    @abstractmethod
    def getClientThread(self, addr):
        pass
