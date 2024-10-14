import flet as ft
from message import Message

class ClientGUI:
    def __init__(self, connect_event, send_event, disconnect_event, refresh_event, logger):
        self.logger = logger
        
        self.connect_event = connect_event
        self.send_event = send_event
        self.disconnect_event = disconnect_event
        self.refresh_event = refresh_event

        self.users = [ft.Text(value="User1")]
        self.messages = [
            ft.Column([ft.Text(value="User1"), ft.Text(value="message")])
            ]
        self.servername=ft.Text(value="Server1")
        self.tsend = ft.TextField(label="Enter message", hint_text="Type here...")
        self.tip = ft.TextField(label="Enter Server IP", hint_text="192.168.0.0")
        self.tport = ft.TextField(label="Enter Server port", hint_text="8001")
        self.tname = ft.TextField(label="Enter your name", hint_text="John Smith")

    def addMessage(self, msg):
        self.messages.append(ft.Column([ft.Text(value=msg.senderName), ft.Text(value=msg.text)]))
        self.page.update()

    def setMessages(self, msgs):
        self.messages.clear()
        for m in msgs:
            self.messages.append(ft.Column([ft.Text(value=m.senderName), ft.Text(value=m.text)]))
        self.page.update()

    def addUser(self, user):
        self.users.append(ft.Text(value=user))
        self.page.update()

    def removeUser(self, user):
        self.users.remove(user)
        self.page.update()

    def setUsers(self, users):
        self.users.clear()
        for u in users:
            self.users.append(ft.Text(value=u))
        self.page.update()

    def setServerName(self, name):
        self.servername.value = name
        self.page.update()
    

    def getIP(self):
        return self.tip.value
    
    def getPort(self):
        return self.tport.value
    
    def getName(self):
        return self.tname.value
    
    def getMsg(self):
        return self.tsend.value
    
    def render_(self, page: ft.Page):
        self.page=page
        page.title = "Chat App"
        
        bconnect = ft.ElevatedButton(text="Connect", on_click=self.connect_event)
        ccol=ft.Column(
            [ft.Row([
                self.tip,
                self.tport,
                bconnect
            ]), 
            self.tname]
        )
        cconnect = ft.Container(content = ccol, bgcolor="#BDB1A2", margin=0, padding=20, border=ft.border.all(1, "#000000"))
        
        
        bsend = ft.ElevatedButton(text="Send", on_click=self.send_event)
        bdisconnect=ft.ElevatedButton(text="Disconnect", on_click=self.disconnect_event)
        brefresh=ft.ElevatedButton(text="Refresh", on_click=self.refresh_event)
        
        
        cchat=ft.Container(content = ft.Row([
            ft.Column([self.servername, ft.Column(self.messages), ft.Row([self.tsend, bsend])]), 
            ft.Column([ft.Column(self.users), bdisconnect, brefresh])
            ]), bgcolor="#BDB1A2", margin=0, padding=20, border=ft.border.all(1, "#000000"))

        page.add(cconnect, cchat)


    def run(self):
        ft.app(self.render_)

