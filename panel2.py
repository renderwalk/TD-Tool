#!/usr/bin/env python

#rsync interface

import wx
import wx.lib.stattext
import subprocess
import thread

# rsync -avuE --delete source destination
#   -a archive
#   -v verbose
#   -u update - not necessary for true backup, assumes destination could have newer files
#   -E for syncing to a non-hfs+ volume


class runPanel(wx.Panel):
    def __init__(self, obj, parent):
        wx.Panel.__init__(self, parent)
        
        self.sourceFolder = "none"
        self.targetFolder = "none"
        
        wx.Button(self, 1, 'Choose Source Folder', (10, 5))
        self.s = wx.lib.stattext.GenStaticText(self, -1, "rsync source", (20,35))
        wx.Button(self, 2, 'Choose Target Folder', (10, 90))
        self.t = wx.StaticText(self, -1, 'rsync target', (20,120))
        self.deleteTarget = wx.CheckBox(self, -1, 'Delete files on Target that were deleted on Source', (10,180))
        self.goButton = wx.Button(self, 3, '----- Go rsync -----', (100, 300))
        #self.rsyncOutput = wx.TextCtrl(self, -1, '', (390, 10), wx.Size(380,430), style=wx.TE_MULTILINE)
        #self.rsyncOutput.SetEditable(False)
        self.nonHFS = wx.CheckBox(self, -1, 'Sync to non-HFS volume (Mac Only)', (10, 200))

        self.Bind(wx.EVT_BUTTON, self.ChooseSource, id=1)
        self.Bind(wx.EVT_BUTTON, self.ChooseTarget, id=2)
        self.Bind(wx.EVT_BUTTON, self.GoRsync, id=3)
        
    def ChooseSource(self, event):
        dlg = wx.DirDialog(self, "Choose a Source Folder:", style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            #print ('You selected: %s\n' % dlg.GetPath())
            pass
        dlg.Destroy()
        
        if dlg.GetPath():
            self.sourceFolder = (dlg.GetPath() + '/')
            self.s.SetLabel(self.sourceFolder)
        else:
            self.sourceFolder = 'none'
            self.s.SetLabel('')
            
    def ChooseTarget(self, event):
        dlg = wx.DirDialog(self, "Choose a Target Folder:", style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            pass
        dlg.Destroy()
        
        if dlg.GetPath():
            self.targetFolder = dlg.GetPath()
            self.t.SetLabel(self.targetFolder)
        else:
            self.targetFolder = 'none'
            self.t.SetLabel('')

#    def updateUI(self):
#        o = self.p.stdout.readline()
#        self.rsyncOutput.AppendText(o)
    
    def execRsync(self):
        if self.deleteTarget.GetValue():
            if self.nonHFS.GetValue():
                cmd = ["rsync", "-avE", "--delete", self.sourceFolder, self.targetFolder]
            else:
                cmd = ["rsync", "-av", "--delete", self.sourceFolder, self.targetFolder]
        else:
            if self.nonHFS.GetValue():
                cmd = ["rsync", "-avE", self.sourceFolder, self.targetFolder]
            else:
                cmd = ["rsync", "-av", self.sourceFolder, self.targetFolder]
        
        #Change Button
        self.goButton.SetLabel('!!!!! Rsync Running !!!!!')
        p = subprocess.Popen(cmd)
        
        p.wait()
        
        #while True:
        #    if p.poll() != None:
        #        break
        #Change Button
        self.goButton.SetLabel('----- Go rsync -----')
        
        dlg = wx.MessageDialog(self, '',
                        'Rsync is Finished!',
                        wx.OK | wx.ICON_INFORMATION
                        #wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                        )
        dlg.ShowModal()
        dlg.Destroy()
    
    def GoRsync(self, event):
        if self.sourceFolder == 'none':
            pass #dialog
        elif self.targetFolder == 'none':
            pass #dialog
        else:
            thread.start_new_thread(self.execRsync, ())
            #self.execRsync()
            
    def StopRsync(self, event):
        pass
    