#!/usr/bin/env python

import wx

class MainFrame(wx.Frame):

        def __init__(self, parent, id, title):
            wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, wx.Size(800,530))

            # Create the Notebook
            self.nb = wx.Notebook(self, -1, wx.Point(0,0), wx.Size(0,0), wx.NB_FIXEDWIDTH)

            # Make PANEL_1 (filename: panel1.py)
            self.module = __import__("panel1", globals())
            self.window = self.module.runPanel(self, self.nb)
            if self.window:
                    self.nb.AddPage(self.window, "Project Builder")

            # Make PANEL_2 (filename: panel2.py)
            self.module = __import__("panel2", globals())
            self.window = self.module.runPanel(self, self.nb)
            if self.window:
                    self.nb.AddPage(self.window, "rsync")

            # Make PANEL_3 (filename: panel3.py)
            self.module = __import__("panel3", globals())
            self.window = self.module.runPanel(self, self.nb)
            if self.window:
                    self.nb.AddPage(self.window, "Sequence Renamer")
                    
            # Make PANEL_4 (filename: panel4.py)
            self.module = __import__("panel4", globals())
            self.window = self.module.runPanel(self, self.nb)
            if self.window:
                    self.nb.AddPage(self.window, "Render Queue")

class PBTApp(wx.App):
    def OnInit(self):
        frame = MainFrame(None, -1, "Technical Director's Tool")
        frame.Show(True)
        frame.Centre()
        return True
    
app = PBTApp(0)
app.MainLoop()