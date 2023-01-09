import maya.cmds as cmds
import pymel.core as pm
import maya.mel as mel

charJointsList = []

def DuplicateChar(selection):
    if len(selection) == 1:
        cmds.Duplicate(selection)
        
def DuplicateMesh(mesh):
    cmds.setAttr(mesh + '.visibility', 0)
    cmds.Duplicate(mesh)
    meshDupl = cmds.ls(sl = True)
    cmds.setAttr(meshDupl[0] + '.visibility', 1)
    
def CreateCharJointsListFullPath(char):
    del charJointsList[:]
    charJointsList.extend(char)
    charJointsList.extend(pm.listRelatives(char, children = True, allDescendents = True, fullPath = True))
    
def CreateCharJointsList(char):
    del charJointsList[:]
    charJointsList.extend(char)
    charJointsList.extend(pm.listRelatives(char, children = True, allDescendents = True))
    
def CreateCharJointsList(char):
    del charJointsList[:]
    charJointsList.extend(char)
          
def DeleteLeftPartOfChar(char):
    charForDelJointsList = []
    for joint_ in charJointsList:
        if (joint_[-len('Thigh'):] == 'Thigh' and 'L' in joint_) or ((joint_[-len('Clavicle'):] == 'Clavicle' or joint_[-len('Collarbone'):] == 'Collarbone') and 'L' in joint_):
            charForDelJointsList.append(joint_)
        if pm.objectType(joint_, isType = 'transform'):
            charForDelJointsList.append(joint_)
    for joint_ in charForDelJointsList:
        pm.delete(joint_)

def FindTrashString(char):
    charFirstChilds = cmds.listRelatives(char, children = True)
    if charFirstChilds:
        for joint_ in charFirstChilds:
            if 'Pelvis' in joint_:
                trashString = joint_[5:-6]
        print (trashString)
        return trashString

def GetTrashStringText():
	trashStringFromTxtField = cmds.textField(trashStringTxtField, editable = True, query = True, text = True)
	return trashStringFromTxtField
	
def GetInitialCharName():
    initialCharName = cmds.textField(initialCharNameTxtField, editable = True, query = True, text = True)
    return initialCharName
            
def RenameCharacter(char):
    trashString = GetTrashStringText()
    for joint_ in charJointsList:
        pm.rename(joint_, joint_.replace(GetInitialCharName(), 'Bip02').replace(trashString, ''))
    char = cmds.ls(sl = True)
    CreateCharJointsListFullPath(char)
    for joint_ in charJointsList:
        if joint_.find('Ribcage') == -1:
            pm.rename(joint_, joint_.replace('R', ''))
    CreateCharJointsList(char)

def SetIKLabels(char):
    CreateCharJointsList(char)
    cmds.setAttr(char[0] + '.type', 1)
    cmds.setAttr(char[0] + '.drawLabel', 1)
    cmds.setAttr('Bip02Ribcage' + '.type', 18)
    cmds.setAttr('Bip02Ribcage.otherType', 'Chest', type = "string")
    cmds.setAttr('Bip02Ribcage' + '.drawLabel', 1)
    if cmds.objExists('Bip02UpperArm'):
        cmds.setAttr('Bip02UpperArm' + '.type', 10)
        cmds.setAttr('Bip02UpperArm' + '.drawLabel', 1)
    if cmds.objExists('Bip02Upperarm'):
        cmds.setAttr('Bip02Upperarm' + '.type', 10)
        cmds.setAttr('Bip02Upperarm' + '.drawLabel', 1)
    if cmds.objExists('Bip02Hand'):
        cmds.setAttr('Bip02Hand' + '.type', 12)
        cmds.setAttr('Bip02Hand' + '.drawLabel', 1)
    if cmds.objExists('Bip02Palm'):
        cmds.setAttr('Bip02Palm' + '.type', 12)
        cmds.setAttr('Bip02Palm' + '.drawLabel', 1)
    cmds.setAttr('Bip02Thigh' + '.type', 2)
    cmds.setAttr('Bip02Thigh' + '.drawLabel', 1)
    cmds.setAttr('Bip02Foot' + '.type', 4)
    cmds.setAttr('Bip02Foot' + '.drawLabel', 1)
    
def PrepareSkelForAdvSkel(char):
    cmds.setAttr(char[0] + '.visibility', 0)
    DuplicateChar(char)
    charDupl = cmds.ls(sl = True)
    cmds.setAttr(charDupl[0] + '.visibility', 1)
    CreateCharJointsListFullPath(charDupl)
    DeleteLeftPartOfChar(charDupl)
    CreateCharJointsListFullPath(charDupl)
    RenameCharacter(charDupl)
    for joint_ in charJointsList:
        if cmds.objectType(joint_, isType = 'joint'):
            cmds.setAttr(joint_ + '.drawStyle', 0)
    SetIKLabels(cmds.ls(sl = True))


def GetJointsForSkin():
    jointsList = cmds.listRelatives('DeformationSystem', children = True, allDescendents = True )
    return jointsList
    
def GetJointsInSkinnedMesh(mesh):
    jointsListInSkinnedMesh = cmds.skinCluster(mesh[0], influence = True, query = True)
    skinCluster_ = mel.eval('findRelatedSkinCluster ' + mesh[0])
    return (skinCluster_, jointsListInSkinnedMesh)

def removeUnusedInfls(skinClust):
    allInfls = cmds.skinCluster(skinClust, query = True, influence = True)
    weightedInfls = cmds.skinCluster(skinClust, query = True, weightedInfluence = True)
    unusedInfls = [inf for inf in allInfls if inf not in weightedInfls]
    cmds.skinCluster(skinClust, edit = True, removeInfluence = unusedInfls)
    
def DuplicateMeshAndBindSkin(selMesh):
    DuplicateMesh(selMesh)
    duplMesh = cmds.ls(sl = True)
    cmds.skinCluster(duplMesh, GetJointsForSkin())
    sourceMeshSkinCluster = mel.eval('findRelatedSkinCluster ' + selMesh)
    destinationSkinCluster = mel.eval('findRelatedSkinCluster ' + duplMesh[0])
    cmds.copySkinWeights(sourceSkin = sourceMeshSkinCluster, destinationSkin = destinationSkinCluster, noMirror = True, surfaceAssociation =  'closestPoint', influenceAssociation = 'closestJoint')
    removeUnusedInfls(destinationSkinCluster)

def DuplicateMultMeshAndBindSkin(selMeshes):
    cmds.select(clear = True)
    for mesh in selMeshes:
        cmds.select(mesh)
        DuplicateMeshAndBindSkin(mesh)
        
def ReparentDummiesToNewSkel(char):
    CreateCharJointsListFullPath(char)
    dummiesParentsList = []
    for joint_ in charJointsList:
        if pm.objectType(joint_, isType = 'transform'):
            dummiesParentsList.append( (pm.listRelatives(joint_, allParents = True), joint_) )
    
           
window = cmds.window( title="Prepare character", iconName='PC', widthHeight=(200, 200) )
cmds.columnLayout( adjustableColumn=True )
cmds.text('Enter initial character name')
initialCharNameTxtField = cmds.textField(editable = True, text = '')
cmds.text('Enter trash substring')
trashStringTxtField = cmds.textField( editable = True, text = FindTrashString(cmds.ls('Bip01')) )
#cmds.button( label = 'Find trash string', command = lambda *args: FindTrashString(GetInitialCharName()) )
cmds.button( label = 'Create Fit Skeleton', command = lambda *args: PrepareSkelForAdvSkel(cmds.ls(sl = True)) )
cmds.button( label = 'Duplicate and skin meshes', command = lambda *args: DuplicateMultMeshAndBindSkin( cmds.ls(sl = True)) )
#cmds.button( label = 'Reparent Dummies To FitSkel', command = lambda *args: ReparentDummiesToNewSkel(cmds.ls(sl = True)) )
cmds.setParent( '..' )
cmds.showWindow( window )