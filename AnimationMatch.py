import maya.cmds as cmds
childsListAll = []

def DuplicateChar():
    selection = cmds.ls(sl=True)
    if len(selection) == 1:
        charInit = selection
        cmds.Duplicate(charInit)
        cmds.select(clear = True)

def CreateCharHierarchyList(char):
    charList = cmds.listRelatives(char, children = True, allDescendents = True )
    return charList
    
def MatchNodesTransform():
    selection = cmds.ls(sl=True)
    if len(selection) == 2:
        nodeDupl = selection[0]
        nodeInit = selection[1]
        cmds.matchTransform(nodeDupl, nodeInit, position = True, rotation = True)

def GetMatchDepthInt():
	matchDepthInt = cmds.intField(matchDepthIntField, editable = True, query = True, value = True)
	return matchDepthInt

def GetFramestepInt():
	framestepInt = cmds.intField(framestepIntField, editable = True, query = True, value = True)
	return framestepInt
       
def Match2Hierarchies():
    charInit = cmds.ls("TOP_Avatar:Char")
    charDupl = cmds.ls("Char")
    charDuplList = CreateCharHierarchyList(charDupl)
    charInitList = CreateCharHierarchyList(charInit)
    #idxsToRemoveFromCharLists = [i for i, s in enumerate(charInitList) if "Constraint" in s]
    for node in charDuplList:
        if "Constraint" in node:
            charDuplList.remove(node)
    for node in charInitList:
        if "Constraint" in node:
            charInitList.remove(node)
    keyframeStart = int(cmds.playbackOptions(q=True,min=True))
    keyframeEnd = int(cmds.playbackOptions(q=True,max=True))
    keyframesList = []
    if cmds.checkBox(matchInCurrFrameCheckBox, query = True, value = True):
        currFrame = int(cmds.currentTime(query = True))
        keyframesList.extend( list(range(currFrame, currFrame + 2)) )
        framestep = 1
    else:
        keyframesList.extend( list(range(keyframeStart, keyframeEnd + 2)) )
        framestep = GetFramestepInt()
    matchDepth = GetMatchDepthInt()
    for frame in range(keyframesList[0], keyframesList[-1], framestep):
        cmds.currentTime(frame)
        for j in range(matchDepth):
            for i in range(len(charDuplList)):
                cmds.matchTransform(charDuplList[i], charInitList[i])
                cmds.setKeyframe(charDuplList[i], t = frame)
                
def Match2HierarchiesRec(rootNode):
    for child in cmds.listRelatives(rootNode, children = True) or []:
        Match2HierarchiesRec(child)
        childsListAll.append(child)
        print (childsListAll)
     
        
window = cmds.window( title="AnimationMatch", iconName='AM', widthHeight=(200, 150) )
cmds.columnLayout( adjustableColumn=True )
cmds.button( label = 'Duplicate Char', command = lambda *args: DuplicateChar() )
cmds.text('Enter match depth')
matchDepthIntField = cmds.intField(editable = True, value = 10)
cmds.text('Enter frame step')
framestepIntField = cmds.intField(editable = True, value = 1)
matchInCurrFrameCheckBox = cmds.checkBox( label = 'Match at current frame' )
cmds.button( label = 'Match Animation', command = lambda *args: Match2Hierarchies() )
cmds.button( label = 'Match AnimationRec', command = lambda *args: Match2HierarchiesRec(cmds.ls(sl=True)) )
cmds.setParent( '..' )
cmds.showWindow( window )