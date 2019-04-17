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
        
        IKJntChain = cmds.duplicate(skinJntChain, name = InputCurve + '_ikJnt', parentOnly = True)
        ikTfkJnt = cmds.duplicate(skinJntChain, name = InputCurve + '_ikTfkJnt', parentOnly = True)

        #创建定位用的面片并蒙皮
        guideSurface = self.CreatGuideSurface(inputCurve, skinJntChain)
        cmds.skinCluster( guideSurface, skinJntChain, tsb=True, skinMethod = 0, maximumInfluences = 1, dropoffRate = 10.0 )

        #给骨骼添加位置属性,标识在面片上的位置
        self.AddPosOnSurfaceAttr(skinJntChain, JntNUm)
        varFKCtrl = self.CreatVarFkCtrl(inputCurve, CtrlNum, guideSurface)

        #使用已有的曲线ikCurve给骨骼链做ik链
        ikSolvers = cmds.ikHandle(name=IKJntChain + '_IKHandle', sj=IKJntChain[0], ee=IKJntChain[JntNUm - 1], curve = inputCurve, sol='ikSplineSolver',ccv = True)

        ikCurve = ikSolvers[2]

        self.CreakIkCtrl(IKJntChain, ikCurve, CtrlNum) #制作方案待定。。。。。

        #复制曲线制作hair动力学系统
        DynCurveOrg = cmds.duplicate(inputCurve)
        DynObjects = self.CreatDynSys(DynCurveOrg) 

        #复制曲线制作非线性变形器效果
        deformCurve = cmds.duplicate(inputCurve, name = InputCurve + '_deformCurve')
        deformGrps = self.CreatDeform(deformCurve,skinJntChain[0])
        deformCtrlGrp = deformGrps[0]
        deformHandleGrp = deformGrps[1]

        curves = cmds.duplicate(inputCurve, 2) #把曲线复制出3份出来，分别用于ik控制器，非线性变形器，头发动力学系统
        
        self.CreatHairDyn(curves[1])

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

        for i in range(1, JntNum):
            cmds.parent(JntChain[i], JntChain[i - 1], absolute = True)

        print('created and oriented Jnt Chain')
        cmds.select(JntChain[0])

        return JntChain

    def CreatGuideSurface(self, InputCurve, JntChain):
        #用骨骼定位，先创建两条曲线，再根据曲线创建面片
        loftCurves = []
        for i in range(2):
            listOffsetJnts = cmds.duplicate(JntChain, rr = True, name = 'b' + InputCurve + '_offset', parentOnly = True)

            for jnt in listOffsetJnts:
                if i == 0:
                    cmds.move(0,0,-0.5, jnt, relative = True, objectSpace = True, preserveChildPosition = True)
                if i == 1:
                    cmds.move(0,0,0.5, jnt, relative = True, objectSpace = True, preserveChildPosition = True)
                
            loftCurvePoints = []

            for each in listOffsetJnts:
                jntPos = cmds.xform(each, q = True, t = True, ws = True)
                loftCurvePoints.append(jntPos)
            
            loftcurve = cmds.curve(name = InputCurve + '_loftCurve' + str(i), degree = 1, point = loftCurvePoints)
            loftCurves.append(loftcurve)
            cmds.delete(listOffsetJnts)
        #创建surface面片
        guideSurface = cmds.loft(loftCurves[0], loftCurves[1], name = InputCurve + '_gude_surface', ar=True, rsn=True, d=3, ss=1, object=True, ch=False, polygon=0 )
        guideSurface = cmds.rebuildSurface( guideSurface ,ch=1, rpo=1, rt=0, end=1, kr=1, kcp=0, kc=0, su=0, du=3, sv=1, dv=3, tol=0.01, fr=0, dir=2 )
        #清理掉不用的文件
        cmds.delete(loftCurves)
        cmds.setAttr(guideSurface[0] + ".inheritsTransform", False)
        cmds.setAttr(guideSurface[0] + ".overrideEnabled", True)
        cmds.setAttr(guideSurface[0] + ".overrideDisplayType", 1)

        return guideSurface


    def AddPosOnSurfaceAttr(self, jntChain, JntNUm):
        
        i = 0
        for jnt in jntChain:
            cmds.addAttr( jnt, longName = 'jointPosition', attributeType = 'float', keyable = True )
            cmds.setAttr( jnt + '.jointPosition', i*1.0/(len(JntChain) - 1), lock = True)
            i = i +1
        
    
    def CreatVarFkCtrl(self, ctrName, num, surf):
        ctrlGrp = cmds.group( name = ctrName + '_VFkCtrls', empty = True, world = True)
        cmds.setAttr(ctrlGrp + ".inheritsTransform ", 0)
        listOfCtrls = []

        for i in range(num):
            if num > 1:
                FolliclePos = (1.0/(num - 1)) * i
            else:
                FolliclePos = (1.0/num) * i
            
            #创建loc做控制器，并清理和添加一些属性
            currentCtrl = cmds.circle( name = ( 'ctrl_vFK' + str( i+1 )+ '_' + ctrName ), c=(0,0,0), nr=(1,0,0), sw=360, r=1.5, d=3, ut=0, tol=0.01, s=8, ch=False)
            
            cmds.setAttr(currentCtrl[0] + ".overrideEnabled", True)
            cmds.setAttr(currentCtrl[0] + ".overrideColor", 4)
            cmds.setAttr(currentCtrl[0] + ".translateX", lock = True, keyable = False, channelBox = False)
            cmds.setAttr(currentCtrl[0] + ".translateY", lock = True, keyable = False, channelBox = False)
            cmds.setAttr(currentCtrl[0] + ".translateZ", lock = True, keyable = False, channelBox = False)
            cmds.setAttr(currentCtrl[0] + ".scaleX", lock = True)

            cmds.addAttr( longName='rotateStrength', attributeType='float', keyable=True, defaultValue=1)
            cmds.addAttr( longName='position', attributeType='float', keyable=True, min=0-FolliclePos, max=1-FolliclePos )
            cmds.addAttr( longName='radius', attributeType='float', keyable=True, min=0.0001, defaultValue=0.3 )

            #创建毛囊
            currentFollicle = self.create_follicle(surf[0], uPos=FolliclePos, vPos=0.5)
            cmds.setAttr(currentFollicle + ".simulationMethod", 0)
            cmds.setAttr(currentFollicle + ".collide", 0)
            cmds.setAttr(currentFollicle + ".flipDirection", True)
            currentFollicleTran = cmds.listRelatives(currentFollicle, parent = True)[0]

            #设置旋转强度属性
            rotStrengthMul = cmds.shadingNode( 'multiplyDivide', asUtility = True, n = str( currentCtrl[0] ) + "_strength_mult" )
            cmds.connectAttr(currentCtrl[0] + ".rotate", rotStrengthMul + ".input1")
            cmds.connectAttr(currentCtrl[0] + ".rotateStrength", rotStrengthMul + ".input2X", f = True)
            cmds.connectAttr(currentCtrl[0] + ".rotateStrength", rotStrengthMul + ".input2Y", f = True)
            cmds.connectAttr(currentCtrl[0] + ".rotateStrength", rotStrengthMul + ".input2Z", f = True)

            #设置控制器位置属性
            jntPosPlus = cmds.shadingNode( 'plusMinusAverage', asUtility = True, n=currentCtrl[0] + '_jntposZeroCompensate' )
            FolloclePos = cmds.getAttr(currentFollicle + ".parameterU")
            cmds.setAttr(jntPosPlus + ".input1D[0]", FolloclePos)
            cmds.connectAttr(currentCtrl[0] + '.position', jntPosPlus + '.input1D[1]', f=True )
            cmds.connectAttr(jntPosPlus + '.output1D', currentFollicle + ".parameterU", f=True )

            #给控制器设置层级
            offsetGrp = cmds.group(em = True, n = currentCtrl + "_Offset")
            self.Align(offsetGrp, currentCtrl)
            cmds.parent(currentCtrl, offsetGrp)
            followGrp = cmds.group(currentCtrl, n = currentCtrl + "_follow")

            cmds.connectAttr(currentFollicleTran + ".translate", followGrp + ".translate")
            cmds.parent(offsetGrp, ctrlGrp)

            listOfCtrls.append(currentCtrl[0])
            cmds.select(clear = True)

        return listOfCtrls


    def Align(self, current, target):
        #current：当前的位置，target：要对齐的目标位置
        targetPos = cmds.xform(target, q=True, ws=True, t=True)
        cmds.xform(current, ws=True, t=[targetPos[0],targetPos[1],targetPos[2]])
        targetRot = cmds.xform(target, q=True, ws=True, ro=True)
        cmds.xform(current, ws=True, ro=[targetRot[0],targetRot[1],targetRot[2]])


    def create_follicle(self, nurbs, uPos, vPos):
        if cmds.objectType( nurbs, isType='transform' ):
            nurbs = cmds.listRelatives(nurbs, s = True)
        elif cmds.objectType( nurbs, isType='nurbsSurface'):
            pass
        else:
            return False
        
        #创建毛囊节点
        follicleNode = cmds.createNode('follicle', name=nurbs + "_follicle")
        cmds.connectAttr(nurbs + '.local',  follicleNode + '.inputSurface')
        follicleTran = cmds.listRelatives(follicleNode, parent = True)[0]

        #链接毛囊节点与面片
        cmds.connectAttr(nurbs + '.worldMatrix[0]',  follicleNode + '.inputWorldMatrix')
        cmds.connectAttr(follicleNode + '.outRotate',  follicleTran + '.rotate')
        cmds.connectAttr(follicleNode + '.outTranslate',  follicleTran + '.translate')
        cmds.setAttr(follicleNode + '.parameterU', uPos)
        cmds.setAttr(follicleNode + '.parameterV', vPos)
        cmds.setAttr(follicleTran + '.rotate', lock = True)
        cmds.setAttr(follicleTran + '.rotate', lock = True)

        return follicleNode


    def CreatDeform(self, dynCurve, jnt):
        
        deformGrps = []

        #创建变形器，sin和 squash 

        sineDefs = cmds.nonLinear(dynCurve, type='sine', name = dynCurve + "_sine" )
        squashDefs = cmds.nonLinear(dynCurve, type='squash', lowBound = -2, highBound = 0, name = dynCurve + "_squash" )
        self.Align(squashDefs[1], jnt)

        #创建变形器的控制器，整理并添加属性，并链接属性
        deformCtrl = cmds.spaceLocator(p = (0,0,0), n = jnt.split("_", 1)[0] + "_demform_ctrl")[0]
        
        cmds.transformLimits(deformCtrl, tx = (0,1), etx=(True, False))
        cmds.setAttr(deformCtrl + ".translateY", lock = True, keyable = False, channelBox = False)
        cmds.setAttr(deformCtrl + ".translateZ", lock = True, keyable = False, channelBox = False)
        cmds.setAttr(deformCtrl + ".scaleX", lock = True, keyable = False, channelBox = False)
        cmds.setAttr(deformCtrl + ".scaleY", lock = True, keyable = False, channelBox = False)
        cmds.setAttr(deformCtrl + ".scaleZ", lock = True, keyable = False, channelBox = False)
        cmds.setAttr(deformCtrl + ".rotateX", lock = True, keyable = False, channelBox = False)
        cmds.setAttr(deformCtrl + ".rotateY", lock = True, keyable = False, channelBox = False)
        cmds.setAttr(deformCtrl + ".rotateZ", lock = True, keyable = False, channelBox = False)

        cmds.addAttr( longName='deform_switch', attributeType='float', keyable=True, min=0, max=1 )
        cmds.addAttr( longName='amplitude', attributeType='float', keyable=True, min=-20, max=20, defaultValue = 1 )
        cmds.addAttr( longName='wavelength', attributeType='float', keyable=True, min=1, max =10 , defaultValue = 5)
        cmds.addAttr( longName='offset', attributeType='float', keyable=True, min=-10, max=10)
        cmds.addAttr( longName='dropoff', attributeType='float', keyable=True, min=-10, max=10, defaultValue = 10)

        cmds.addAttr( longName='factor', attributeType='float', keyable=True, min=-20, max=20 )
        cmds.addAttr( longName='expand', attributeType='float', keyable=True, min=0, max=10)
        cmds.addAttr( longName='maxExpandPos', attributeType='float', keyable=True, min=0.1, max=9.9, defaultValue = 1)
        cmds.addAttr( longName='startSmooth', attributeType='float', keyable=True, min=0, max=1 )
        cmds.addAttr( longName='endSmooth', attributeType='float', keyable=True, min=0, max=1)


        followGrp = cmds.group(deformCtrl, n = deformCtrl + "_follow")
        offsetGrp = cmds.group(followGrp, n = deformCtrl + "_Offset")
        deformGrps.append(offsetGrp)
        self.Align(offsetGrp, jnt)
        tranY = cmds.getAttr(offsetGrp + ".translateY")
        cmds.setAttr(offsetGrp + ".translateY", tranY + 5)

        #修改handle的旋转方向，使其能和曲线同向，+1--->-1
        jntOri = cmds.getAttr(jnt + ".jointOrientY")
        o = abs(jntOri)%360 /90 
        if o == 0 :
            cmds.setAttr(sineDefs[1] + ".rotateZ", 90)
            cmds.setAttr(squashDefs[1] + ".rotateZ", 90)
        elif 0 == 1 :
            cmds.setAttr(sineDefs[1] + ".rotateX", -90)
            cmds.setAttr(squashDefs[1] + ".rotateX", -90)
        elif 0 == 2 :
            cmds.setAttr(sineDefs[1] + ".rotateZ", -90)
            cmds.setAttr(squashDefs[1] + ".rotateZ", -90)
        elif 0 == 3 :
            cmds.setAttr(sineDefs[1] + ".rotateX", 90)
            cmds.setAttr(squashDefs[1] + ".rotateX", 90)
        
        #链接控制器和变形器的属性
        squashRange = cmds.shadingNode("setRange", asUtility = True, name = sineDefs[0] + "_squash_setRange")

        cmds.connectAttr(deformCtrl + ".factor", squashRange + ".valueX" )
        cmds.setAttr(squashRange + ".minX", -2)
        cmds.setAttr(squashRange + ".maxX", 2)
        cmds.setAttr(squashRange + ".oldMinX", -20)
        cmds.setAttr(squashRange + ".oldMaxX", 20)
        cmds.connectAttr(squashRange + ".outValueX", squashDefs[0] + ".factor" )

        cmds.connectAttr(deformCtrl + ".expand", squashRange + ".valueY" )
        cmds.setAttr(squashRange + ".minY", 0)
        cmds.setAttr(squashRange + ".maxY", 1)
        cmds.setAttr(squashRange + ".oldMinY", 0)
        cmds.setAttr(squashRange + ".oldMaxY", 10)
        cmds.connectAttr(squashRange + ".outValueY", squashDefs[0] + ".expand" )

        cmds.connectAttr(deformCtrl + ".maxExpandPos", squashRange + ".valueZ" )
        cmds.setAttr(squashRange + ".minZ", 0.01)
        cmds.setAttr(squashRange + ".maxZ", 0.99)
        cmds.setAttr(squashRange + ".oldMinZ", 0.1)
        cmds.setAttr(squashRange + ".oldMaxZ", 10)
        cmds.connectAttr(squashRange + ".outValueZ", squashDefs[0] + ".maxExpandPos" )

        cmds.connectAttr(deformCtrl + ".startSmooth", squashDefs[0] + ".startSmoothness" )
        cmds.connectAttr(deformCtrl + ".endSmooth", squashDefs[0] + ".endSmoothness" )


        sineRange = cmds.shadingNode("setRange", asUtility = True, name = sineDefs[0] + "_sine_setRange")

        cmds.connectAttr(deformCtrl + ".amplitude", sineRange + ".valueX" )
        cmds.setAttr(sineRange + ".minX", -5)
        cmds.setAttr(sineRange + ".maxX", 5)
        cmds.setAttr(sineRange + ".oldMinX", -20)
        cmds.setAttr(sineRange + ".oldMaxX", 20)
        cmds.connectAttr(sineRange + ".outValueX", sineDefs[0] + ".amplitude" )

        cmds.connectAttr(deformCtrl + ".wavelength", sineRange + ".valueY" )
        cmds.setAttr(sineRange + ".minY", 1)
        cmds.setAttr(sineRange + ".maxY", 10)
        cmds.setAttr(sineRange + ".oldMinY", 1)
        cmds.setAttr(sineRange + ".oldMaxY", 10)
        cmds.connectAttr(sineRange + ".outValueY", sineDefs[0] + ".wavelength" )

        cmds.connectAttr(deformCtrl + ".offset", sineDefs[0] + ".offset" )

        cmds.connectAttr(deformCtrl + ".dropoff", sineRange + ".valueZ" )
        cmds.setAttr(sineRange + ".minZ", -1)
        cmds.setAttr(sineRange + ".maxZ", 1)
        cmds.setAttr(sineRange + ".oldMinZ", -10)
        cmds.setAttr(sineRange + ".oldMaxZ", 10)
        cmds.connectAttr(sineRange + ".outValueZ", sineDefs[0] + ".dropoff" )

        cmds.pointConstraint(deformCtrl, squashDefs[1], mo = True)
        cmds.pointConstraint(deformCtrl, sineDefs[1], mo = True)

        deformGrp = cmds.group(squashDefs[1],sineDefs[1], n = dynCurve + "deform_Grp")
        deformGrps.append(offsetGrp)

        return offsetGrp


    # def ReName(self, Obj, Name):
    #     j = 0
    #     for i in Obj:
    #         cmds.rename(i, Name + str(j))
    #         j = j + 1
    
    def CreatDeform(self, deformCurve):
        #需要返回变形器节点，用以链接控制器属性
        

    # def CreatDynSys(self, dynCurve):
    #     #因为无法之间获取创建动力学曲线后生成的曲线毛囊等物件
    #     #所以，此方法主要处理生成物件的命名与大组；
    #     #然后获得动力学输出曲线，和解算器（用于链接开关）
    #     dynSys = 

    
    
    def CreakIkCtrl(self, JntChain, inputCurve,ikCtrlNum):
        #给曲线创建簇控制点，并为簇点创建控制器
        #蒙皮骨骼约束ik控制器，使其能跟随运动
        #控制器的位置，需要从根部到尾部逐渐变密集 ？？？ 能否实现
