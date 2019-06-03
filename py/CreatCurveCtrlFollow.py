#给曲线创建跟随控制器
#步骤：
#创建绳子控制器，个数可设置
#给曲线创建相应个数的pointOnCurve节点，并连接控制器
#给控制器设置切线约束（用选定曲线和设置的骨骼）和缩放约束（用设定骨骼的控制器）
import maya.cmds as cmds

class CreatCurveCtrl():
    """docstring for CreatCurveCtrl"""
    WINDOW_NAME = "CreatCurveCtrlFollowUI"

    numOffset = 0

    POCNodes = []

    def showUI(self):

        if cmds.window(self.WINDOW_NAME, exists = True):
            cmds.deleteUI(self.WINDOW_NAME, window = True)

        main_window = cmds.window(self.WINDOW_NAME, title =  "Curve Edit", w = 320, h = 200, sizeable = 1)
        
        cmds.columnLayout(w = 250, columnOffset = ("left", 10))
        cmds.columnLayout(h =3)
        cmds.setParent( '..' ) 

        cmds.columnLayout(w = 270, columnOffset = ("left", 2))
        cmds.setParent( '..' )

        cmds.rowLayout( numberOfColumns = 2, columnAttach=(1, 'right', 2), columnWidth = (1, 95) )

        selcurveButton = cmds.button("curveButton", label = "select Curve", h = 25, command = self.selCurve)
        jntTextField = cmds.textField("curvename", text = "", en = 1, w = 180 )

        cmds.setParent( '..' )

        cmds.rowLayout( numberOfColumns = 2, columnAttach=(1, 'right', 2), columnWidth = (1, 100) )

        seljntButton = cmds.button("jntButton", label = "select wordUp", h = 25, command = self.selJoint)
        jntTextField = cmds.textField("jntname", text = "", en = 1, w = 180 )

        cmds.setParent( '..' )

        cmds.rowLayout( numberOfColumns = 1, columnAttach=(1, 'both', 0), columnWidth3=(80, 75, 150) )
        #cmds.rowLayout( numberOfColumns=3, columnWidth3=(80, 75, 150), adjustableColumn=2, columnAlign=(1, 'right'), columnAttach=[(1, 'both', 0), (2, 'both', 0), (3, 'both', 0)] )

        #cmds.separator(height = 10, style = 'in')
        CtrNum_slider = cmds.intSliderGrp(
                    'ctrNum', label = '控制器数量 : ',
                    field = True, minValue = 1, maxValue = 10,
                    fieldMaxValue = 10, value = 1,
                    columnWidth3=(80,30,150))
        cmds.setParent( '..' )


        #cmds.separator(height = 10, style = 'in')
        #cmds.separator(height = 10, style = 'in')
        cmds.columnLayout( w = 270, columnOffset = ("left", 20))

        creatcon_button = cmds.button(label = "create con", align = "center", w = 250, h = 30, command = self.CurveCtr)
        cmds.setParent( '..' )
        
        #cmds.separator(height = 10, style = 'in')

        cmds.showWindow(main_window)


    def selJoint(self, *args):
        self.selectObj('jntname','joint')

    def selCurve(self, *args):
        self.selectObjB('curvename','nurbsCurve')

    def selectObj(self, objName, t):
        obj = cmds.ls(sl = True, type = t)
        if len(obj) != 1:
            return
        cmds.textField(objName, e = True, text = obj[0])

    def selectObjB(self, objName, t):
        obj = cmds.ls(sl = True)
        objShape = cmds.listRelatives(obj[0], s = True)
        if len(obj) != 1 and cmds.nodeType(obj) != t :
            return
        cmds.textField(objName, e = True, text = obj[0])

    def CurveCtr(self, *args):
        ctrNum = cmds.intSliderGrp('ctrNum', q = True, value = True)
        selCurve = cmds.textField("curvename", q = True, text = True)
        selJnt = cmds.textField("jntname", q = True, text = True)
        global POCNodes
        self.doNumOffset(selCurve)
        print ctrNum,selCurve,selJnt
        try:
            if ctrNum < 1:
                return
            for i in range(0,ctrNum):
                print "im in for circle"
                jntCtrGrp = self.creatJntCtr(selCurve + "_Jnt" + str(i + self.numOffset))
                print jntCtrGrp
                POCNode = self.creatPointOnCurve(selCurve, jntCtrGrp + "_poc")
                self.POCNodes.append(POCNode)
                print"im out poc"
                print POCNode
                cmds.connectAttr(POCNode + ".position" , jntCtrGrp + ".translate")
                cmds.tangentConstraint(selCurve, jntCtrGrp, w = 1, aimVector = (1,0,0), worldUpType = "objectrotation", worldUpVector = (0,1,0), worldUpObject = selJnt)
                cmds.scaleConstraint(selJnt + "_Ctrl", jntCtrGrp, mo = True, w = 1)
            self.changePosUI()
        except Exception as e:
            raise e

    def doNumOffset(self, name):
        global numOffset
        for i in range(0,100):
            print "asd"
            if not(cmds.objExists(name + "_Jnt" + str(i))):
                self.numOffset = i
                return


    def creatJntCtr(self, jntName):
        print "im in  creatJntCtr"
        cmds.undoInfo(openChunk=True)
        cmds.select(cl = True)
        try:
            jnt = cmds.joint(name = jntName)
            shape = cmds.circle(c=(0,0,0), nr = (1, 0, 0), sw = 360, r = 1, d = 3, ut = 0, tol = 0.00155, s = 8, ch = 0, n = jnt + "_Con")
            print jnt, shape[0]
            self.Align(shape[0], jnt)
            cmds.parent(jnt, shape[0])
            grp = cmds.group(shape[0], r = True, n = shape[0] + "Grp")
            print grp
            return grp
        except Exception as e:
            print 'creatJntCtr something wrong...'
            cmds.undoInfo(closeChunk=True)
        

    def creatPointOnCurve(self,curve,nodeName):
        print "im in  creatPointOnCurve"
        cmds.undoInfo(openChunk=True)
        print "poc"
        try:
            poc = cmds.pointOnCurve(curve, ch = True)
            poc = cmds.rename(poc, nodeName)
            cmds.setAttr(poc + ".turnOnPercentage", 1)
            print poc
            return poc
        except Exception as e:
            print 'creatPointOnCurve something wrong...'
            cmds.undoInfo(closeChunk=True)

    def Align(self, current, target):
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
        
    def changePosUI(self):
        if cmds.window("change", exists = True):
            cmds.deleteUI("change", window = True)
        window = cmds.window("change",title='ChangePos')
        cmds.columnLayout()
        Num = cmds.intSliderGrp('ctrNum', q = True, value = True)
        for i in range(0,Num):
            cmds.floatSliderGrp("PosFSG" + str(i + self.numOffset), label="curveJnt" + str(i + self.numOffset) + "_poc:", field=True,minValue=0.000, maxValue=1.000, fieldMinValue=0.000, fieldMaxValue=1.000, value=0.000, dragCommand = "CreatCurveCtrl().PosValue(" +  str(i) + ")" )
        cmds.showWindow( window )

    def PosValue(self, i):
        print i
        val = cmds.floatSliderGrp("PosFSG" + str(int(i) + self.numOffset) , q = True, value = True)
        print val
        cmds.setAttr(self.POCNodes[int(i)]+ ".parameter", val)

CreatCurveCtrl().showUI()