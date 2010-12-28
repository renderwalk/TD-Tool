#!/usr/bin/env python

# This panel will create folders to start projects
# W. Scott Meador

# TODO:
# DEAL WITH DUPLICATE FOLDER ENTRIES
# ADD HELP TO THE RIGHT SIDE OF TREECTRL

import os
import wx
import images
import xml.etree.cElementTree as ET
import wsm_paths as wsm

class runPanel(wx.Panel):
    def __init__(self, obj, parent):
        wx.Panel.__init__(self, parent)
        self.dirPath = ""
        
        # Buttons - Choose, Add, Create Folders, Remove (or with the delete key)
        wx.Button(self, 1, 'Choose Project Folder', (10, 5))
        wx.Button(self, 2, 'Add', (10, 435))
        wx.Button(self, 3, 'Remove', (88,435))
        wx.Button(self, 4, 'Make Defaults', (170,435))
        wx.Button(self, 5, 'Create Folders', (295, 435))
        
        self.tree = wx.TreeCtrl(self, -1, (10,30), wx.Size(400,400), style=wx.SIMPLE_BORDER|wx.TR_HAS_BUTTONS)
        
        isz = (16,16)
        il = wx.ImageList(isz[0], isz[1])
        self.fldridx = il.Add(wx.ArtProvider_GetBitmap(wx.ART_FOLDER,      wx.ART_OTHER, isz))
        self.fldropenidx = il.Add(wx.ArtProvider_GetBitmap(wx.ART_FILE_OPEN,   wx.ART_OTHER, isz))
        self.fileidx = il.Add(wx.ArtProvider_GetBitmap(wx.ART_NORMAL_FILE, wx.ART_OTHER, isz))
        self.smileidx = il.Add(images.getSmilesBitmap())
        
        self.tree.SetImageList(il)
        self.il = il
        
        # Get XML file
        # Call fillmeup
        tmpPath = os.path.split((os.path.abspath(wsm.__file__)))
        wsm.userpaths = tmpPath[0] + '/user_paths.xml'
        self.xml = ET.parse(wsm.userpaths)
        root = self.fillmeup()
        
        # expand root
        self.tree.Expand(root)
        # Bindings
        self.Bind(wx.EVT_BUTTON, self.OnChoose, id=1)
        self.Bind(wx.EVT_BUTTON, self.OnAdd, id=2)
        self.Bind(wx.EVT_BUTTON, self.OnRemove, id=3)
        self.Bind(wx.EVT_BUTTON, self.userDefaults, id=4)
        self.Bind(wx.EVT_BUTTON, self.OnCreate, id=5)
        
        self.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged, self.tree)
        self.Bind(wx.EVT_TREE_BEGIN_LABEL_EDIT, self.OnBeginEdit, self.tree)
        self.Bind(wx.EVT_TREE_END_LABEL_EDIT, self.OnEndEdit, self.tree)
        
        self.tree.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        self.tree.Bind(wx.EVT_RIGHT_UP, self.OnRightUp)
    
    def fillmeup(self):
        xml = self.xml.getroot() #goes to root of xml file
        tree = self.tree #tree control
        root = tree.AddRoot(xml.tag) #adds root, which is first tag in file
        def add(parent, elem): #add function gets root and rest of xml
            for e in elem:
                text = e.text.strip()
                val = tree.AppendItem(parent, text)
                tree.SetPyData(val, e)
                tree.SetItemImage(val, self.fldridx, wx.TreeItemIcon_Normal)
                tree.SetItemImage(val, self.fldropenidx, wx.TreeItemIcon_Expanded)
                add(val, e)
        add(root, xml) #root = treeCtrl, xml = xml root
        return root
    
    def OnChoose(self, event):
        dlg = wx.DirDialog(self, "Choose a directory:", style=wx.DD_DEFAULT_STYLE)
        if dlg.ShowModal() == wx.ID_OK:
            #print ('You selected: %s\n' % dlg.GetPath())
            pass
        dlg.Destroy()
        
        self.dirPath = dlg.GetPath()
        self.dirname = os.path.basename(dlg.GetPath())
        # make directory name the same as the root folder
        self.tree.SetItemText(self.tree.GetRootItem(),self.dirname)
    
    def OnAdd(self, event):
        # Consider a text entry box
        cursel = self.tree.GetSelection()
        sub = self.tree.AppendItem(cursel, 'untitled')
        self.tree.SetPyData(sub, None)
        self.tree.SetItemImage(sub, self.fldridx, wx.TreeItemIcon_Normal)
        self.tree.SetItemImage(sub, self.fldropenidx, wx.TreeItemIcon_Expanded)
        self.tree.EditLabel(sub)
        # Note self.tree.SortChildren()
    
    def OnRemove(self, event):
        cursel = self.tree.GetSelection()
        root = self.tree.GetRootItem()
        if cursel == root:
            wx.Bell()
            # print "Can't remove root folder"
            event.Veto()
        else:
            self.tree.Delete(cursel)
    
    def folderList(self, child, folder):
        # make a list and feed into os.makedirs
        self.list.append(folder)
        parent = self.tree.GetItemParent(child)
        self.list.insert(0,self.tree.GetItemText(parent))
        # loop through list to find parent and build a path and then empty list
        while True:
            parent = self.tree.GetItemParent(parent)
            if parent:
                self.list.insert(0,self.tree.GetItemText(parent))
            else:
                break
        self.list.pop(0)
        try:
            os.makedirs(self.dirPath + '/' + ('/'.join(self.list))) # make directories here
        except os.error:
            pass
        self.list = []
    
    def subFolders(self, folder, cookie, parentDir):
        item,cookie = self.tree.GetFirstChild(folder)
        self.folderList(item,self.tree.GetItemText(item))
        while True:
            if self.tree.ItemHasChildren(item):
                self.subFolders(item,item,self.tree.GetItemText(item))
            item = self.tree.GetNextSibling(item)
            if not item:
                break
            self.folderList(item,self.tree.GetItemText(item))
    
    def OnCreate(self, event):
        self.list = []
        if self.dirPath == "":
            dlg = wx.MessageDialog(self, 'Choose a Project Folder',
                        "Can't do it yet",
                        wx.OK | wx.ICON_INFORMATION
                        #wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                        )
            dlg.ShowModal()
            dlg.Destroy()
        else:
            #check if project folder already exists - throw up a dialog to check if overwrite
            cookie = 0
            rootItem = self.tree.GetRootItem()
            item,cookie = self.tree.GetFirstChild(rootItem)
    
            while True:
                if not item:
                    # Confirm with a dialog box
                    dlg = wx.MessageDialog(self, 'Folders Created!',
                                'DONE',
                                wx.OK | wx.ICON_INFORMATION
                                #wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                                )
                    dlg.ShowModal()
                    dlg.Destroy()
                    break
                self.folderList(item,self.tree.GetItemText(item)) # adds main tree members
                if self.tree.ItemHasChildren(item):
                    self.subFolders(item,item,self.tree.GetItemText(item)) # adds tree child members
                item = self.tree.GetNextSibling(item)
    
    def OnRightDown(self, event):
        pt = event.GetPosition();
        item, flags = self.tree.HitTest(pt)
        if item:
            self.tree.SelectItem(item)
    
    def OnRightUp(self, event):
        pt = event.GetPosition();
        item, flags = self.tree.HitTest(pt)
        if item:        
            self.tree.EditLabel(item)
    
    def OnBeginEdit(self, event):
        # show how to prevent edit...
        item = event.GetItem()
        root = self.tree.GetRootItem()
        if item == root: #and self.tree.GetItemText(item)
            wx.Bell()
            #print "You can't edit this one...\n"
            event.Veto()
    
    def OnEndEdit(self, event):
        pass
    
    def OnSelChanged(self, event):
        pass
    
    def userDefaults(self, event):
        xmlroot = ET.Element("Project_Builder")
        cookie = 0
        rootItem = self.tree.GetRootItem()
        item,cookie = self.tree.GetFirstChild(rootItem)
    
        def subNodes(folder, cookie, elem):
            item,cookie = self.tree.GetFirstChild(folder)
            new = ET.SubElement(elem, "node")
            new.text = self.tree.GetItemText(item)
    
            while True:
                if self.tree.ItemHasChildren(item):
                    subNodes(item,item,new)
                item = self.tree.GetNextSibling(item)
                if not item:
                    break
                current = ET.SubElement(elem, "node")
                current.text = self.tree.GetItemText(item)
    
        while True:
            if not item:
                break
            new = ET.SubElement(xmlroot, "node")
            new.text = self.tree.GetItemText(item)
            if self.tree.ItemHasChildren(item):
                subNodes(item,item, new) # adds tree child members
            item = self.tree.GetNextSibling(item)
    
        tree = ET.ElementTree(xmlroot)
        #tree.write("/Applications/TD_Tool/user_paths.xml")
        tree.write(wsm.userpaths)

