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
    
def CreateCharJointsList(char):
    del charJointsList[:]
    charJointsList.extend(char)
    charJointsList.extend(pm.listRelatives(char, children = True, allDescendents = True, fullPath = True))
          
def DeleteLeftPartOfChar(char):
    CreateCharJointsList(char)
    charForDelJointsList = []
    for joint_ in charJointsList:
        if (joint_[-len('Thigh'):] == 'Thigh' and 'L' in joint_) or (joint_[-len('Clavicle'):] == 'Clavicle' and 'L' in joint_):
            charForDelJointsList.append(joint_)
    for joint_ in charForDelJointsList:
        pm.delete(joint_)

def FindTrashString(char):
    charFirstChilds = cmds.listRelatives(char, children = True)
    for joint_ in charFirstChilds:
        if 'Pelvis' in joint_:
            trashString = joint_[5:-6]
    return trashString

def GetTrashStringText():
	trashStringFromTxtField = cmds.textField(trashStringTxtField, editable = True, query = True, text = True)
	return trashStringFromTxtField
            
def RenameCharacter(char):
    CreateCharJointsList(char)
    trashString = GetTrashStringText()
    for joint_ in charJointsList:
        pm.rename(joint_, joint_.replace('Bip01', 'Bip02').replace(trashString, ''))
        if joint_.find('Ribcage') == -1:
            pm.rename(joint_, joint_.replace('R', ''))
    
def SetIKLabels(char):
    CreateCharJointsList(char)
    cmds.setAttr(char[0] + '.type', 1)
    cmds.setAttr(char[0] + '.drawLabel', 1)
    cmds.setAttr('Bip02Ribcage' + '.type', 18)
    cmds.setAttr('Bip02Ribcage.otherType', 'Chest', type = "string")
    cmds.setAttr('Bip02Ribcage' + '.drawLabel', 1)
    cmds.setAttr('Bip02UpperArm' + '.type', 10)
    cmds.setAttr('Bip02UpperArm' + '.drawLabel', 1)
    cmds.setAttr('Bip02Hand' + '.type', 12)
    cmds.setAttr('Bip02Hand' + '.drawLabel', 1)
    cmds.setAttr('Bip02Thigh' + '.type', 2)
    cmds.setAttr('Bip02Thigh' + '.drawLabel', 1)
    cmds.setAttr('Bip02Foot' + '.type', 4)
    cmds.setAttr('Bip02Foot' + '.drawLabel', 1)
    
def PrepareSkelForAdvSkel(char):
    cmds.setAttr(char[0] + '.visibility', 0)
    DuplicateChar(char)
    char = cmds.ls(sl = True)
    cmds.setAttr(char[0] + '.visibility', 1)
    DeleteLeftPartOfChar(char)
    RenameCharacter(char)
    CreateCharJointsList(char)
    for joint_ in charJointsList:
        cmds.setAttr(joint_ + '.drawStyle', 0)
    SetIKLabels(char)

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

window = cmds.window( title="Prepare character", iconName='PC', widthHeight=(200, 100) )
cmds.columnLayout( adjustableColumn=True )
cmds.text('Enter trash substring')
trashStringTxtField = cmds.textField(editable = True, text = FindTrashString(cmds.ls('Bip01')))
cmds.button( label = 'Create Fit Skeleton', command = lambda *args: PrepareSkelForAdvSkel(cmds.ls(sl = True)) )
cmds.button( label = 'Duplicate and skin meshes', command = lambda *args: DuplicateMultMeshAndBindSkin( cmds.ls(sl = True)) )
cmds.setParent( '..' )
cmds.showWindow( window )