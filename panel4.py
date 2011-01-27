#!/usr/bin/env python

#Setup to save executable as a saved setting

import wx
import wx.lib.stattext
import subprocess
import thread

class runPanel(wx.Panel):
    def __init__(self, obj, parent):
        #Globals
        self.appFolder = ""
        self.newProject = ""
        self.newCommand = ""
        self.queueList = []
        #self.queueFinished = []
        self.newOutputFolder = ""
        
        wx.Panel.__init__(self, parent)
        
        wx.Button(self, 1, 'Executable', (10, 5))
        self.execPath = wx.TextCtrl(self, -1, 'Path to application executable', (110, 5), wx.Size(635, -1))
        
        wx.Button(self, 2, 'Project File', (10, 35))
        self.projFileTxt = wx.lib.stattext.GenStaticText(self, -1, 'Project Filename and path', (110, 37))
        self.isBlender = wx.CheckBox(self, 11, 'Blender File', (500, 35))
        self.isBlender.SetValue(True)
        self.blenderAnim = wx.CheckBox(self, 12, 'Animation', (600, 35))
        #self.blenderAnim.Enable(False)
        
        wx.Button(self, 3, 'Output Folder', (10, 65))
        self.outputFolderTxt = wx.lib.stattext.GenStaticText(self, -1, 'Optional Output Folder Path', (130, 67))
       
        wx.StaticText(self, -1, 'Command Options:', (10, 95))
        self.commandOpts = wx.TextCtrl(self, -1, 'Not ready yet', (140, 95), wx.Size(605, -1))
        self.commandOpts.Enable(False)
        
        wx.StaticText(self, -1, 'Final Command:', (10, 125))
        self.finalCommand = wx.lib.stattext.GenStaticText(self, -1, 'Final Command Layout', (120, 125))
        
        wx.Button(self, 4, 'Add to Queue', (10, 155))
        self.projFiles = wx.ListCtrl(self, -1, (10, 185), wx.Size(280, 180), style=wx.LC_REPORT)
        self.projFiles.InsertColumn(0,'Job Files')
        self.projFiles.SetColumnWidth(0, 280)
        
        wx.Button(self, 5, 'Remove from Queue', (10, 370))
        wx.Button(self, 9, 'Clear Queue', (10, 405))
        
        #wx.StaticText(self, -1, 'Current Render:', (360, 155))
        #self.currentRender = wx.lib.stattext.GenStaticText(self, -1, '', (465, 155))
        
        #wx.StaticText(self, -1, 'Finished:', (405, 185))
        #self.queueFinished = wx.ListCtrl(self, -1, (465, 185), wx.Size(280, 180), style=wx.LC_REPORT)
        #self.queueFinished.InsertColumn(0, 'Finished Jobs')
        #self.queueFinished.SetColumnWidth(0, 280)
        #wx.Button(self, 8, 'Clear Finished', (550, 370))
        
        self.startButton = wx.Button(self, 6, '----- Start Queue -----', (300, 400))
        wx.Button(self, 7, '----- Stop Queue -----', (300, 435))

        self.Bind(wx.EVT_BUTTON, self.execDir, id=1)
        self.Bind(wx.EVT_BUTTON, self.getProject, id=2)
        self.Bind(wx.EVT_CHECKBOX, self.blenderJob, id=11)
        self.Bind(wx.EVT_CHECKBOX, self.isBlenderAnim, id=12)
        self.Bind(wx.EVT_BUTTON, self.outputFolder, id=3)
        self.Bind(wx.EVT_TEXT, self.updateCmd, self.commandOpts)
        self.Bind(wx.EVT_BUTTON, self.addQueue, id=4)
        self.Bind(wx.EVT_BUTTON, self.removeQueue, id=5)
        self.Bind(wx.EVT_BUTTON, self.startQueue, id=6)
        #self.Bind(wx.EVT_BUTTON, self.stopQueue, id=7)
        #self.Bind(wx.EVT_BUTTON, self.clearFinished, id=8)
        #self.Bind(wx.EVT_BUTTON, self.clearJobs, id=9)
        
    #Functions
    
    def buildCommand(self):
        newCommandList = []
        newFinalList = []
        if self.appFolder != "":
            newCommandList.append(self.appFolder)
            a = self.appFolder.split('/')
            newFinalList.append(a[-1])
        if self.isBlender.GetValue() == True:
            newCommandList.append(' -b ')
            newFinalList.append(' -b ')
        if self.newProject != "":
            newCommandList.append(self.newProject)
            b = self.newProject.split('/')
            newFinalList.append(b[-1])
        if self.newOutputFolder != "":
            newCommandList.append(' -o ' + self.newOutputFolder)
            c = self.newOutputFolder.split('/')
            newFinalList.append(' -o ' + c[-2])
        if self.blenderAnim.GetValue() == True:
            newCommandList.append(' -a')
            newFinalList.append(' -a')
        
        self.newCommand = ''
        finalCommandTxt = ''
        for i in newCommandList:
            self.newCommand = self.newCommand + i
        for i in newFinalList:
            finalCommandTxt = finalCommandTxt + i
        self.finalCommand.SetLabel(finalCommandTxt)
        
    
    def execDir(self, event):
        dlg = wx.FileDialog(self, "Choose Renderer:", style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            pass
        dlg.Destroy()
        
        if dlg.GetFilename():
            self.appFolder = dlg.GetPath()
            if self.appFolder.endswith('.app') == True:
                self.execPath.SetValue(self.appFolder + '/Contents/MacOS/blender')
                self.appFolder = self.appFolder + '/Contents/MacOS/blender'
                self.buildCommand()
            else:
                self.execPath.SetValue(self.appFolder)
                self.buildCommand()
        else:
            self.appFolder = ''
    
    def getProject(self, event):
        dlg = wx.FileDialog(self, "Choose Project File:", style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            pass
        dlg.Destroy()
        
        if dlg.GetFilename():
            self.newProject = dlg.GetPath()
            self.newProjectFilename = dlg.GetFilename()
            self.projFileTxt.SetLabel(self.newProjectFilename)
            #Create command
            self.buildCommand()
        else:
            pass
    
    def blenderJob(self, event):
        if self.isBlender.GetValue() == True:
            self.blenderAnim.Enable(True)
            self.buildCommand()
        else:
            self.buildCommand()
    
    def isBlenderAnim(self, event):
        self.buildCommand()
    
    def outputFolder(self, event):
        dlg = wx.DirDialog(self, "Choose an Output Folder:", style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            pass
        dlg.Destroy()
        
        if dlg.GetPath():
            self.newOutputFolder = dlg.GetPath() + '/'
            self.outputFolderTxt.SetLabel(self.newOutputFolder)
            self.buildCommand()
        else:
            self.newOutputFolder = ''
            self.outputFolderTxt.SetLabel('Optional Output Folder Path')
            self.buildCommand()
    
    def updateCmd(self, event):
        #Not ready yet - will add the ability to add the rest of the flags available to renderer
        pass
        
    # Get files and put into a list
    def addQueue(self, event):
        if self.appFolder != '':
            if self.newCommand != "":
                self.queueList.append(self.newCommand)
                a = self.newProject.split('/')
                index = len(self.queueList) - 1
                self.projFiles.InsertStringItem(index, a[-1])
        else:
            pass
    
    def removeQueue(self, event):
        index = self.projFiles.GetFocusedItem()
        if index != -1:
            self.projFiles.DeleteItem(index)
            self.queueList.pop(index)
    
    def render(self):
        self.startButton.SetLabel('!!!!! Queue Running !!!!!')
        for i in range(len(self.queueList)):
            listTxt = self.projFiles.GetItemText(i)
            self.currentRender.SetLabel(listTxt)
            try:
                self.process = subprocess.Popen([self.queueList[i]], shell=True) #, stdout=subprocess.PIPE
                self.process.wait()
                #while True:
                #    if self.process.poll() != None:
                #        break
                self.queueFinished.InsertStringItem(i, listTxt)
            except:
                break
            
        dlg = wx.MessageDialog(self, '',
                        'Render Jobs are Finished!',
                        wx.OK | wx.ICON_INFORMATION
                        #wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                        )
        dlg.ShowModal()
        dlg.Destroy()
        self.startButton.SetLabel('----- Start Queue -----')
    
    def startQueue(self, event):
        if self.queueList != []:
            thread.start_new_thread(self.render, ()) #threaded so the GUI is not locked

    #def stopQueue(self, event):
    #    try:
    #        self.process.terminate() #requires Python 2.6+
    #    except:
    #        pass
        
    def clearJobs(self, event):
        self.projFiles.ClearAll()
        self.queueList = []
    
    #def clearFinished(self, event):
    #    self.queueFinished.ClearAll()