#替换模型
import maya.cmds as cmds 
selObj = cmds.ls(sl = True)
baseName = str(selObj[0])
changObj = selObj[1]
parentObj = cmds.listRelatives(selObj[0], parent= True)
cmds.delete(selObj[0])
Obj = cmds.rename(changObj, baseName)
cmds.parent(Obj, parentObj)
