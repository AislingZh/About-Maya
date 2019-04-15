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
        object.__init__(self)
        # self.inputCurve =  cmds.ls(sl = True)
        # self.JntNUm = 10

    
    def BuildAutoRig(self, inputCurve, CtrlNum, JntNUm):

        #根据曲线和设定的骨骼数创建骨骼，并复制两份出来
        skinJntChain = self.CreatJntChin(inputCurve, JntNUm)
        IKJntChain = cmds.duplicate(skinJntChain, rr = True)
        self.ReName(IKJntChain, inputCurve + "_IKJnt")
        ikTfkJnt = cmds.duplicate(skinJntChain, rr = True)
        self.ReName(IKJntChain, inputCurve + "_ikTfkJnt")

        #使用已有的曲线ikCurve给骨骼链做ik链
        IKs = self.CreakIk(jntChin, inputCurve) 

        self.CreatIKCtrlSys(inputCurve, JntNUm/5)

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

    def CreatJntChain(self, inputCurve = cmds.ls(sl = True), JntNum = 10, orientation = 'xyz'):
        
        JntChain = []


        #根据曲线等间距创建骨骼
        loc = cmds.spaceLocator(p = (0,0,0))
        motionpath = cmds.pathAnimation(loc[0], inputCurve)
        cmds.setAttr(motionpath+".fractionMode", True)
        sdf = cmds.connectionInfo(motionpath + '.uValue', sourceFromDestination = True)
        cmds.disconnectAttr(sdf, motionpath + '.uValue')
        for i in range(0,JntNum,1):
            cmds.select(cl = True)
            cmds.setAttr(motionpath + '.uValue', i*1.0/JntNum)
            pos = cmds.xform(loc[0], q = True, ws = True, piv = True)
            jnt = cmds.joint(p = (pos[0], pos[1], pos[2]), n = inputCurve + '_SKinJnt' + str(i))
            JntChain.append(jnt)

        #设置目标约束的两个向量，Y向上
        aimDict = {}
        aimDict[orientation[0]] = 1
        aimDict[orientation[1]] = 0
        aimDict[orientation[2]] = 0
        aimVec = ( aimDict['x'], aimDict['y'], aimDict['z'] )

        orientDict = {}
        orientDict[orientation[0]] = 0
        orientDict[orientation[1]] = 0
        orientDict[orientation[2]] = 1
        orientVec = ( orientDict['x'], orientDict['y'], orientDict['z'] )

        #旋转第一根骨骼的方向
        aimCons = cmds.aimConstraint(JntChain[1], JntChain[0], aimVector = aimVec, upVector = (0,1,0), worldUpType = "scene")
        cmds.delete(aimCons)
        rotf = cmds.getAttr(JntChain[0] + '.rotate')[0]
        cmds.setAttr(JntChain[0] + '.jointOrient', rotf[0], rotf[1], rotf[2], type = "float3")
        cmds.setAttr(JntChain[0] + '.rotate', 0,0,0, type = "float3")

        #旋转中间骨骼的方向
        for i in range(1, JntNum - 1):
            aimCons = cmds.aimConstraint(JntChain[i + 1], JntChain[i], aimVector = aimVec, upVector = orientVec, worldUpType = "objectrotation", worldUpVector = orientVec, worldUpObject = JntChain[i-1] )
            cmds.delete(aimCons)
            rotm = cmds.getAttr(JntChain[i] + '.rotate')[0]
            cmds.setAttr(JntChain[i] + '.jointOrient', rotm[0], rotm[1], rotm[2], type = "float3")
            cmds.setAttr(JntChain[i] + '.rotate', 0,0,0, type = "float3")

        #旋转最后骨骼的方向
        rotl = cmds.getAttr(JntChain[JntNum - 2] + '.jointOrient')[0]
        cmds.setAttr(JntChain[JntNum - 1] + '.jointOrient', rotl[0], rotl[1], rotl[2], type = "float3")

        for i in range(1, jntNum):
            cmds.parent(JntChain[i], JntChain[i - 1], absolute = True)

        print('created and oriented Jnt Chain')
        cmds.select(JntChain[0])

        return JntChain

    def ReName(self, Obj, Name):
        j = 0
        for i in Obj:
            cmds.rename(i, Name + str(j))
            j = j + 1

    
    
    def CreatIKCtrlSys(self, inputCurve,ikCtrlNum):
        #给曲线创建簇控制点，并为簇点创建控制器
        #蒙皮骨骼约束ik控制器，使其能跟随运动
        #控制器的位置，需要从根部到尾部逐渐变密集 ？？？ 能否实现