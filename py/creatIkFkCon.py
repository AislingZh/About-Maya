#选择所有骨骼
#给骨骼建立控制器并打组
#排列组的位置
#建立父子关系并做约束

import maya.cmds as cmds
import maya.mel as mel
class CreatIkFkCon():
    """docstring for CreatIkFkCon"""
       
    def creatCtr(self):
        BaseJnt = cmds.ls(sl = True, type = "joint")
        childJnt = cmds.listRelatives(BaseJnt, allDescendents = True, type = "joint")
        childJnt.reverse()
        selJnt = BaseJnt +  childJnt
        # posGrp = []
        # Grp = []
        con = [None] * len(selJnt)
        for i in range(0, len(selJnt)):
            shape = cmds.circle(c=(0,0,0), nr = (1, 0, 0), sw = 360, r = 1, d = 3, ut = 0, tol = 0.00155, s = 8, ch = 0, n = selJnt[i] + "Con")
            con[i] = shape[0]
            grp = cmds.group(con[i], r = True, n = con[i] + "_Grp")

            if i >= 1:
                posgrp = cmds.group(grp, r = True, n = grp + "_ro", p = posgrp)
                self.Align(posgrp, selJnt[i-1])
            else:
                posgrp = cmds.group(grp, r = True, n = grp + "_ro")
                self.Align(posgrp, selJnt[i])
            
            self.Align(grp, selJnt[i])
            cmds.parent(selJnt[i], con[i])
            if i >=1:
                cmds.orientConstraint(con[i-1], posgrp, mo = True, w = 1)


        self.zeroAllAttr(BaseJnt[0] + "_Grp_ro")
        



    def Align(self, current, target):
        targetPos = cmds.xform(target, q=True, ws=True, t=True)
        cmds.xform(current, ws=True, t=[targetPos[0],targetPos[1],targetPos[2]])
        targetRot = cmds.xform(target, q=True, ws=True, ro=True)
        cmds.xform(current, ws=True, ro=[targetRot[0],targetRot[1],targetRot[2]])
    
    def zeroAllAttr(self, mysl):
        cmds.undoInfo(openChunk=True)
        try:
            atname1 = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz']
            atname2 = ['sx', 'sy', 'sz', 'v']
            for i in mysl:
                for ii in atname1:
                    if not cmds.getAttr(i+'.'+ii, lock=True):
                        cmds.setAttr(i+'.'+ii, 0)
                for ii in atname2:
                    if not cmds.getAttr(i+'.'+ii, lock=True):
                        cmds.setAttr(i+'.'+ii, 1)
            print 'Zero All The Attr...'
        except:
            print 'something wrong…'
            cmds.undoInfo(closeChunk=True)
        cmds.undoInfo(closeChunk=True)

CreatIkFkCon().creatCtr()