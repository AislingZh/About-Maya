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

        #根据曲线和设定的骨骼数创建骨骼
        skinJntChain = self.CreatJntChain(inputCurve, JntNUm)

        #创建定位用的面片并蒙皮
        guideSurface = self.CreatGuideSurface(inputCurve, skinJntChain)[0]
        cmds.skinCluster( guideSurface, skinJntChain, tsb=True, skinMethod = 0, maximumInfluences = 1, dropoffRate = 10.0 )

        #给骨骼添加位置属性,标识在面片上的位置
        self.AddPosOnSurfaceAttr(skinJntChain, JntNUm)
        varFKCtrl = self.CreatVarFkCtrl(inputCurve, CtrlNum, guideSurface, skinJntChain[0])
     

        #复制曲线制作hair动力学系统
        DynCurve = cmds.duplicate(inputCurve, name = inputCurve + '_DynCurve')[0]
        DynNucleus = self.CreatDynSys(DynCurve)

        #复制曲线制作非线性变形器效果
        deformCurve = cmds.duplicate(inputCurve, name = inputCurve + '_deformCurve')[0]
        deformGrps = self.CreatDeform(deformCurve,skinJntChain[0])
        deformCtrlGrp = deformGrps[0]
        deformHandleGrp = deformGrps[1]


        #根据inputCurve去创建ik控制器，并返回ik控制器控制的曲线，会用此曲线去与inputCurve做blendshape

        ikCtrlSys = self.CreakIkCtrl( inputCurve, CtrlNum, guideSurface) 
        ikCtrlCurve = ikCtrlSys[0]

        #使用inputCurve曲线给骨骼链做ik链，并通过约束将运动传递到ikTfkjnt
        IKJntChain = cmds.duplicate(skinJntChain, name = inputCurve + '_ikJnt', parentOnly = True)
        ikSolvers = cmds.ikHandle(name=inputCurve + '_ikJnt_IKHandle', sj=IKJntChain[0], ee=IKJntChain[JntNUm - 1], curve = inputCurve, sol='ikSplineSolver',ccv = False)
        #ikSolvers -- > [u'_IKHandle', u'effector3', u'_curve'] 
        ikBS = cmds.blendShape(ikCtrlCurve, deformCurve, DynCurve, inputCurve, w=[(0, 1), (1, 0), (2, 0)])[0]

        ikTfkJnt = cmds.duplicate(skinJntChain, name = inputCurve + '_ikTfkJnt', parentOnly = True)
        for i in range(0,len(IKJntChain)):
            cmds.parentConstraint(IKJntChain[i], ikTfkJnt[i], mo = True)
        
        
        #创建主控制器   ！！！！添加控制的相关属性！！！
        mainCtrl = cmds.curve( name="MainCtrl", d = 1, p = [(-1,1,1),(1,1,1),(1,1,-1),(-1,1,-1),(-1,1,1),(-1,-1,1),(-1,-1,-1),(1,-1,-1),(1,-1,1),(-1,-1,1),(1,-1,1),(1,1,1),(1,1,-1),(1,-1,-1),(-1,-1,-1),(-1,1,-1)])
        mainCtrlShape = cmds.listRelatives(mainCtrl, s = True)[0]

        cmds.addAttr(mainCtrl, longName='ZLimit', attributeType='float', keyable=True, defaultValue=0)
        cmds.addAttr(mainCtrl, longName='ZRoll', attributeType='float', keyable=True, max=0, defaultValue=0 )
        cmds.addAttr(mainCtrl, longName='ZSize', attributeType='float', keyable=True, defaultValue=0)
        cmds.addAttr(mainCtrl, longName='YLimit', attributeType='float', keyable=True, defaultValue=0)
        cmds.addAttr(mainCtrl, longName='YRoll', attributeType='float', keyable=True, max=0, defaultValue=0 )
        cmds.addAttr(mainCtrl, longName='YSize', attributeType='float', keyable=True, defaultValue=0)
        cmds.addAttr(mainCtrl, longName='BodyTwist', attributeType='float', keyable=True, defaultValue=0)
        cmds.addAttr(mainCtrl, longName='IKCtrl', attributeType='float', keyable=True,min = 0, max=1, defaultValue=0)
        cmds.addAttr(mainCtrl, longName='stretch', attributeType='float', keyable=True,min = 0, max=1, defaultValue=0)
        cmds.addAttr(mainCtrl, longName='DynSwitch', attributeType='float', keyable=True,min = 0, max=1, defaultValue=0)
        cmds.addAttr(mainCtrl, longName='DeformSwitch', attributeType='float', keyable=True,min = 0, max=1, defaultValue=0)

        cmds.setAttr(mainCtrl + ".visibility", lock = True, keyable = False, channelBox = False)
        cmds.setAttr(mainCtrlShape + ".overrideEnabled", True)
        cmds.setAttr(mainCtrlShape + ".overrideColor", 17)
        mainCtrlGrp = cmds.group(mainCtrl, name = mainCtrl + "_offset")
        self.Align(mainCtrlGrp, ikTfkJnt[0])
        ###为主控制器上的开关做链接
        cmds.connectAttr(mainCtrl + ".BodyTwist", ikSolvers[0] + ".twist")
        cmds.connectAttr(mainCtrl + ".IKCtrl", ikCtrlSys[1] + ".visibility")
        
        cmds.connectAttr(mainCtrl + ".DynSwitch", DynNucleus + ".enable")
        cmds.connectAttr(mainCtrl + ".DynSwitch", ikBS + ".weight[2]")

        cmds.connectAttr(mainCtrl + ".DeformSwitch", ikBS + ".weight[1]")
        cmds.connectAttr(mainCtrl + ".DeformSwitch", deformCtrlGrp + ".visibility")

        

        #在ik上设置拉伸功能
        stretchBlend = cmds.shadingNode( 'blendTwoAttr', asUtility = True, n = inputCurve + '_stretchBlend' )
        curveInfoNode = cmds.arclen(inputCurve, ch=True)
        curveLen = cmds.getAttr(curveInfoNode + ".arcLength")
        cmds.connectAttr(mainCtrl + ".stretch", stretchBlend + ".attributesBlender")
        curveLenMul = cmds.shadingNode( 'multiplyDivide', asUtility = True, n = inputCurve + '_curveLenMul' )
        cmds.connectAttr(curveInfoNode + ".arcLength", curveLenMul + ".input1X")
        cmds.setAttr(curveLenMul + ".operation", 2)

        golableScaleMul = cmds.shadingNode( 'multiplyDivide', asUtility = True, n = inputCurve + '_golableScaleMul' )
        cmds.connectAttr(mainCtrl + ".scale", golableScaleMul + ".input1")
        cmds.setAttr(golableScaleMul + ".input2X", curveLen)
        cmds.connectAttr(golableScaleMul + ".output.outputX", curveLenMul + ".input2X")

        clamp = cmds.shadingNode( 'clamp', asUtility = True, n = inputCurve + '_stretchClamp' )
        cmds.setAttr(clamp + ".maxR", 1)
        cmds.connectAttr(curveLenMul + ".output.outputX", clamp + ".input.inputR")
        cmds.connectAttr(clamp + ".output.outputR", stretchBlend + ".input[0]")
        cmds.connectAttr(curveLenMul + ".output.outputX", stretchBlend + ".input[1]")

        for jnt in IKJntChain:
            cmds.connectAttr(stretchBlend + ".output" , jnt + ".scale.scaleX")


        #整理层级
        #####模型组
        geoGrp = cmds.group( name = inputCurve + '_geoGrp', empty = True, world = True)
        self.Align(geoGrp, skinJntChain[0])
        #####控制器组-----ik， fk控制器； input曲线，jnt组
        ctrlGrp = cmds.group( name = inputCurve + '_ctrlGrp', empty = True, world = True)
        FKCtrlGrp = cmds.listRelatives(varFKCtrl, fullPath = True)[0].split("|", 3)[1]
        jntGrp = cmds.group(skinJntChain[0],ikTfkJnt[0], IKJntChain[0], name = "jntGrp")
        cmds.parent(FKCtrlGrp, ikCtrlSys[1], deformCtrlGrp, inputCurve,jntGrp, mainCtrl, r = True)
        cmds.parent(mainCtrlGrp, ctrlGrp, r = True)
        #####其他组
        OtherGrp = cmds.group( name = inputCurve + '_otherGrp', empty = True, world = True)
        DynGrp = cmds.listRelatives(DynNucleus, parent = True)[0]
        ikSysGrp = cmds.listRelatives(ikCtrlCurve, fullPath = True)[0].split("|", 3)[1]

        cmds.parent(DynGrp, deformHandleGrp, guideSurface, ikSysGrp, deformCurve, DynCurve, ikSolvers[0], OtherGrp, r = True)
        ########总层级
        allGrp = cmds.group(geoGrp, ctrlGrp, OtherGrp, name = inputCurve + '_allGrp', world = True)

        
        ##global scale
        offsetLoc = cmds.spaceLocator( n = inputCurve + '_ctrl_offsetLoc')[0]
        cmds.setAttr(offsetLoc + ".inheritsTransform", 0)
        cmds.setAttr(offsetLoc + ".visibility", 0)
        cmds.parentConstraint( mainCtrl, offsetLoc, maintainOffset = False)
        cmds.scaleConstraint( mainCtrl, offsetLoc, maintainOffset = False)
        cmds.parent(offsetLoc, mainCtrl, r = True)

        for i in varFKCtrl:
            follow = cmds.listRelatives(i, parent = True)[0]
            cmds.connectAttr(offsetLoc + ".rotate", follow + ".rotate")
            cmds.connectAttr(offsetLoc + ".scale", follow + ".scale")

        
        ######使用节点控制蒙皮骨骼的盘起以及variableFK的功能
        j = 1
        for jnt in skinJntChain:
            rotateMultipliers = []
            # create a layered texture node and strength multiplier for every joint to multiply all scale values
            scaleMultiplier = cmds.shadingNode( 'layeredTexture', asUtility = True, n = 'util_' + jnt + '_scaleInput' )
            
            i = 0
            for ctrl in varFKCtrl:
                rotateMultiplier = self.create_ctrlOutput(ctrl, jnt)
                rotateMultipliers.append(rotateMultiplier)
                #链接ctrl的scale 到 scale multiplier
                cmds.connectAttr( ctrl + '.scale', scaleMultiplier + '.inputs[' + str(i) + '].color' )
                cmds.setAttr( scaleMultiplier + '.inputs[' + str(i) + '].blendMode', 6 )
                
                # get remapDistance outValue and connect to scale multiplier input[i] alpha
                remapDist = cmds.listConnections( rotateMultiplier , type = 'remapValue' )[0]
                cmds.connectAttr( remapDist + '.outValue', scaleMultiplier + '.inputs[' + str(i) + '].alpha' )
                
                i += 1
        
            # sum up rotate outputs of all controls and connect to joints
            # connect to sum +-avg node
            sum = cmds.shadingNode( 'plusMinusAverage', asUtility = True, n = 'util_' + jnt + '_sum_rotate' )	
            for i in range( len(rotateMultipliers ) ):
                cmds.connectAttr(rotateMultipliers[i] + ".output", sum + ".input3D[" + str(i) + "]")
            
            posNum = j - 1 - len(skinJntChain)
            j = j+1
            self.creatRollFun(jnt, sum, mainCtrl, posNum)
            # cmds.connectAttr( sum + '.output3D', jnt + '.rotate' )
            

            # set last input to base value of 1, OOP methods does not work on sub attributes of layeredTexture
            i += 1
            cmds.setAttr( scaleMultiplier + '.inputs[' + str(i) + '].color', 1,1,1,type = "float3" )
            cmds.setAttr( scaleMultiplier + '.inputs[' + str(i) + '].alpha', 1)
            cmds.setAttr( scaleMultiplier + '.inputs[' + str(i) + '].blendMode', 0 )
            
            
            # connect scale multiplier to joint scale YZ
            cmds.connectAttr(scaleMultiplier + ".outColor", jnt + ".scale")



        # curves = cmds.duplicate(inputCurve, 2) #把曲线复制出3份出来，分别用于ik控制器，非线性变形器，头发动力学系统

        
        # self.CreatHairDyn(curves[1])

        # cmds.blendShape(curves, inputCurve) #对曲线做bs，并以inputCurve

        # ikTfkJnt = cmds.duplicate(jntChin) #复制骨骼链出来，作为ikfk链接的中间骨骼

        # j = 0
        # for i in jntChin:

        #     alignCons = cmds.parentConstraint(i, ikTfkJnt[i], mo = True)
        #     j = j+1

        # fkJnt = cmds.duplicate(jntChin) #复制骨骼链出来蒙皮骨骼

        # self.CreatVarFK(fkJnt, CtrlNum)
    def creatRollFun(self, jnt, pulsNode, mainCon, posNum):

        RollSumRotateNode = cmds.shadingNode('plusMinusAverage', asUtility = True, name = jnt + '_RollSumRotate')
        cmds.connectAttr( pulsNode + '.output3D', RollSumRotateNode + '.input3D[0]')
        
        ReverseNode = cmds.shadingNode('reverse', asUtility = True, name = jnt + '_sumRotate_Reverse')
        cmds.connectAttr( pulsNode + '.output3D', ReverseNode + '.input')
        OrgRotSwitchNode = cmds.shadingNode('multiplyDivide', asUtility = True, name = jnt + '_OrgRotSwitch')
        cmds.connectAttr( ReverseNode + '.output', OrgRotSwitchNode + '.input1')
        cmds.connectAttr( OrgRotSwitchNode + '.output', RollSumRotateNode + '.input3D[1]')

        RollSubNode = cmds.shadingNode('plusMinusAverage', asUtility = True, name = jnt + '_posSubRoll')
        cmds.setAttr(RollSubNode + '.operation', 2)
        cmds.setAttr(RollSubNode + '.input3D[0]', 0, posNum, posNum, type = "float3")  #把节点设置为减法
        cmds.connectAttr(mainCon + '.YRoll', RollSubNode + '.input3D[1].input3Dy', f = True)
        cmds.connectAttr(mainCon + '.ZRoll', RollSubNode + '.input3D[1].input3Dz', f = True)
        
        yzClampNode = cmds.shadingNode('clamp', asUtility = True, name = jnt + '_yzClamp')
        cmds.setAttr(yzClampNode + '.max',1,1,1,type = "float3")
        cmds.connectAttr(RollSubNode + '.output3Dy', yzClampNode + '.inputG', f = True)
        cmds.connectAttr(RollSubNode + '.output3Dz', yzClampNode + '.inputB', f = True)

        yzClampAddNode = cmds.shadingNode('addDoubleLinear', asUtility = True, name = jnt + '_yzClampAdd')
        cmds.connectAttr(yzClampNode + '.outputG', yzClampAddNode + '.input1' , f = True)
        cmds.connectAttr(yzClampNode + '.outputB', yzClampAddNode + '.input2' , f = True)
        cmds.connectAttr(yzClampAddNode + '.output' ,yzClampNode + '.inputR' , f = True)
        ## 到此 clamp节点的'outputR'的值为 整个盘起系统的 开关控制器 ， clamp节点的'outputG'的值为 YRoll的开关， clamp节点的'outputB'的值为 ZRoll的开关;

        cmds.connectAttr(yzClampNode + '.outputR', OrgRotSwitchNode + '.input2X' , f = True)
        cmds.connectAttr(yzClampNode + '.outputR', OrgRotSwitchNode + '.input2Y' , f = True)
        cmds.connectAttr(yzClampNode + '.outputR', OrgRotSwitchNode + '.input2Z' , f = True)


        sizeMultNode = cmds.shadingNode('multiplyDivide', asUtility = True, name = jnt + '_sizeMult')
        cmds.connectAttr(mainCon + '.YSize', sizeMultNode + '.input1Y', f = True)
        cmds.connectAttr(mainCon + '.ZSize', sizeMultNode + '.input1Z', f = True)
        cmds.setAttr(sizeMultNode + '.input2', 0, 0.1, 0.1, type = "float3") 
        YSizeAddNode = cmds.shadingNode('addDoubleLinear', asUtility = True, name = jnt + '_YSizeAdd')
        ZSizeAddNode = cmds.shadingNode('addDoubleLinear', asUtility = True, name = jnt + '_ZSizeAdd')
        cmds.connectAttr(sizeMultNode + '.outputY' ,YSizeAddNode + '.input1' , f = True)
        cmds.connectAttr(sizeMultNode + '.outputZ' ,ZSizeAddNode + '.input1' , f = True)

        RollMultNode = cmds.shadingNode('multiplyDivide', asUtility = True, name = jnt + '_RollMult')
        cmds.connectAttr(yzClampNode + '.outputG' ,RollMultNode + '.input1Y' , f = True)
        cmds.connectAttr(yzClampNode + '.outputB' ,RollMultNode + '.input1Z' , f = True)
        cmds.connectAttr(mainCon + '.YLimit' ,RollMultNode + '.input2Y' , f = True)
        cmds.connectAttr(mainCon + '.ZLimit' ,RollMultNode + '.input2Z' , f = True)

        RollSizMultNode = cmds.shadingNode('multiplyDivide', asUtility = True, name = jnt + '_RollSizMult')
        cmds.connectAttr(RollMultNode + '.output' ,RollSizMultNode + '.input1' , f = True)
        cmds.connectAttr(YSizeAddNode + '.output' ,RollSizMultNode + '.input2Y' , f = True)
        cmds.connectAttr(ZSizeAddNode + '.output' ,RollSizMultNode + '.input2Z' , f = True)


        cmds.connectAttr(RollSizMultNode + '.output' ,RollSumRotateNode + '.input3D[2]' , f = True)
        cmds.connectAttr(RollSumRotateNode + '.output3D' ,jnt + '.rotate' , f = True)


    def CreatJntChain(self, inputCurve = cmds.ls(sl = True), JntNum = 10, orientation = 'xyz'):
        
        JntChain = []


        #根据曲线等间距创建骨骼
        loc = cmds.spaceLocator(p = (0,0,0))
        motionpath = cmds.pathAnimation(loc[0], inputCurve)
        cmds.setAttr(motionpath+".fractionMode", True)
        sdf = cmds.connectionInfo(motionpath + '.uValue', sourceFromDestination = True)
        cmds.disconnectAttr(sdf, motionpath + '.uValue')
        for i in range(0,JntNum):
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
        cmds.delete(loc)

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
            cmds.setAttr( jnt + '.jointPosition', i*1.0/(len(jntChain) - 1), lock = True)
            i = i +1
        
    
    def CreatVarFkCtrl(self, ctrName, num, surf, jnt):
        ctrlGrp = cmds.group( name = ctrName + '_VFkCtrls', empty = True, world = True)
        self.Align(ctrlGrp, jnt)
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
            cmds.addAttr( longName='position', attributeType='float', keyable=True, min=(0-FolliclePos)*10, max=(1-FolliclePos)*10 )
            cmds.addAttr( longName='radius', attributeType='float', keyable=True, min=0.0001, defaultValue=2 )

            ctrlRadiusRange = cmds.shadingNode( 'setRange', asUtility = True, n=currentCtrl[0] + '_ctrlRadiusRange' )
            cmds.setAttr(ctrlRadiusRange + ".minX", 0.0001)
            cmds.setAttr(ctrlRadiusRange + ".maxX", 5)
            cmds.setAttr(ctrlRadiusRange + ".oldMinX", 0.0001)
            cmds.setAttr(ctrlRadiusRange + ".oldMaxX", 30)
            cmds.connectAttr(currentCtrl[0] + '.radius', ctrlRadiusRange + ".valueX")

            #创建毛囊
            currentFollicle = self.create_follicle("fkCtrFollicle", surf, uPos=FolliclePos, vPos=0.5)
            cmds.setAttr(currentFollicle + ".simulationMethod", 0)
            cmds.setAttr(currentFollicle + ".collide", 0)
            cmds.setAttr(currentFollicle + ".flipDirection", True)
            currentFollicleTran = cmds.listRelatives(currentFollicle, parent = True)[0]

            cmds.parent(currentFollicle, ctrlGrp)

            #设置旋转强度属性
            rotStrengthMul = cmds.shadingNode( 'multiplyDivide', asUtility = True, n = str( currentCtrl[0] ) + "_strength_mult" )
            cmds.connectAttr(currentCtrl[0] + ".rotate", rotStrengthMul + ".input1")
            cmds.connectAttr(currentCtrl[0] + ".rotateStrength", rotStrengthMul + ".input2X", f = True)
            cmds.connectAttr(currentCtrl[0] + ".rotateStrength", rotStrengthMul + ".input2Y", f = True)
            cmds.connectAttr(currentCtrl[0] + ".rotateStrength", rotStrengthMul + ".input2Z", f = True)

            #设置控制器位置属性
            ctrlPosRange = cmds.shadingNode( 'setRange', asUtility = True, n=currentCtrl[0] + '_ctrlPosRange' )
            cmds.setAttr(ctrlPosRange + ".minX", 0-FolliclePos)
            cmds.setAttr(ctrlPosRange + ".maxX", 1-FolliclePos)
            cmds.setAttr(ctrlPosRange + ".oldMinX", (0-FolliclePos)*10)
            cmds.setAttr(ctrlPosRange + ".oldMaxX", (1-FolliclePos)*10)
            cmds.connectAttr(currentCtrl[0] + '.position', ctrlPosRange + ".valueX")

            jntPosPlus = cmds.shadingNode( 'plusMinusAverage', asUtility = True, n=currentCtrl[0] + '_jntposZeroCompensate' )
            FolloclePos = cmds.getAttr(currentFollicle + ".parameterU")
            cmds.setAttr(jntPosPlus + ".input1D[0]", FolloclePos)
            cmds.connectAttr(ctrlPosRange + '.outValueX', jntPosPlus + '.input1D[1]', f=True )
            cmds.connectAttr(jntPosPlus + '.output1D', currentFollicle + ".parameterU", f=True )

            #给控制器设置层级
            offsetGrp = cmds.group(em = True, n = currentCtrl[0] + "_Offset")
            self.Align(offsetGrp, currentCtrl[0])
            cmds.parent(currentCtrl[0], offsetGrp, r = True)
            # followGrp = cmds.group(currentCtrl[0], n = currentCtrl[0] + "_follow")

            cmds.connectAttr(currentFollicleTran + ".translate", offsetGrp + ".translate")
            cmds.parent(offsetGrp, ctrlGrp, r = True)

            listOfCtrls.append(currentCtrl[0])
            cmds.select(clear = True)

        return listOfCtrls

    def create_ctrlOutput(self, ctrl, jnt):
        prefix = "util_" + ctrl + "_" + jnt + "_"
        jntposMinusCtrlpos = cmds.shadingNode('plusMinusAverage', asUtility = True, n=prefix + 'jntpos-Ctrlpos')
        cmds.setAttr(jntposMinusCtrlpos + ".operation", 2)
        absPower = cmds.shadingNode('multiplyDivide', asUtility = True, n=prefix + 'absPower')
        cmds.setAttr(absPower + ".input2", 2,2,2, type='double3')
        cmds.setAttr(absPower + ".operation", 3)
        absSqrt = cmds.shadingNode('multiplyDivide', asUtility = True, n=prefix + 'absSqrt')
        cmds.setAttr(absSqrt + '.input2', .5,.5,.5, type='double3')
        cmds.setAttr(absSqrt + '.operation', 3)
        remapDist = cmds.shadingNode('remapValue', asUtility = True, n=prefix + 'remapDist')
        rotateMultiplier = cmds.shadingNode('multiplyDivide', asUtility = True, n = prefix + 'infl_mult')
        
        # get existing offset nodes which were created in controller function
        ctrlPosRange = cmds.listConnections( ctrl + ".position", exactType = True, type = 'setRange' )[0]
        jntposZeroCompensate = cmds.listConnections( ctrlPosRange, exactType = True, type = 'plusMinusAverage' )[0]
        rotateStrengthMultiplier = cmds.listConnections( ctrl, exactType = True, type = 'multiplyDivide' )[0]

        ctrlRadusRange = cmds.listConnections(ctrl + ".radius", exactType = True, type = 'setRange' )[0]
        
        # jntpos - ctrlpos
        cmds.connectAttr(jnt + '.jointPosition', jntposMinusCtrlpos + '.input1D[0]', f=1)
        cmds.connectAttr(jntposZeroCompensate + '.output1D', jntposMinusCtrlpos + '.input1D[1]', f=1)
        
        # abs
        cmds.connectAttr(jntposMinusCtrlpos + '.output1D', absPower + '.input1X', f=1)
        cmds.connectAttr(absPower + '.outputX', absSqrt + '.input1X', f=1)
        
        # rotate remap: distance 0 to 1 | falloff distance to 0
        cmds.connectAttr(absSqrt + '.outputX', remapDist + '.inputValue', f=1)
        cmds.connectAttr(ctrlRadusRange + '.outValueX', remapDist + '.value[1].value_Position', f=1)
        cmds.setAttr(remapDist + '.value[0].value_Position', 0)
        cmds.setAttr(remapDist + '.value[0].value_FloatValue', 1)
        cmds.setAttr(remapDist + '.value[1].value_FloatValue', 0)
        cmds.setAttr(remapDist + '.value[0].value_Interp', 2)
        
        # connect strength multiplier to rotate multiplier
        cmds.connectAttr(rotateStrengthMultiplier + ".output", rotateMultiplier + ".input1")
        cmds.connectAttr(remapDist + '.outValue', rotateMultiplier + '.input2X', f=1)
        cmds.connectAttr(remapDist + '.outValue', rotateMultiplier + '.input2Y', f=1)
        cmds.connectAttr(remapDist + '.outValue', rotateMultiplier + '.input2Z', f=1)
        
        # print('Created ' + ctrl + '--' + jnt + ' output.')
        return rotateMultiplier

        

    def Align(self, current, target):
        #current：当前的位置，target：要对齐的目标位置
        targetPos = cmds.xform(target, q=True, ws=True, t=True)
        cmds.xform(current, ws=True, t=[targetPos[0],targetPos[1],targetPos[2]])
        targetRot = cmds.xform(target, q=True, ws=True, ro=True)
        cmds.xform(current, ws=True, ro=[targetRot[0],targetRot[1],targetRot[2]])


    def create_follicle(self, N, nurbs, uPos, vPos):
        if cmds.objectType( nurbs, isType='transform' ):
            nurbs = cmds.listRelatives(nurbs, s = True)[0]
        elif cmds.objectType( nurbs, isType='nurbsSurface'):
            pass
        else:
            return False
        
        #创建毛囊节点
        follicleNode = cmds.createNode('follicle', name= N)
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
        targetPos = cmds.xform(jnt, q=True, ws=True, t=True)
        cmds.xform(squashDefs[1], ws=True, t=[targetPos[0],targetPos[1],targetPos[2]])

        #创建变形器的控制器，整理并添加属性，并链接属性
        deformCtrl = cmds.spaceLocator(p = (0,0,0), n = jnt.split("_", 1)[0] + "_demform_ctrl")[0]
        posLoc = cmds.spaceLocator(p = (0,0,0), n = jnt.split("_", 1)[0] + "_posLoc")[0]
        
        cmds.transformLimits(deformCtrl, tx = (0,1), etx=(True, False))
        cmds.setAttr(deformCtrl + ".translateY", lock = True, keyable = False, channelBox = False)
        cmds.setAttr(deformCtrl + ".translateZ", lock = True, keyable = False, channelBox = False)
        cmds.setAttr(deformCtrl + ".scaleX", lock = True, keyable = False, channelBox = False)
        cmds.setAttr(deformCtrl + ".scaleY", lock = True, keyable = False, channelBox = False)
        cmds.setAttr(deformCtrl + ".scaleZ", lock = True, keyable = False, channelBox = False)
        cmds.setAttr(deformCtrl + ".rotateX", lock = True, keyable = False, channelBox = False)
        cmds.setAttr(deformCtrl + ".rotateY", lock = True, keyable = False, channelBox = False)
        cmds.setAttr(deformCtrl + ".rotateZ", lock = True, keyable = False, channelBox = False)

        # cmds.addAttr( longName='deform_switch', attributeType='float', keyable=True, min=0, max=1 )
        cmds.addAttr( longName='amplitude', attributeType='float', keyable=True, min=-20, max=20, defaultValue = 1 )
        cmds.addAttr( longName='wavelength', attributeType='float', keyable=True, min=1, max =10 , defaultValue = 5)
        cmds.addAttr( longName='offset', attributeType='float', keyable=True, min=-100, max=100)
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
        jntOri = round(cmds.getAttr(jnt + ".jointOrientY"))
        o = abs(jntOri)%360 /90 
        if o == 0 :
            cmds.setAttr(sineDefs[1] + ".rotateZ", 90)
            cmds.setAttr(squashDefs[1] + ".rotateZ", 90)
        elif o == 1 :
            cmds.setAttr(sineDefs[1] + ".rotateX", -90)
            cmds.setAttr(squashDefs[1] + ".rotateX", -90)
        elif o == 2 :
            cmds.setAttr(sineDefs[1] + ".rotateZ", -90)
            cmds.setAttr(squashDefs[1] + ".rotateZ", -90)
        elif o == 3 :
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

        cmds.connectAttr(deformCtrl + ".translate",posLoc + ".translate")
        # cmds.pointConstraint(posLoc, squashDefs[1], mo = True)
        cmds.pointConstraint(posLoc, sineDefs[1], mo = True)

        deformGrp = cmds.group(squashDefs[1],sineDefs[1], n = dynCurve + "deform_Grp")
        deformGrps.append(deformGrp)

        return deformGrps


    def CreatDynSys(self, dynCurve):
        
        ## test 手动创建动力学相关节点并链接，返回解算器用于控制器链接开关

        orgCurve = cmds.duplicate(dynCurve, rr = True, name = dynCurve + '_start')
        outCurve = cmds.duplicate(dynCurve, rr = True, name = dynCurve + '_out')
        orgCurveShape = cmds.listRelatives(orgCurve, s = True)[0]
        outCurveShape = cmds.listRelatives(outCurve, s = True)[0]

        # rebuildNode = cmds.createNode('rebuildCurve', name=orgCurveShape + "_rebuild")

        # cmds.connectAttr(orgCurveShape + ".worldSpace[0]", rebuildNode + ".inputCurve")

        # newCurve = cmds.createNode('nurbsCurve', name=rebuildNode + "_rebuildCurveShape")
        # cmds.connectAttr(rebuildNode + ".outputCurve", orgCurveShape + ".create")


        follicleNode = cmds.createNode('follicle', name=dynCurve + "_follicle")
        cmds.connectAttr( orgCurveShape + ".local", follicleNode + ".startPosition")
        cmds.connectAttr( orgCurve[0] + ".worldMatrix[0]", follicleNode + ".startPositionMatrix")
        cmds.connectAttr( follicleNode + ".outCurve", outCurveShape + ".create")

        hairSystemNode = cmds.createNode('hairSystem', name=dynCurve + "_hairSystem")
        cmds.connectAttr( follicleNode + ".outHair", hairSystemNode + ".inputHair[0]")
        cmds.connectAttr( hairSystemNode + ".outputHair[0]", follicleNode + ".currentPosition")

        nucleusNode = cmds.createNode('nucleus', name="_nucleus")
        cmds.connectAttr( hairSystemNode + ".currentState", nucleusNode + ".inputActive[0]")
        cmds.connectAttr( hairSystemNode + ".startState", nucleusNode + ".inputActiveStart[0]")
        cmds.connectAttr( nucleusNode + ".outputObjects[0]", hairSystemNode + ".nextState")
        cmds.connectAttr( nucleusNode + ".startFrame", hairSystemNode + ".startFrame")

        cmds.connectAttr("time1.outTime", hairSystemNode + ".currentTime")
        cmds.connectAttr("time1.outTime", nucleusNode + ".currentTime")


        DynGrp = cmds.group(orgCurve, outCurve, follicleNode, hairSystemNode, nucleusNode, name = dynCurve + "_DynGrp")
        cmds.wire(dynCurve, w = outCurve, name = "ikDynWire")[0]

        return nucleusNode

    
    def CreakIkCtrl(self, inputCurve, fkCtrlNum, guideSurface):
        #给曲线创建簇控制点，并为簇点创建控制器
        ##### 一个cv点对应一个簇并且簇点密集度有增加，因此需要处理两个问题：
        #         1.根据需求的控制器数重建曲线的CV点，
        #         2.根据控制器数删除CV点
        #####处理控制器位置问题：
        #         1.跟随（使用pointOnCurve） <---- 在引导面片上做毛囊定位，包括旋转
        #         2.去除双重控制（父层级上减掉多的运动）
        #####返回需要用于与原曲线做blendshape的曲线

        #根据设置的控制器数量计算所需的ik控制器数 
        # cvNum = fkCtrlNum
        # if fkCtrlNum <= 4:
        #     cvNum = (fkCtrlNum - 1) * 2
        #     cmds.delete(CCurve+ ".cv[1]", CCurve+ ".cv["+ str(cvNum + 1) + "]")
        #     for i in range(0,cvNum):
        #         cmds.cluster( 'curve4.cv[4]', rel=True )
        # elif 4 < fkCtrlNum <= 10:
        #     cvNum = (fkCtrlNum-1) * 3
        # elif 10 < fkCtrlNum :
        #     cvNum = (fkCtrlNum - 1) * 4 
        # else:
        #     print ("错误")
        
        cvNum = fkCtrlNum * 2 - 1
        outputCurve = cmds.duplicate(inputCurve, name = inputCurve + '_ikCtrlCurve')[0]
        CCurve = cmds.duplicate(inputCurve, name = outputCurve + '_CC')[0]
        CCurve = cmds.rebuildCurve(CCurve, d = 3, s = cvNum - 1)[0]

        curveGRp = cmds.group(CCurve, outputCurve, name ='ikCtrlcurve_Grp', world = True)

        cHnadleGrp = cmds.group(name = CCurve + '_cHandle', empty = True, world = True)
        IKCtrlGrp = cmds.group(name = inputCurve + '_ikCtrlGrp', empty = True, world = True)
        ikFollGrps = cmds.group(name = inputCurve + "_ikFollicleGrp", empty = True, world = True)
        follicles = []
        for i in range(0,cvNum):
            if cvNum > 1:
                Pos = (1.0/(cvNum - 1)) * i
            else:
                Pos = (1.0/cvNum) * i
            
            #创建毛囊
            currentFollicle = self.create_follicle( "ikCtrFollicle", guideSurface, uPos=Pos, vPos=0.5)
            cmds.setAttr(currentFollicle + ".simulationMethod", 0)
            cmds.setAttr(currentFollicle + ".collide", 0)
            cmds.setAttr(currentFollicle + ".flipDirection", True)
            currentFollicleTran = cmds.listRelatives(currentFollicle, parent = True)[0]
            follicles.append(currentFollicleTran)
            cmds.parent(currentFollicle, ikFollGrps, r = True)            



        
        for i in range(1, cvNum + 1):
            if  i == 1:
                CHandle = cmds.cluster( CCurve + '.cv[0]', CCurve + '.cv[1]', rel=True )
            elif i == cvNum:
                CHandle = cmds.cluster( CCurve + '.cv[' + str(i) + ']', CCurve + '.cv[' + str(i + 1) + ']', rel=True )
            else:
                CHandle = cmds.cluster( CCurve + '.cv[' + str(i) + ']', rel=True )
            cmds.parent(CHandle, cHnadleGrp, r = True)

            #给簇创建控制器，并且整理属性
            IKCtrl = cmds.circle( name = ( inputCurve + '_ikCtrl' + str(i)), c=(0,0,0), nr=(1,0,0), sw=360, r=1.5, d=3, ut=0, tol=0.01, s=8, ch=False)[0]
            cmds.setAttr(IKCtrl + ".rotateX", lock = True, keyable = False, channelBox = False)
            cmds.setAttr(IKCtrl + ".rotateY", lock = True, keyable = False, channelBox = False)
            cmds.setAttr(IKCtrl + ".rotateZ", lock = True, keyable = False, channelBox = False)
            cmds.setAttr(IKCtrl + ".scaleZ", lock = True, keyable = False, channelBox = False)
            cmds.setAttr(IKCtrl + ".scaleY", lock = True, keyable = False, channelBox = False)
            cmds.setAttr(IKCtrl + ".scaleX", lock = True, keyable = False, channelBox = False)
            #给控制器打组，并且约束簇
            offsetGrp = cmds.group(IKCtrl, n = IKCtrl + "_Offset")
            self.Align(offsetGrp, CHandle)
            followGrp = cmds.group(IKCtrl, n = IKCtrl + "_follow")
            #通过pointOnCurve以及表达式控制ik控制器的位置
            cmds.parentConstraint(follicles[i-1], offsetGrp, mo = True)
            # cmds.pointConstraint(follicles[i-1], offsetGrp, mo = True)
            # cmds.orientConstraint(follicles[i-1], offsetGrp, mo = True)
            #减掉双倍位移
            ikCtrMul = cmds.shadingNode( 'multiplyDivide', asUtility = True, n = IKCtrl + "_mult" )
            cmds.connectAttr(IKCtrl + ".translate", ikCtrMul + ".input1")
            cmds.setAttr(ikCtrMul + ".input2", -1,-1,-1,type = "float3")
            cmds.connectAttr(ikCtrMul + ".outputY", followGrp + ".translateY")
            cmds.connectAttr(ikCtrMul + ".outputZ", followGrp + ".translateZ")
            
            cmds.connectAttr(IKCtrl + ".translate", CHandle[1] + ".translate")
            cmds.parent(offsetGrp, IKCtrlGrp, r = True)
            
        #用cc曲线包裹输出的ik曲线
        wireNode = cmds.wire(outputCurve, w = CCurve, name = "ikCtrlWire")[0]
        cmds.setAttr(wireNode + ".dropoffDistance[0]", 99999999)

        IKCtrlSysGrp = cmds.group(curveGRp, cHnadleGrp, ikFollGrps, name ='IKCtrlSys_Grp', world = True)

        return outputCurve, IKCtrlGrp
        

