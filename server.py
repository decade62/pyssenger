import urllib.request
import socket
import wx
from wxasync import AsyncBind, WxAsyncApp, StartCoroutine
import asyncio
from asyncio.events import get_event_loop

# checkpoint that confirms proper transition from Launcher to Main program
launchSuccess = False


# Main program - chat interface and all necessary functions
class PyssMain(wx.Frame):

    username = None
    PORT = None
    IP = None
    HOST = '' # Empty host indicates that server listens to all IPs
    WRITEREADY = False  # Indication that write stream is ready to write
    SOCK_READER = None  # Active stream reader

    # Constructor
    def __init__(self):
        super().__init__(parent=None, title='Pyssenger')
        panelMain = wx.Panel(self)

        stIPInfo = wx.StaticText(panelMain, label="Your external IP is: ", pos=(5,10))
        stIP = wx.TextCtrl(panelMain, value=PyssMain.IP, pos=(125, 5), style=wx.TE_READONLY)

        self.txtConversation = wx.TextCtrl(panelMain, value="", pos=(5, 50), size=(350, 80), style=wx.TE_MULTILINE|wx.TE_READONLY)

        self.txtInputMessage = wx.TextCtrl(panelMain, value="Hey there!", pos=(5, 135), style=wx.TE_PROCESS_ENTER)
        btnSendMsg = wx.Button(panelMain, label='Send', pos=(200, 135))

        # Asynchronous bindings on "Send" button click and "enter" key hit - Both call on_press
        AsyncBind(wx.EVT_BUTTON, self.on_press, btnSendMsg)
        AsyncBind(wx.EVT_TEXT_ENTER, self.on_press, self.txtInputMessage)
        # Show gui
        self.Show()
        # Asynchronous coroutine running in the background while gui runs
        StartCoroutine(self.runHost, self)

        
 

    # Callback function for message submition
    async def on_press(self, event):
            if self.txtInputMessage.GetValue():
                # sets the WRITE flag True
                PyssMain.WRITEREADY = True
                # feeds the READ stream a dummy character in order to move on, to WRITE
                PyssMain.SOCK_READER.feed_data(b" ")

                
    

    # actual function that manages the READ and WRITE stream
    async def msg_server(self, reader, writer):
        # make READ stream available to all class functions
        PyssMain.SOCK_READER = reader
        while True:
            #do the writing
            if PyssMain.WRITEREADY:
                PyssMain.WRITEREADY = False #reset flag
                writer.write((PyssMain.username + ":  " + self.txtInputMessage.GetValue()).encode())
                self.txtConversation.AppendText("\n" + self.txtInputMessage.GetValue())
                self.txtInputMessage.SetValue("")
                await writer.drain()
            #do the reading
            data = await reader.read(100)  # Max number of bytes to read
            if not data:
                await asyncio.sleep(1)
                break
            elif data == b" ":  # dummy character to indicate that WRITE stream is ready
                pass            # and to interupt READ stream
            else:
                # print incoming messages to the text area
                self.txtConversation.AppendText("\n" + str(data, "utf-8"))
        

    # main server function that runs in the background
    async def runHost(self):
        server = await asyncio.start_server(self.msg_server, PyssMain.HOST, PyssMain.PORT)
        await server.serve_forever()





# Launcher - Collects necessary information before main program
class PyssLaunch(wx.Frame):

    # Constructor
    def __init__(self):
        super().__init__(parent=None, title='Pyssenger')
        panelMain = wx.Panel(self)

        # Identify public IP
        try:
            PyssMain.IP = urllib.request.urlopen('https://ident.me').read().decode('utf8')
            #PyssMain.IP = '127.0.0.1'
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

        # Binding - After button click, initiates transition to MainPyss
        btnHostRun.Bind(wx.EVT_BUTTON, self.on_press)

        self.Show()

    # Callback function - Handles the input and validates proper Main program initialization
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
    # app0 represents the Launcher Application
    app0 = wx.App()
    frame = PyssLaunch()
    app0.MainLoop()
    if launchSuccess:
        # app represents the Main Application
        app = WxAsyncApp()
        frame = PyssMain()
        loop = get_event_loop()
        loop.run_until_complete(app.MainLoop())
