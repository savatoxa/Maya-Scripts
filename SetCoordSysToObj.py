import maya.cmds as cmds
cmds.manipMoveContext('Move', e=True, mode=0)
cmds.manipRotateContext('Rotate', e=True, mode=0)
cmds.manipScaleContext('Scale', e=True, mode=0)