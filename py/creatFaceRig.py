import maya.cmds as cmds

#creat contrl for joint
def creatCtr(jnt):
    shape = cmds.circle(c=(0,0,0), nr = (1, 0, 0), sw = 360, r = 1, d = 3, ut = 0, tol = 0.00155, s = 8, ch = 0, n = jnt + "Con")
    drv = cmds.group(shape[0], r = True, n = shape[0] + "_DRV")
    cts = cmds.group(drv, r = True, n = shape[0] + "_CST")
    grp = cmds.group(cts, r = True, n = shape[0] + "_GRP")
    Align(grp, jnt)
    cmds.parentConstraint(shape, jnt, mo = True)


def Align(current, target):
    targetPos = cmds.xform(target, q=True, ws=True, t=True)
    cmds.xform(current, ws=True, t=[targetPos[0],targetPos[1],targetPos[2]])
    targetRot = cmds.xform(target, q=True, ws=True, ro=True)
    cmds.xform(current, ws=True, ro=[targetRot[0],targetRot[1],targetRot[2]])

selLoc = cmds.ls(sl = True)
grpjnt = cmds.group( em = True, n = "jntGrp")

for i in selLoc:
    cmds.select(cl = True)
    pos = cmds.getAttr(i + '.translate')
    jnt = cmds.joint(n = i + '_jnt', p = pos[0])
    cmds.parent(jnt, grpjnt)
    
    if "_L_" in str(i):
        mjnt = cmds.mirrorJoint(jnt, mirrorYZ=True,searchReplace=('L', 'R') )
        creatCtr(mjnt[0])
    creatCtr(jnt)
