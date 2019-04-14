import maya.mel as mel
import maya.cmds as cmds

#给选择的骨骼创建控制器

def CreatFKCtr():
    cmds.undoInfo(openChunk=True)
    seljnt = cmds.ls(sl = True, type = "joint")

    if len(seljnt) == 0:
        print ("select nothing！")
    
    for i in range(0,len(seljnt)):
        print("")
        try:
            shape = cmds.circle(c=(0,0,0), nr = (1, 0, 0), sw = 360, r = 1, d = 3, ut = 0, tol = 0.00155, s = 8, ch = 0, n = seljnt[i] + "_Con")
            print seljnt[i] , shape[0]
            offset = cmds.group(shape[0], r = True, n = shape[0] + "offset")
            grp = cmds.group(offset, r = True, n = shape[0] + "Grp")
            Align(grp, seljnt[i] )
            cmds.parentConstraint(shape[0], seljnt[i])

            if i >= 1 and cmds.objExists(str(seljnt[i-1]) + "_Con"):
                Pctr = str(seljnt[i-1]) + "_Con"
                cmds.parent( grp, Pctr )

            print grp
        except Exception as e:
            print 'creatJntCtr something wrong...'
            cmds.undoInfo(closeChunk=True)


def Align(current, target):
    print "im in  Align"
    cmds.undoInfo(openChunk=True)
    try:
        targetPos = cmds.xform(target, q=True, ws=True, t=True)
        cmds.xform(current, ws=True, t=[targetPos[0],targetPos[1],targetPos[2]])
        targetRot = cmds.xform(target, q=True, ws=True, ro=True)
        cmds.xform(current, ws=True, ro=[targetRot[0],targetRot[1],targetRot[2]])
    except Exception as e:
        print 'Align something wrong...'
        cmds.undoInfo(closeChunk=True)

CreatFKCtr()