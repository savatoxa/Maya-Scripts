import maya.cmds as cmds
def countSelection(* args):
    return len(cmds.ls(sl = True))
cmds.headsUpDisplay( 'Count Selection', section=1, block=0, blockSize='medium', label='Num of selected objects', labelFontSize='large', command=countSelection, event='SelectionChanged' )