import maya.cmds as cmds
selection = cmds.ls(sl=True)
posSelection1 = cmds.xform(selection[1], query=True, translation=True, worldSpace=True)
rotSelection1 = cmds.xform(selection[1], query=True, rotation=True, worldSpace=True)
cmds.xform(selection[0], translation = posSelection1, worldSpace=True)
cmds.xform(selection[0], rotation = rotSelection1, worldSpace=True)