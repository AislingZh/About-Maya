######## Tentacle AutoRigger ########
#	Version 1.00
# 	Version: 15.04.2019
# 	Author: AislingChow
#	融合了variable FK 、IK、非线性变形变形器、头发动力学的多种控制，以满足触角既柔软又有力的运动状态
#  
#
########################################
#根据选择的曲线创建骨骼及控制器，骨骼数量+控制器数量可选
#

import maya.cmds as cmds

class TentacleAutoRig(object):

    def __init__(self):
        print "autoRig"
    
    def BuildAutoRig(self, inputCurve, CtrlNum, JntNUm):
        ikCurve = self.ReBuildCure(inputCurve, JntNUm) #按照骨骼数重建曲线，使曲线有相同的CV点，？？是否必要？？ --->创建骨骼链

        jntChin = self.CreatJntChin(inputCurve, JntNUm)

        IKs = self.CreakIk(jntChin, ikCurve) #使用已有的曲线ikCurve给骨骼链做ik链

        self.CreatIKCtrlSys(ikCurve, JntNUm/5)

        curves = cmds.duplicate(inputCurve, 2) #把曲线复制出3份出来，分别用于ik控制器，非线性变形器，头发动力学系统
        
        self.CreatHairDyn(curves[1])
        self.CreatDeform(curves[2])

        cmds.blendShape(curves, inputCurve) #对曲线做bs，并以inputCurve

        ikTfkJnt = cmds.duplicate(jntChin) #复制骨骼链出来，作为ikfk链接的中间骨骼

        j = 0
        for i in jntChin:

            alignCons = cmds.parentConstraint(i, ikTfkJnt[i], mo = True)
            j = j+1

         fkJnt = cmds.duplicate(jntChin) #复制骨骼链出来蒙皮骨骼

         self.CreatVarFK(fkJnt, CtrlNum)

    def CreatIKCtrlSys(self, inputCurve,ikCtrlNum):
        #给曲线创建簇控制点，并为簇点创建控制器
        #蒙皮骨骼约束ik控制器，使其能跟随运动
        #控制器的位置，需要从根部到尾部逐渐变密集 ？？？ 能否实现