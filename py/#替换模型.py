#替换模型
import maya.cmds as cmds 

selObj = cmds.ls(sl = True)

Align(selObj[1], selObj[0])
baseName = str(selObj[0])
changObj = selObj[1]
parentObj = cmds.listRelatives(selObj[0], parent= True)
cmds.delete(selObj[0])
Obj = cmds.rename(changObj, baseName)
cmds.parent(Obj, parentObj)

def Align(current, target):
    targetPos = cmds.xform(target, q=True, ws=True, t=True)
    cmds.xform(current, ws=True, t=[targetPos[0],targetPos[1],targetPos[2]])
    targetRot = cmds.xform(target, q=True, ws=True, ro=True)
    cmds.xform(current, ws=True, ro=[targetRot[0],targetRot[1],targetRot[2]])