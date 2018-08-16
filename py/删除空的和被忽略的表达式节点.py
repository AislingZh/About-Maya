#删除空的和被忽略的表达式节点
import maya.cmds as mc
selList = mc.ls(type = "script")
for i in selList:
    ire = mc.getAttr( i + ".ignoreReferenceEdits")
    asAttr = mc.getAttr(i + ".after")
    bsAttr = mc.getAttr(i + ".before")
    if ire == 1:
        mc.delete(i)
    elif asAttr == None and bsAttr == None :
        mc.delete(i)