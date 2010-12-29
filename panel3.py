#!/usr/bin/env python

import wx
import os
import glob
import wx.lib.stattext
import sys

class runPanel(wx.Panel):
    def __init__(self, obj, parent):
        wx.Panel.__init__(self, parent)
        
        # Variables to check UI elements and folders
        self.setExisting = 0
        self.setDestination = 0
        self.fileFolder = 'none'
        self.destFolder = 'none'
        
        wx.Button(self, 1, 'Choose Folder', (10, 5))
        self.sf = wx.lib.stattext.GenStaticText(self, -1, "Folder of files to be renamed", (15,35))
        self.destinationCheck = wx.CheckBox(self, 6, 'Copy to rename', (10,70))
        self.destButton = wx.Button(self, 2, 'Destination Folder', (10, 100))
        self.destButton.Enable(False)
        self.df = wx.lib.stattext.GenStaticText(self, -1, "", (15, 130))
        
        self.useExisting = wx.CheckBox(self, 3, 'Use existing filename', (10, 180))
        wx.StaticText(self, -1, 'Prefix:', (10, 210))
        self.prefix = wx.TextCtrl(self, -1, '', (90, 210), wx.Size(200,-1))
        self.prefix.Enable(False)
        wx.StaticText(self, -1, 'Suffix:', (10, 240))
        self.suffix = wx.TextCtrl(self, -1, '', (90, 240), wx.Size(200,-1))
        self.suffix.Enable(False)
        
        wx.StaticText(self, -1, 'New Name:', (10, 300))
        self.newName = wx.TextCtrl(self, -1, '', (90, 300), wx.Size(200,-1))
        wx.StaticText(self, -1, 'Start #:', (20, 330))
        self.startNum = wx.TextCtrl(self, -1, '1', (90, 330), (50,-1))
        wx.StaticText(self, -1, 'Padding:', (180, 330))
        self.padding = wx.TextCtrl(self, -1, '3', (240, 330), (50, -1))
        wx.StaticText(self, -1, 'Separator:', (20, 362))
        sepList = ['_','-','none']
        self.separator = wx.ComboBox(self, -1, value=sepList[0], pos = wx.Point(87, 360), size=wx.Size(70 ,-1), choices=sepList)
      
        wx.Button(self, 5, '----- Rename Files -----', (400, 65))
        
        #self.renameList = wx.TextCtrl(self, -1, '', (390, 100), wx.Size(380, 350), style=wx.TE_MULTILINE)
        #self.renameList.SetEditable(False)
        
        self.combinedName = wx.lib.stattext.GenStaticText(self, -1, "filename.xxx", (400,35))
        
        self.Bind(wx.EVT_BUTTON, self.chooseFolder, id=1)
        self.Bind(wx.EVT_BUTTON, self.chooseDestination, id=2)
        self.Bind(wx.EVT_CHECKBOX, self.existing, id=3)
        self.Bind(wx.EVT_BUTTON, self.renameFiles, id=5)
        self.Bind(wx.EVT_CHECKBOX, self.destMake, id=6)
        
        self.Bind(wx.EVT_TEXT, self.updatePreSuf, self.prefix)
        self.Bind(wx.EVT_TEXT, self.updatePreSuf, self.suffix)
        self.Bind(wx.EVT_TEXT, self.updateSequential, self.newName)
        self.Bind(wx.EVT_TEXT, self.updateSequential, self.startNum)
        self.Bind(wx.EVT_TEXT, self.updateSequential, self.padding)
        self.Bind(wx.EVT_COMBOBOX, self.updateSequential, self.separator)
        
    # Choose a folder full of files to rename
    def chooseFolder(self, event):
        dlg = wx.DirDialog(self, "Choose a Folder:", style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            pass
        dlg.Destroy()
        
        if dlg.GetPath():
            self.fileFolder = dlg.GetPath()
            self.sf.SetLabel(self.fileFolder)
        else:
            self.fileFolder = 'none'
            self.sf.SetLabel('')
    
    # Choose a destination folder if desired
    def chooseDestination(self, event):
        dlg = wx.DirDialog(self, "Choose a Source Folder:", style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            pass
        dlg.Destroy()
        
        if dlg.GetPath():
            self.destFolder = dlg.GetPath()
            self.df.SetLabel(self.destFolder)
        else:
            self.destFolder = 'none'
            self.df.SetLabel('')
    
    # Change UI as needed
    def existing(self, event):
        if self.useExisting.GetValue():
            self.prefix.Enable(True)
            self.suffix.Enable(True)
            self.newName.Enable(False)
            self.setExisting = 1
            self.startNum.Enable(False)
            self.separator.Enable(False)
            self.padding.Enable(False)
            self.updatePreSuf(event)
            
        else:
            self.prefix.Enable(False)
            self.suffix.Enable(False)
            self.newName.Enable(True)
            self.startNum.Enable(True)
            self.separator.Enable(True)
            self.padding.Enable(True)
            self.setExisting = 0
            self.updateSequential(event)
    
    # Change UI if using a destination folder
    def destMake(self, event):
        if self.destinationCheck.GetValue():
            self.destButton.Enable(True)
            self.setDestination = 1
        else:
            self.destButton.Enable(False)
            self.setDestination = 0
    
    # Add prefix and/or suffix
    def doPreSuf(self, filename):
        a = filename #'filename.xxx'
        b = a.split('.')
        
        pre = self.prefix.GetValue()
        suf = self.suffix.GetValue()
        
        if pre != '':
            b.insert(0, pre)
        if suf != '':
            b.insert(-1, suf)
        
        b.insert(-1, '.')
        presuf = ''
        
        for i in b:
            presuf = presuf + i
            
        return presuf
    
    # Update the UI
    def updatePreSuf(self, event):
        returned = self.doPreSuf('filename.xxx')
        self.combinedName.SetLabel(returned)

    # Create the sequential filename
    # n is the current number to add to the filename
    def doSequential(self, filename, n):
        a = filename
        b = a.split('.')
        
        sep = self.separator.GetValue()
        if sep == 'none':
            sep = ''                
        
        # Create number padding - rework
        p = int(self.padding.GetValue())
        c = ''
        if len(n) < p:
            for i in range (len(n), p):
                c = c + '0'
        newStart = c + n
        
        b.pop(0)
        b.insert(0, self.newName.GetValue()) # newName is the name of the file
        b.insert(-1, sep)
        b.insert(-1, newStart)
        b.insert(-1, '.')
        d = ''
        for i in b:
            d = d + i
        
        return d

    # Update the UI to show what changes will happen
    def updateSequential(self, event):
        d = self.doSequential('filename.xxx', self.startNum.GetValue())
        self.combinedName.SetLabel(d)

    # Here is where it all happens
    def renameFiles(self, event):
        #assumes all files are ready to be renamed in a folder and all files have an extension
        # consider checking for OS to replace '/*.*'
        
        # Check to see if a folder was chosen
        if self.fileFolder == 'none':
            dlg = wx.MessageDialog(self, '',
                        'Choose a folder of files to be renamed',
                        wx.OK | wx.ICON_INFORMATION
                        #wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                        )
            dlg.ShowModal()
            dlg.Destroy()
        
        else:
            def copyOrRename(fileName, file):
                # Copy the file
                if self.setDestination == 1:
                    print self.destFolder + '/' + file
                    cmdString = 'cp ' + self.fileFolder + '/' + fileName + ' ' + self.destFolder + '/' + file
                    cmd = os.system(cmdString)
                    #self.renameList.AppendText((fileName + ' --> ' + returned + '\n'))                    
                    
                else:
                    print self.fileFolder + '/' + file
                    #self.renameList.AppendText((fileName + ' --> ' + returned + '\n'))
                    os.rename(self.fileFolder + '/' + fileName, self.fileFolder + '/' + file)
                
            if self.setDestination == 1:
                path = self.destFolder
            else:
                path = self.fileFolder
                
            n = self.startNum.GetValue()
            for infile in glob.iglob(self.fileFolder + '/*.*'):
                fileName = os.path.basename(infile)
                
                if self.setExisting == 1:
                    returned = self.doPreSuf(fileName)
                    copyOrRename(fileName, returned)
                    
                else:
                    returned = self.doSequential(fileName, n)
                    copyOrRename(fileName, returned)
                    n = int(n) + 1
                    n = str(n)
                
            dlg = wx.MessageDialog(self, 'Renamed Files',
                        'DONE!',
                        wx.OK | wx.ICON_INFORMATION
                        #wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                        )
            dlg.ShowModal()
            dlg.Destroy()
            #self.renameList.AppendText('\n' + 'DONE!!' + '\n')