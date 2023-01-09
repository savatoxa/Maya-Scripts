import maya.cmds as cmds
cmds.manipMoveContext('Move', e=True, mode=2)
cmds.manipRotateContext('Rotate', e=True, mode=1)
cmds.manipScaleContext('Scale', e=True, mode=2)