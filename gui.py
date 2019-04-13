import urllib.request
import socket
import wx
from wxasync import AsyncBind, WxAsyncApp, StartCoroutine
import asyncio
from asyncio.events import get_event_loop

# Flags here
launchSuccess = False

#class PyssConverse :
    
    # MOVE EVERYTHING TO PYSSMAIN


class PyssMain(wx.Frame):

    username = None
    PORT = None
    IP = None
    HOST = '127.0.0.1'

    def __init__(self):
        super().__init__(parent=None, title='Pyssenger')
        
        panelMain = wx.Panel(self)

        stIPInfo = wx.StaticText(panelMain, label="Your external IP is: ", pos=(5,10))
        stIP = wx.TextCtrl(panelMain, value=PyssMain.IP, pos=(125, 5), style=wx.TE_READONLY)

        self.txtConversation = wx.TextCtrl(panelMain, value="test", pos=(5, 50), size=(350, 80), style=wx.TE_MULTILINE|wx.TE_READONLY)

        self.txtInputMessage = wx.TextCtrl(panelMain, value="moar", pos=(5, 135), style=wx.TE_PROCESS_ENTER)
        btnSendMsg = wx.Button(panelMain, label='Send', pos=(200, 135))

        btnSendMsg.Bind(wx.EVT_BUTTON, self.on_press)
        self.txtInputMessage.Bind(wx.EVT_TEXT_ENTER, self.on_press)
        self.Show()
        StartCoroutine(self.runHost, self)
        
        
    #    asyncio.run(self.parallelRun())


    #async def parallelRun(self):
    #    await asyncio.gather(self.showGUI(), self.runHost())


    #async def showGUI(self):

    
    async def on_press(self, event):
            if self.txtInputMessage.GetValue():
                self.txtConversation.AppendText("\n" + self.txtInputMessage.GetValue())
                self.txtInputMessage.SetValue("")
    

    """async def runHost(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.HOST, self.PORT))
            s.listen()
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr)
                while True:
                    data = conn.recv(1024)
                    if not data:
                        #break SLEEP
                        await asyncio.sleep(2)
                    else:
                        self.txtConversation.AppendText("\n" + repr(data))
                    #conn.sendall(data)"""


    
    async def read_server(self, reader, writer):
        while True:
            data = await reader.read(100)  # Max number of bytes to read
            if not data:
                await asyncio.sleep(1)
                break
            else:
                self.txtConversation.AppendText("\nFriend:   " + str(data, "utf-8"))
        #writer.write(data)
        #await writer.drain()  # Flow control, see later
    #writer.close()

    #async def main(host, port):
    #    server = await asyncio.start_server(read_server, host, port)
    #    await server.serve_forever()
    #asyncio.run(main('127.0.0.1', 5000))

    async def runHost(self):
        server = await asyncio.start_server(self.read_server, self.HOST, self.PORT)
        await server.serve_forever()






class PyssLaunch(wx.Frame):

    def __init__(self):
        super().__init__(parent=None, title='Pyssenger')
        panelMain = wx.Panel(self)

        # Other initialization
        try:
            #PyssMain.IP = urllib.request.urlopen('https://ident.me').read().decode('utf8')
            PyssMain.IP = '127.0.0.1'
            socket.inet_aton(PyssMain.IP)
        except:
            wx.MessageBox('Could not determine external IP. Your computer is not connected to the Internet or the remote server is unreachable.', 'Connectivity Error', wx.OK | wx.ICON_EXCLAMATION)
            PyssMain.IP = 'undefined'
            exit()
        #except Exception as x:
        #except socket.error:
            


        stUsername = wx.StaticText(panelMain, label="Enter your username:", pos=(5,10))
        # IDEA: add an array of fancy usernames and select each time a random to present as default
        self.txtInputUsername = wx.TextCtrl(panelMain, value="LeeroyJenkins", pos=(125, 5))

        stPort = wx.StaticText(panelMain, label="Port to connect:", pos=(5,40))
        self.txtInputPort = wx.TextCtrl(panelMain, value="2410", pos=(125, 35))

        btnHostRun = wx.Button(panelMain, label='Run Server', pos=(55, 75))

        # Event binding here
        btnHostRun.Bind(wx.EVT_BUTTON, self.on_press)

        self.Show()


    def on_press(self, event):
        global launchSuccess
        PyssMain.username = self.txtInputUsername.GetValue()
        PyssMain.PORT     = int(self.txtInputPort.GetValue())
        if not PyssMain.username or not PyssMain.PORT:
            print("Both fields are required in order to initiate connection!")
        else:
            self.Destroy()
            launchSuccess = True



if __name__ == '__main__':
    app0 = wx.App()
    frame = PyssLaunch()
    app0.MainLoop()
    if launchSuccess:
        app = WxAsyncApp()
        frame = PyssMain()
        loop = get_event_loop()
        loop.run_until_complete(app.MainLoop())
    #print(PyssMain.username, PyssMain.port, PyssMain.IP)
