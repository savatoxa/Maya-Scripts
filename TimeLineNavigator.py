import maya.cmds as cmds
import pymel.core as pm

rangeLocator = 'rangelocator'
rangeList = []

def SortRangeListByRangeBeg():
    def GetRangebeg(rangename):
        return cmds.attributeQuery(rangename, node = rangeLocator, minimum = True)[0]
    rangeList.sort(key = GetRangebeg)

def AddToRangeList(rangename):
    rangeList.append(rangename)
    SortRangeListByRangeBeg()
    RefreshScrolList()
    
def DeleteFromRangeList(rangename):
    rangeList.remove(rangename)
    SortRangeListByRangeBeg()
    
def RenameInRangeList(newRangename, oldRangename):
    rangeList.remove(oldRangename[0])
    rangeList.append(newRangename)
    SortRangeListByRangeBeg()
    RefreshScrolList()

def CreateRangesLocator():
    if cmds.objExists(rangeLocator):
        ranges = cmds.listAttr(rangeLocator, userDefined = True)
        if ranges:
            rangeList.extend(ranges)
            SortRangeListByRangeBeg()
    else:
        cmds.spaceLocator(p = (0, 0, 0), n = rangeLocator)
        cmds.setAttr(rangeLocator + '.visibility', 0)
        #cmds.createDisplayLayer(name = rangeLocator + 'Layer')
        #cmds.setAttr(rangeLocator + 'Layer.visibility', 0)
        cmds.select(clear = True)

def GetRangenameText():
	return cmds.textField(rangenameTxtField, editable = True, query = True, text = True)

def GetRangesNamesScrolList():
    rangename = cmds.textScrollList(rangesScrolList, query = True, selectItem = True)
    cmds.textField(rangenameTxtField, edit = True, text = rangename[0])
    return rangename
    
def CreateRangeAttr(rangename):
    if (rangename != '' and rangename not in rangeList):
        cmds.select(rangeLocator)
        cmds.addAttr(longName = rangename, attributeType = 'float', minValue = cmds.playbackOptions(q=True,min=True),
                     maxValue = cmds.playbackOptions(q=True,max=True), keyable = False, writable = True)
        cmds.select(clear = True)
        AddToRangeList(rangename)
    
def ChangeRange(rangename):
    if (rangename and len(rangename) == 1):
        att = pm.PyNode(rangeLocator + '.' + rangename[0])
        if cmds.playbackOptions(q=True,max=True) <= cmds.attributeQuery(rangename, node = rangeLocator, maximum = True)[0]:
            att.setMin(cmds.playbackOptions(q=True,min=True))
            att.setMax(cmds.playbackOptions(q=True,max=True))
        else:
            att.setMax(cmds.playbackOptions(q=True,max=True))
            att.setMin(cmds.playbackOptions(q=True,min=True))
        SortRangeListByRangeBeg()
        RefreshScrolList()
    
def SetRanges(rangesname):
    if (rangesname):
        rangebeg = cmds.attributeQuery(rangesname[0], node = rangeLocator, minimum = True)[0]
        rangeend = cmds.attributeQuery(rangesname[len(rangesname) - 1], node = rangeLocator, maximum = True)[0]
        cmds.playbackOptions(minTime = rangebeg, maxTime = rangeend)
    
def DeleteRange(rangenames):
    if (rangenames):
        for rangename in rangenames:
            cmds.deleteAttr(rangeLocator, at = rangename)
            DeleteFromRangeList(rangename)
        RefreshScrolList()
    
def RenameRange(newRangename, oldRangename):
    if (oldRangename and len(oldRangename) == 1 and newRangename != '' and newRangename not in rangeList):
        cmds.renameAttr(rangeLocator + '.' + oldRangename[0], newRangename)
        RenameInRangeList(newRangename, oldRangename)
        cmds.textField(rangenameTxtField, edit = True, text = newRangename)
      
def RefreshScrolList():
    cmds.textScrollList(rangesScrolList, edit=True, removeAll=True)
    cmds.textScrollList(rangesScrolList, edit = True, append = rangeList)

CreateRangesLocator()

#if cmds.window(window , exists = 1) : cmds.deleteUI(window)
window = cmds.window( title = "TimeLine navigator", iconName = 'TLN', widthHeight = (200, 325) )
cmds.columnLayout( adjustableColumn=True )
rangesScrolList = cmds.textScrollList('rangesscrollist', numberOfRows=12, allowMultiSelection = True, append = rangeList,
                                       selectCommand = lambda *args: GetRangesNamesScrolList())
rangenameTxtField = cmds.textField(editable = True)
cmds.button( label = 'Ctreate Range', command = lambda *args: CreateRangeAttr(GetRangenameText()) )
cmds.button( label = 'Redefine Range', command = lambda *args: ChangeRange(GetRangesNamesScrolList()) )
cmds.button( label = 'Set Range', command = lambda *args: SetRanges(GetRangesNamesScrolList()) )
cmds.button( label = 'Delete Range', command = lambda *args: DeleteRange(GetRangesNamesScrolList()) )
cmds.button( label = 'Rename Range', command = lambda *args: RenameRange(GetRangenameText(), GetRangesNamesScrolList()) )
cmds.setParent( '..' )
cmds.showWindow( window )