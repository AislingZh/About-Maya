import maya.mel as mel
import maya.cmds as cmds

obj = "Knee_R"
parentObj = "Hip_R"

if not cmds.objExists("locator1"):
    locPos = cmds.spaceLocator(n = "locator1")
ponA = cmds.parentConstraint( obj, "locator1", mo = False)
cmds.bakeResults( "locator1", simulation=True, t = (0, 40), hierarchy= "below",  sb = 1, dic = True, pok = True, ral = False, rwl = False, cp = True)
cmds.delete(ponA)
keyframelist = cmds.ls(type='animCurveTL')+cmds.ls(type='animCurveTA')+cmds.ls(type='animCurveTU')
for i in keyframelist:
    if not (obj not in i):
        cmds.delete(i)
cmds.parent( obj, parentObj )
ponB = cmds.parentConstraint( 'locator1', obj, mo = True)
cmds.bakeResults( obj, simulation=True, t = (0, 40), hierarchy= "below",  sb = 1, dic = True, pok = True, ral = False, rwl = False, cp = True)
cmds.delete(ponB)