import maya.cmds as cmds
import maya.mel as mel
def Align(current, target):
    targetPos = cmds.xform(target, q=True, ws=True, t=True)
    cmds.xform(current, ws=True, t=[targetPos[0],targetPos[1],targetPos[2]])
    targetRot = cmds.xform(target, q=True, ws=True, ro=True)
    cmds.xform(current, ws=True, ro=[targetRot[0],targetRot[1],targetRot[2]])
def ChangeBSTarget(orgobj, curobj):
    #替换blendshape目标体
    
    OrgAttr = orgobj + ".worldMesh[0]"
    CurrentAttr = curobj + ".worldMesh[0]"

    if  not (cmds.objExists(OrgAttr) and cmds.objExists(CurrentAttr)):
        cmds.confirmDialog(t=u'敬告！！！', m=u'请选择两个模型，原bs + 现bs', b=[u'好的'], db=u'好的')
        return

    destination = cmds.connectionInfo(OrgAttr, destinationFromSource = True)
    if len(destination) >= 1 and cmds.objExists(destination[0]):
        cmds.disconnectAttr(OrgAttr, destination[0])
        cmds.connectAttr(CurrentAttr, destination[0])
    else:
        cmds.confirmDialog(t=u'敬告！！！', m=u'所选模型不是bsTarget' + destination[0], b=[u'好的'], db=u'好的')
        return
    
    Align(curobj, orgobj)
    baseName = str(orgobj)

    tempName = baseName.split("|")

    baseName = tempName[len(tempName) - 1]

    changObj = curobj
    parentObj = cmds.listRelatives(orgobj, parent= True)
    cmds.delete(orgobj)
    Obj = cmds.rename(changObj, baseName)
    cmds.parent(Obj, parentObj)

obj = cmds.ls(sl = True)
org = cmds.listRelatives(obj[0], children = True)
#cur =  cmds.listRelatives(obj[1], children = True)
for i in org:
    cur = "pasted__" + i
    if cmds.objExists(cur):
        ChangeBSTarget(i, cur)
        
