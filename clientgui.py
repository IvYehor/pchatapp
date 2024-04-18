import flet as ft

class ClientGUI:
    def __init__(self, connect_event, send_event, disconnect_event):
        self.connect_event = connect_event
        self.send_event = send_event
        self.disconnect_event = disconnect_event

    def render_(self, page: ft.Page):
        page.title = "Chat App"
        tip = ft.TextField(label="Enter Server IP", hint_text="192.168.0.0")
        tname = ft.TextField(label="Enter your name", hint_text="John Smith")
        bconnect = ft.ElevatedButton(text="Connect", on_click=self.connect_event)
        ccol=ft.Column(
            [ft.Row([
                tip,
                bconnect
            ]), 
            tname]
        )
        cconnect = ft.Container(content = ccol, bgcolor="#BDB1A2", margin=0, padding=20, border=ft.border.all(1, "#000000"))
        
        tsend = ft.TextField(label="Enter message", hint_text="Type here...")
        bsend = ft.ElevatedButton(text="Send", on_click=self.send_event)
        bdisconnect=ft.ElevatedButton(text="Disconnect", on_click=self.disconnect_event)
        cchat=ft.Container(content = ft.Row([
            ft.Column([ft.Text(), ft.Row([tsend, bsend])]), 
            ft.Column([ft.Text(), bdisconnect])
            ]), bgcolor="#BDB1A2", margin=0, padding=20, border=ft.border.all(1, "#000000"))

        page.add(cconnect, cchat)


    def run(self):
        ft.app(self.render_)

def a(e):
    pass
def b(e):
    pass
def c(e):
    pass

c = ClientGUI(a, b, c)
c.run()
