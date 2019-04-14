
# ------------------------------------------------------------------------------------------------------------//
# ------------------------------------------------------------------------------------------------------------//
# 	SCRIPT:	FacialConnectWin.py
# 	VERSION: 1.0
# 	AUTHOR:	Aislingzh
# 			Aislingzh@qq.com
# 	DATE:		3 12, 2019
	

# 	DESCRIPTION:	 
# 			一键链接blendshape和表情控制面板

# ------------------------------------------------------------------------------------------------------------//	
# ------------------------------------------------------------------------------------------------------------//

# ------------------------------------------------------------------------------------------------------------//
# 	PROC:	FacialConnectWin
	
#bs命名对应规则，ctr名（脸部部位+左中右）+动作
#首先将不同位置的bs放在不同的字符串里，明确一一对应不同位置的bs与控制器的不同的链接方式 --------bs命名就只需要包含控制器的名字就ok啦~~ 
# ------------------------------------------------------------------------------------------------------------//



import maya.mel as mel
import maya.cmds as cmds
class FacialConnectWin(object):
    # Vertical 竖直方向 y轴
    #+
    blName1 = ['Brows_R_Up', 'Brows_L_Up', 'BrowsC_R_Up', 'BrowsC_L_Up', 'EyesOut_L_WideOut', 'JawZ_Fwd', 'Jaw_Up', 'Chin_Up', 'BrowsCR_L_Up', 'BrowsCR_R_Up']
    blName2 = ['Eyes_R_Wide', 'Eyes_L_Wide', 'Eyes_Look_Up', 'Mouth_Up', 'Lips_L_Smile', 'Lips_R_Smile', 'EyesOut_R_WideOut']

    blNameB1 = ['Brows_R_UpB', 'Brows_L_UpB', 'BrowsC_R_UpB', 'BrowsC_L_UpB' , 'EyesOut_L_WideOutB', 'EyesOut_R_WideOutB']
    #-
    blName3 = ['Brows_R_Down', 'Brows_L_Down', 'BrowsC_L_Down', 'BrowsC_R_Down', 'EyesOut_L_NarrowOut', 'JawZ_Bc', 'EyesOut_R_NarrowOut']


    blNameB2 = ['Brows_R_DownB', 'Brows_L_DownB', 'BrowsC_L_DownB', 'BrowsC_R_DownB', 'EyesOut_L_NarrowOutB', 'EyesOut_R_NarrowOutB']

    blName4 = ['Eyes_R_Blink', 'Eyes_L_Blink', 'Eyes_Look_Down', 'Jaw_Open', 'Mouth_Down', 'Lips_L_Frown', 'Lips_R_Frown']
    #Horizontal 水平方向 x轴
    #+
    blName5 = ['Eyes_Look_Left', 'EyesOut_L_NarrowInner', 'EyesOut_R_NarrowInner']
    blName6 = ['BrowsC_R_Squeeze', 'BrowsC_L_Squeeze', 'Nostril_Flare', 'JawL_NarrowOpen']

    blNameB3 = ['BrowsC_R_SqueezeB', 'BrowsC_L_SqueezeB']

    blName7 = ['O_Phoneme', 'Ch_Phoneme', 'MBP_Phoneme', 'Fv_Phoneme']  
    blName8 = ['Jaw_Left', 'Mouth_ScrunchLeft', 'Lips_L_Narrow', 'Lips_R_Narrow']  
    #-
    blName9 = ['Nostril_Narrow', 'Jaw_Right', 'Mouth_ScrunchRight']
    blName10 = ['Eyes_Look_Right', 'Lips_L_Stretch', 'Lips_R_Stretch']

    blNameB4 = []
    #Corners 四个角 xy轴混合用
    #+-
    blName11 = ['Cheek_LSquint', 'UpperLips_LDown', 'LowerLips_LUp', 'UpperLipsY_LIn', 'LowerLipsY_LIn', 'UpperLipsRX_LClose', 'LowerLipsRX_LClose','LowerEyeLips_LUp', 'UpperEyeLips_LDown']
    #-+
    blName12 = ['Cheek_LPuff', 'UpperLips_LUp', 'LowerLips_LDown', 'UpperLipsY_ROut', 'LowerLipsY_ROut', 'Sneer_Up_Left', 'UpperLipsRX_RFunnel', 'LowerLipsRX_RFunnel', 'LowerLipsConner_RDown', 'UpperLipsConner_RUp', 'LowerEyeLips_LDown', 'UpperEyeLips_LUp']
    #++
    blName13 = ['Cheek_RPuff', 'UpperLips_RUp', 'LowerLips_RDown', 'UpperLipsY_LOut', 'LowerLipsY_LOut', 'Sneer_Up_Right', 'UpperLipsRX_LFunnel', 'LowerLipsRX_LFunnel', 'LowerLipsConner_LDown', 'UpperLipsConner_LUp', 'LowerEyeLips_RDown', 'UpperEyeLips_RUp']
    #--
    blName14 = ['Cheek_RSquint', 'UpperLips_RDown', 'LowerLips_RUp', 'UpperLipsY_RIn', 'LowerLipsY_RIn', 'UpperLipsRX_RClose', 'LowerLipsRX_RClose', 'LowerEyeLips_RUp', 'UpperEyeLips_RDown']

    WINDOW_NAME = "FACEUI"

    def __init__(self):
        #构造函数
        self.bsName = None

        if cmds.window(self.WINDOW_NAME, exists = True):
            cmds.deleteUI(self.WINDOW_NAME, window = True)

        main_window = cmds.window(self.WINDOW_NAME, title =  "FACE Edit", rtf = True,  menuBar=True)
        # main_layout = cmds.formLayout(parent = main_window)

        cmds.menu( label='Help', helpMenu=True )
        cmds.menuItem( 'Application..."', label='"About' )

        
        cmds.frameLayout("Face:", collapsable = True, labelVisible=1, marginWidth=5,marginHeight=5,borderStyle='etchedOut' )
        cmds.columnLayout(adj=1)
        
        Import_button = cmds.button(label = "ChangeBSTarget",h=25,command = self.ChangeBSTarget) 

        
        cmds.separator( height=5,style='in' )
        cmds.separator( height=5,style='in' )

        Moth_button = cmds.button(label = "ConnectHeadBS",h=25,command = self.HeadBSConnect )
        cmds.separator( height=10,style='in' )    
        Eye_button = cmds.button(label = "ConnectBrowesBS",h=25,command = self.DoBrowesBSConnect)

        cmds.separator( height=10,style='in' )


        cmds.showWindow(main_window)

    def Import_FaceBtCon(self, *args):
        #导入表情面板
        # cmds.file('Y:/Face_Temp.mb', i=True, f=True)
        print "sdfsdf"

    def HeadBSConnect(self, *args):
        self.bsName = 'head_BS'
        self.DoHeadConnect()

    def DoBrowesBSConnect(self, *args):
        self.bsName = 'Brows_BS'
        self.DoBrowesConnect()

    def DoBrowesConnect(self):
        blNameList = self.blNameB3 + self.blNameB1 + self.blNameB2 + self.blNameB4
        for name in blNameList:
            if not cmds.objExists(self.bsName + "." + name):
                cmds.confirmDialog(t=u'敬告！！！', m=u'场景中缺少目标体' + name , b=[u'好的'], db=u'好的')
                return
        
        self.clearUnuseNode()

        blNameVerUp = self.blNameB1
        for name in blNameVerUp:
            self.VerticalUp(name)

        blNameVerBottom = self.blNameB2
        for name in blNameVerBottom:
            self.VerticalBottom(name)
        
        blNameHorRight = self.blNameB3
        for name in blNameHorRight:
            self.HorizontalRight(name)

        blNameHorLeft = self.blNameB4
        for name in blNameHorLeft:
            self.HorizontalLeft(name)

    def DoHeadConnect(self):
        blNameList = self.blName1+self.blName2+self.blName3+self.blName4+\
                        self.blName5+self.blName6+self.blName7+self.blName8+\
                        self.blName9+self.blName10+self.blName11+self.blName12+\
                        self.blName13+self.blName14
        
        for name in blNameList:
            if not cmds.objExists(self.bsName + "." + name):
                cmds.confirmDialog(t=u'敬告！！！', m=u'场景中缺少目标体' + name , b=[u'好的'], db=u'好的')
                return
        
        self.clearUnuseNode()

        blNameVerUp = self.blName1+self.blName2
        for name in blNameVerUp:
            self.VerticalUp(name)
        
        blNameVerBottom = self.blName3+self.blName4
        for name in blNameVerBottom:
            self.VerticalBottom(name)

        blNameHorRight = self.blName5 + self.blName6 + self.blName7 + self.blName8
        for name in blNameHorRight:
            self.HorizontalRight(name)

        blNameHorLeft = self.blName9 + self.blName10
        for name in blNameHorLeft:
            self.HorizontalLeft(name)

        blNameCorTR = self.blName12
        for name in blNameCorTR:
            self.CornersTopRight(name)

        blNameCorTL = self.blName13
        for name in blNameCorTL:
            self.CornersTopLeft(name)

        blNameCorBR = self.blName11
        for name in blNameCorBR:
            self.CornersButtomRight(name)

        blNameCorBL = self.blName14
        for name in blNameCorBL:
            self.CornersButtomLeft(name)


    def VerticalUp(self, bsItem):
        #选择竖直方向的上方向
        self.ConnectControlVertical("top",bsItem)
    
    def VerticalBottom(self, bsItem):
        #选择竖直方向的下方向
        self.ConnectControlVertical("bottom",bsItem)

    def HorizontalRight(self, bsItem):
        self.ConnectControlHorizontal("right", bsItem)
    
    def HorizontalLeft(self, bsItem):
        self.ConnectControlHorizontal("left", bsItem)

    def CornersTopRight(self, bsItem):
        self.ConnectControlCorners("topRight", bsItem)  

    def CornersButtomRight(self, bsItem):
        self.ConnectControlCorners("bottomRight", bsItem)

    def CornersButtomLeft(self, bsItem):
        self.ConnectControlCorners("bottomLeft", bsItem)

    def CornersTopLeft(self, bsItem):
        self.ConnectControlCorners("topLeft", bsItem)

    def ConnectControlVertical(self, position, bsItem):
        #链接竖直方向位置上的BS
        name = self.GetCtrName(bsItem)
        if cmds.objExists(name + "Grp"):
            if position == "top":
                #create clamp node
                topClampName = cmds.createNode('clamp', n = name + "TopClamp")
                #set clamp max and min
                cmds.setAttr(topClampName + ".maxR", 1)
                cmds.setAttr(topClampName + ".minR", 0)
                #connect control to clamp and clamp to blend
                cmds.connectAttr(name + "CircleCtrl.ty", topClampName + ".inputR")
                cmds.connectAttr(topClampName + ".outputR", self.bsName + "." + bsItem)
        
            elif position == "bottom":
                #create clamp node
                bottomClampName = cmds.createNode('clamp', n = name + "BottomClamp")
                #create multiply divide node
                bottomMultName = cmds.createNode('multiplyDivide', n = name + "BottomMultDivide")
                #set operation to multiply and input 2 to -1
                cmds.setAttr(bottomMultName + ".operation", 1)
                cmds.setAttr(bottomMultName + ".input2X", -1)

                #set clamp max and min
                cmds.setAttr(bottomClampName + ".maxR", 1)
                cmds.setAttr(bottomClampName + ".minR", 0)

                cmds.connectAttr(name + "CircleCtrl.ty", bottomMultName + ".input1X")
                cmds.connectAttr(bottomMultName + ".outputX", bottomClampName + ".inputR")
                cmds.connectAttr(bottomClampName + ".outputR", self.bsName + "." + bsItem)
        
        # print ("connection succesfully made!\n")



    def ConnectControlHorizontal(self, position, bsItem):
        #链接水平方向位置上的BS
        name = self.GetCtrName(bsItem)
        if cmds.objExists(name + "Grp"):
            if position == "right":
                rightClampName = cmds.createNode('clamp', n = name + "RightClamp")

                cmds.setAttr(rightClampName + ".maxR", 1)
                cmds.setAttr(rightClampName + ".minR", 0)

                cmds.connectAttr(name + "CircleCtrl.tx", rightClampName + ".inputR")
                cmds.connectAttr(rightClampName + ".outputR", self.bsName + "." + bsItem)
            
            elif position == "left":
                leftClampName = cmds.createNode('clamp', n = name + "LeftClamp")
                #create multiply divide node
                leftMultName = cmds.createNode('multiplyDivide', n = name + "LeftMultDivide")
                #set operation to multiply and input 2 to -1
                cmds.setAttr(leftMultName + ".operation", 1)
                cmds.setAttr(leftMultName + ".input2X", -1)

                #set clamp max and min
                cmds.setAttr(leftClampName + ".maxR", 1)
                cmds.setAttr(leftClampName + ".minR", 0)

                cmds.connectAttr(name + "CircleCtrl.tx", leftMultName + ".input1X")
                cmds.connectAttr(leftMultName + ".outputX", leftClampName + ".inputR")
                cmds.connectAttr(leftClampName + ".outputR", self.bsName + "." + bsItem)



    def ConnectControlCorners(self, position, bsItem):
        #链接斜角方向位置上的BS
        name = self.GetCtrName(bsItem)
        if cmds.objExists(name + "Grp"):
            if position == "topRight":

                topRightXClampName = cmds.createNode('clamp', n = name + "TopRightXClamp")
                topRightYClampName = cmds.createNode('clamp', n = name + "TopRightYClamp")
                topRightAddName = cmds.createNode('addDoubleLinear', n = name + "TopRightAdd")
                topRightMultName = cmds.createNode('multiplyDivide', n = name + "TopRightMultDivide")

                cmds.setAttr(topRightXClampName + ".maxR", 1)
                cmds.setAttr(topRightXClampName + ".minR", 0)
                cmds.setAttr(topRightYClampName + ".maxR", 1)
                cmds.setAttr(topRightYClampName + ".minR", 0)
                cmds.setAttr(topRightAddName + ".input2", 1)

                cmds.connectAttr(name + "CircleCtrl.tx", topRightAddName + ".input1")
                cmds.connectAttr(topRightAddName + ".output", topRightXClampName + ".inputR")

                cmds.connectAttr(name + "CircleCtrl.ty", topRightYClampName + ".inputR")

                cmds.connectAttr(topRightXClampName + ".outputR", topRightMultName + ".input1X")
                cmds.connectAttr(topRightYClampName + ".outputR", topRightMultName + ".input2X")

                cmds.connectAttr(topRightMultName + ".outputX", self.bsName + "." + bsItem)

            elif position == "bottomRight":
                bottomRightXClampName = cmds.createNode('clamp', n = name + "BottomRightXClamp")
                bottomRightYClampName = cmds.createNode('clamp', n = name + "BottomRightYClamp")

                bottomRightAddName = cmds.createNode('addDoubleLinear', n = name + "BottomRightAdd")

                bottomRightMultName = cmds.createNode('multiplyDivide', n = name + "BottomRightMultDivide")
                bottomRightYMultName = cmds.createNode('multiplyDivide', n = name + "BottomRightYMultDivide")

                cmds.setAttr(bottomRightXClampName + ".maxR", 1)
                cmds.setAttr(bottomRightXClampName + ".minR", 0)
                cmds.setAttr(bottomRightYClampName + ".maxR", 1)
                cmds.setAttr(bottomRightYClampName + ".minR", 0)
                cmds.setAttr(bottomRightAddName + ".input2", 1)
                cmds.setAttr(bottomRightYMultName + ".input2X", -1)

                cmds.connectAttr(name + "CircleCtrl.tx", bottomRightAddName + ".input1")
                cmds.connectAttr(bottomRightAddName + ".output", bottomRightXClampName + ".inputR")

                cmds.connectAttr(name + "CircleCtrl.ty", bottomRightYMultName + ".input1X")
                cmds.connectAttr(bottomRightYMultName + ".outputX", bottomRightYClampName + ".inputR")

                cmds.connectAttr(bottomRightXClampName + ".outputR", bottomRightMultName + ".input1X")
                cmds.connectAttr(bottomRightYClampName + ".outputR", bottomRightMultName + ".input2X")

                cmds.connectAttr(bottomRightMultName + ".outputX", self.bsName + "." + bsItem)

            elif position == "topLeft":
                topLeftXClampName = cmds.createNode('clamp', n = name + "TopLeftXClamp")
                topLeftYClampName = cmds.createNode('clamp', n = name + "TopLeftYClamp")

                topLeftXAddName = cmds.createNode('addDoubleLinear', n = name + "TopLeftAdd")

                topLeftMultName = cmds.createNode('multiplyDivide', n = name + "TopLeftMultDivide")
                topLeftXMultName = cmds.createNode('multiplyDivide', n = name + "TopLeftXMultDivide")

                cmds.setAttr(topLeftXClampName + ".maxR", 1)
                cmds.setAttr(topLeftXClampName + ".minR", 0)
                cmds.setAttr(topLeftYClampName + ".maxR", 1)
                cmds.setAttr(topLeftYClampName + ".minR", 0)
                cmds.setAttr(topLeftXAddName + ".input2", 1)
                cmds.setAttr(topLeftXMultName + ".input2X", -1)

                cmds.connectAttr(name + "CircleCtrl.tx", topLeftXMultName + ".input1X")

                cmds.connectAttr(topLeftXMultName + ".outputX", topLeftXAddName + ".input1")
                cmds.connectAttr(topLeftXAddName + ".output", topLeftXClampName + ".inputR")

                cmds.connectAttr(name + "CircleCtrl.ty", topLeftYClampName + ".inputR")

                cmds.connectAttr(topLeftXClampName + ".outputR", topLeftMultName + ".input1X")
                cmds.connectAttr(topLeftYClampName + ".outputR", topLeftMultName + ".input2X")

                cmds.connectAttr(topLeftMultName + ".outputX", self.bsName + "." + bsItem)

            elif position == "bottomLeft":
                bottomLeftXClampName = cmds.createNode('clamp', n = name + "BottomLeftXClamp")
                bottomLeftYClampName = cmds.createNode('clamp', n = name + "BottomLeftYClamp")

                bottomLeftXAddName = cmds.createNode('addDoubleLinear', n = name + "BottomLeftAdd")

                bottomLeftMultName = cmds.createNode('multiplyDivide', n = name + "BottomLeftMultDivide")
                bottomLeftXMultName = cmds.createNode('multiplyDivide', n = name + "BottomLeftXMultDivide")
                bottomLeftYMultName = cmds.createNode('multiplyDivide', n = name + "BottomLeftYMultDivide")

                cmds.setAttr(bottomLeftXClampName + ".maxR", 1)
                cmds.setAttr(bottomLeftXClampName + ".minR", 0)
                cmds.setAttr(bottomLeftYClampName + ".maxR", 1)
                cmds.setAttr(bottomLeftYClampName + ".minR", 0)
                cmds.setAttr(bottomLeftXAddName + ".input2", 1)
                cmds.setAttr(bottomLeftXMultName + ".input2X", -1)
                cmds.setAttr(bottomLeftYMultName + ".input2X", -1)

                cmds.connectAttr(name + "CircleCtrl.tx", bottomLeftXMultName + ".input1X")

                cmds.connectAttr(bottomLeftXMultName + ".outputX", bottomLeftXAddName + ".input1")
                cmds.connectAttr(bottomLeftXAddName + ".output", bottomLeftXClampName + ".inputR")

                cmds.connectAttr(name + "CircleCtrl.ty", bottomLeftYMultName + ".input1X")
                cmds.connectAttr(bottomLeftYMultName + ".outputX", bottomLeftYClampName + ".inputR")

                cmds.connectAttr(bottomLeftXClampName + ".outputR", bottomLeftMultName + ".input1X")
                cmds.connectAttr(bottomLeftYClampName + ".outputR", bottomLeftMultName + ".input2X")

                cmds.connectAttr(bottomLeftMultName + ".outputX", self.bsName + "." + bsItem)


    def GetCtrName(self, item):
        #通过拆分组合bs的名字找到控制器的名字
        name = item.split("_")
        ctr = name[0]
        for i in range(1, len(name) - 1):
            ctr = ctr + "_" + name[i]
        if not cmds.objExists(ctr + "Grp"):
                cmds.confirmDialog(t=u'敬告！！！', m=u'场景中缺少控制器' + ctr , b=[u'好的'], db=u'好的')
                return
        return ctr

    def ChangeBSTarget(self, *args):
        #替换blendshape目标体
        selObj = cmds.ls(sl = True, type = "transform")

        if len(selObj) != 2 :
            cmds.confirmDialog(t=u'敬告！！！', m=u'请选择两个模型，原bs + 现bs', b=[u'好的'], db=u'好的')
            return
        
        OrgAttr = selObj[0] + ".worldMesh[0]"
        CurrentAttr = selObj[1] + ".worldMesh[0]"

        if  not (cmds.objExists(OrgAttr) and cmds.objExists(CurrentAttr)):
            cmds.confirmDialog(t=u'敬告！！！', m=u'请选择两个模型，原bs + 现bs', b=[u'好的'], db=u'好的')
            return

        destination = cmds.connectionInfo(OrgAttr, destinationFromSource = True)
        if len(destination) >= 1 and cmds.objExists(destination[0]):
            cmds.disconnectAttr(OrgAttr, destination[0])
            cmds.connectAttr(CurrentAttr, destination[0])
        else:
            cmds.confirmDialog(t=u'敬告！！！', m=u'所选模型不是bsTarget', b=[u'好的'], db=u'好的')
            return
        
        self.Align(selObj[1], selObj[0])
        baseName = str(selObj[0])

        tempName = baseName.split("|")

        baseName = tempName[len(tempName) - 1]

        changObj = selObj[1]
        parentObj = cmds.listRelatives(selObj[0], parent= True)
        cmds.delete(selObj[0])
        Obj = cmds.rename(changObj, baseName)
        cmds.parent(Obj, parentObj)

    def Align(self, current, target):
        targetPos = cmds.xform(target, q=True, ws=True, t=True)
        cmds.xform(current, ws=True, t=[targetPos[0],targetPos[1],targetPos[2]])
        targetRot = cmds.xform(target, q=True, ws=True, ro=True)
        cmds.xform(current, ws=True, ro=[targetRot[0],targetRot[1],targetRot[2]])
    
    def clearUnuseNode(self):
        #清除所有没用的节点
       
        if cmds.objExists(self.bsName):
            bsAttrs = cmds.listAttr(self.bsName, s = True, m = True, r = True, c = True, k = True, v = True)
            for attr in bsAttrs:
                attrN = self.bsName + '.' + attr
                if cmds.objExists(attrN):
                    source = cmds.connectionInfo(attrN, sourceFromDestination = True)
                    if cmds.objExists(source):
                        cmds.disconnectAttr(source, attrN)


        mel.eval('hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes");')


FacialConnectWin()