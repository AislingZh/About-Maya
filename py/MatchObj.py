import maya.mel as mel
import maya.cmds as cmds
#在模型的质心处建立骨骼

def DoMatch():
    selObj = cmds.ls(sl = True)

    if len(seljnt) == 0:
        print ("select nothing！")

    for obj in selObj:
        
        cube = cmds.polyCube( sx=1, sy=1, sz=1, h=1 )

        cmds.matchTransform(cube,obj)

        jnt = cmds.joint()

        Align(jnt, cube)



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

DoMatch()