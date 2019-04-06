import urllib.request
import wx

# Flags here
launchSuccess = False

class PyssMain(wx.Frame):

    username = None
    port = None
    IP = None

    def __init__(self):
        super().__init__(parent=None, title='Pyssenger')
        panelMain = wx.Panel(self)

        stIPInfo = wx.StaticText(panelMain, label="Your external IP is: ", pos=(5,10))
        stIP = wx.TextCtrl(panelMain, value=PyssMain.IP, pos=(125, 5), style=wx.TE_READONLY)

        self.txtConversation = wx.TextCtrl(panelMain, value="test", pos=(5, 50), size=(250, 80), style=wx.TE_MULTILINE|wx.TE_READONLY)

        self.txtInputMessage = wx.TextCtrl(panelMain, value="moar", pos=(5, 135), style=wx.TE_PROCESS_ENTER)
        btnSendMsg = wx.Button(panelMain, label='Send', pos=(200, 135))

        btnSendMsg.Bind(wx.EVT_BUTTON, self.on_press)
        self.txtInputMessage.Bind(wx.EVT_TEXT_ENTER, self.on_press)

        self.Show()

    def on_press(self, event):
            if self.txtInputMessage.GetValue():
                self.txtConversation.AppendText("\n" + self.txtInputMessage.GetValue())
                self.txtInputMessage.SetValue("")






class PyssLaunch(wx.Frame):

    def __init__(self):
        super().__init__(parent=None, title='Pyssenger')
        panelMain = wx.Panel(self)

        # Other initialization
        try:
            PyssMain.IP = urllib.request.urlopen('https://ident.me').read().decode('utf8')
        except Exception as x:
            print(x)
            PyssMain.IP = 'undefined'

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
        PyssMain.port     = self.txtInputPort.GetValue()
        if not PyssMain.username or not PyssMain.port:
            print("Both fields are required in order to initiate connection!")
        else:
            self.Destroy()
            launchSuccess = True



if __name__ == '__main__':
    app = wx.App()
    frame = PyssLaunch()
    app.MainLoop()
    if launchSuccess:
        frame = PyssMain()
        app.MainLoop()
    #print(PyssMain.username, PyssMain.port, PyssMain.IP)
