import maya.cmds as cmds


def DifOf2Vect3(vect1, vect2):
    vectRes = []
    for i in range(len(vect1)):
        vectRes.append(vect1[i] - vect2[i])
    return vectRes
    
def SumOf2Vect3(vect1, vect2):
    vectRes = []
    for i in range(len(vect1)):
        vectRes.append(vect1[i] + vect2[i])
    return vectRes

def BakeScaleNoOffsets(selection):
    scaleSelection1 = cmds.xform(selection[1], query=True, scale=True, worldSpace=True)
    cmds.xform(selection[0], scale = scaleSelection1, worldSpace=True)

def BakeNoOffssets(selection):
    posSelection1 = cmds.xform(selection[1], query=True, translation=True, worldSpace=True)
    rotSelection1 = cmds.xform(selection[1], query=True, rotation=True, worldSpace=True)
    cmds.xform(selection[0], translation = posSelection1, worldSpace=True)
    cmds.xform(selection[0], rotation = rotSelection1, worldSpace=True)
        
def BakeWithRotOffset(selection, rotOffset):
    posSelection1 = cmds.xform(selection[1], query=True, translation=True, worldSpace=True)
    rotSelection1 = cmds.xform(selection[1], query=True, rotation=True, worldSpace=True)
    rotSelection1WithOffset = SumOf2Vect3(rotSelection1, rotOffset)
    cmds.xform(selection[0], translation = posSelection1, worldSpace=True)
    cmds.xform(selection[0], rotation = rotSelection1WithOffset, worldSpace=True)
         
        
def BakeWithPosOffset(selection, posOffset):
    posSelection1 = cmds.xform(selection[1], query=True, translation=True, worldSpace=True)
    rotSelection1 = cmds.xform(selection[1], query=True, rotation=True, worldSpace=True)
    posSelection1WithOffset = SumOf2Vect3(posSelection1, posOffset)
    cmds.xform(selection[0], translation = posSelection1WithOffset, worldSpace=True)
    cmds.xform(selection[0], rotation = rotSelection1, worldSpace=True)
        
def BakeWithPosAndRotOffset(selection, posOffset, rotOffset):
    posSelection1 = cmds.xform(selection[1], query=True, translation=True, worldSpace=True)
    rotSelection1 = cmds.xform(selection[1], query=True, rotation=True, worldSpace=True)
    posSelection1WithOffset = SumOf2Vect3(posSelection1, posOffset)
    rotSelection1WithOffset = SumOf2Vect3(rotSelection1, rotOffset)
    cmds.xform(selection[0], translation = posSelection1WithOffset, worldSpace=True)
    cmds.xform(selection[0], rotation = rotSelection1WithOffset, worldSpace=True)

def GetFramestepInt():
	framestepInt = cmds.intField(framestepIntField, editable = True, query = True, value = True)
	return framestepInt

def BakeAnimation():
    selection = cmds.ls(sl=True)
    keyframeStart = int(cmds.playbackOptions(q=True,min=True))
    keyframeEnd = int(cmds.playbackOptions(q=True,max=True))
    keyframesList = []
    if cmds.checkBox(bakeInCurrFrameCheckBox, query = True, value = True):
        currFrame = int(cmds.currentTime(query = True))
        keyframesList.extend( list(range(currFrame, currFrame + 2)) )
        framestep = 1
    else:
        keyframesList.extend( list(range(keyframeStart, keyframeEnd + 1)) )
        framestep = GetFramestepInt()
    posOffsetCheckValue = cmds.checkBox(posOffsetCheckBox, query = True, value = True)
    rotOffsetCheckValue = cmds.checkBox(rotOffsetCheckBox, query = True, value = True)
    matchScaleCheckValue = cmds.checkBox(matchScaleCheckBox, query = True, value = True)
    if len(selection) == 2:
        cmds.currentTime(keyframesList[0])
        posSelection1 = cmds.xform(selection[1], query=True, translation=True, worldSpace=True)
        posSelection0 = cmds.xform(selection[0], query=True, translation=True, worldSpace=True)
        rotSelection1 = cmds.xform(selection[1], query=True, rotation=True, worldSpace=True)
        rotSelection0 = cmds.xform(selection[0], query=True, rotation=True, worldSpace=True)
        posOffset = DifOf2Vect3(posSelection0, posSelection1)
        rotOffset = DifOf2Vect3(rotSelection0, rotSelection1)
        for frame in range(keyframesList[0], keyframesList[-1], framestep):
            cmds.currentTime(frame)
            if matchScaleCheckValue:
                BakeScaleNoOffsets(selection)
            if posOffsetCheckValue:
                BakeWithPosOffset(selection, posOffset)
            if rotOffsetCheckValue:
                BakeWithRotOffset(selection, rotOffset)
            if posOffsetCheckValue and rotOffsetCheckValue:
                BakeWithPosAndRotOffset(selection, posOffset, rotOffset)
            if  not posOffsetCheckValue and not rotOffsetCheckValue:
                BakeNoOffssets(selection)
            cmds.setKeyframe(selection[0], t = frame)
        #cmds.select(selection[0])

window = cmds.window( title="AnimatedAllign", iconName='AAN', widthHeight=(200, 125) )
cmds.columnLayout( adjustableColumn=True )
cmds.button( label = 'Bake Animation', command = lambda *args: BakeAnimation() )
bakeInCurrFrameCheckBox = cmds.checkBox( label = 'Allign at current frame' )
cmds.text('Enter frames step')
framestepIntField = cmds.intField(editable = True, value = 1)
posOffsetCheckBox = cmds.checkBox( label = 'Keep Position Offset' )
rotOffsetCheckBox = cmds.checkBox( label = 'Keep Rotation Offset' )
matchScaleCheckBox = cmds.checkBox( label = 'Match Scale' )
cmds.setParent( '..' )
cmds.showWindow( window )