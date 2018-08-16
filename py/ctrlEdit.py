# 对控制器进行修改
#   1.控制器大小，放大缩小
#   2.控制器位移，各个轴向的移动
#   3.控制器在原地的旋转
#   4.控制器颜色
#   5.控制器形状替换

import maya.cmds as cmds
import maya.mel as mel

class CurveChange():

    def conScale(self, selObj = None, x = None, y = None, z =None):
        ops = {'objectSpace':True, 'absolute':True}
        self._doTransform(cmds.scale, selObj, x, y, z, ops)

    def conTran(self, selObj = None, x = None, y = None, z = None):
        ops = {'objectSpace':True, 'absolute':True}
        self._doTransform(cmds.move, selObj, x, y, x, ops)

    def conRotate(self, selObj = None, x = None, y = None, z = None):
        ops = {'translate':True, 'objectSpace':True, 'absolute':True}
        self._doTransform(cmds.rotate, selObj, x, y, z, ops);

    # def _doTransform(self, func, x, y, z, ops):
    #   for name in ('x','y','z'):
    #        val = locals()[name]
    #        if val is not None:
    #           mel.eval('selectCurveCV ("all")');
    #           func(val, self.name, **ops)

    def _doTransform(self, func, selObj, x, y, z, ops):
        cmds.undoInfo(openChunk=True)
        try:
            cmds.select(selObj, r=True )
            mel.eval('selectCurveCV ("all");')
            func(x, y, z, **ops)
        except:
            print 'something wrong…'
            cmds.undoInfo(closeChunk=True)
        cmds.undoInfo(closeChunk=True)

    # def curveShape(self, baseObj, changeObj):
    #     # 替换形状


    def SetColor(self, selObj, val):
        # 改变颜色
        cmds.undoInfo(openChunk = True)
        try:
            shape = cmds.listRelatives(selObj, s = 1)
            if val == 0:
                cmds.setAttr(shape[0] + '.overrideEnabled', 0)
                cmds.setAttr(shape[0] + '.overrideColor', 0)
            else:
                cmds.setAttr(shape[0] + '.overrideEnabled', 1)
                cmds.setAttr(shape[0] + '.overrideColor', val)

        except Exception as e:
            raise e



class CtrlEditUI():
    
    WINDOW_NAME = "CtrlEditUi"

    FORM_OFFSET = 2

    SELECT_NUM = cmds.ls(sl = True)


    """docstring for CtrlEditUI"""
    def __init__(self):
        
        if cmds.window(self.WINDOW_NAME, exists = True):
            cmds.deleteUI(self.WINDOW_NAME, window = True)

        # super(CtrlEditUI, self).__init__()
        # CurveChange.__init__(self)

        main_window = cmds.window(self.WINDOW_NAME, title =  "Curve Edit", rtf = True,  menuBar=True)
        # main_layout = cmds.formLayout(parent = main_window)

        cmds.menu( label='Help', helpMenu=True )
        cmds.menuItem( 'Application..."', label='"About' )


        cmds.radioButtonGrp("all_select_type", label = 'select type:', labelArray3=['select', 'hierarchy', 'all'], numberOfRadioButtons = 3, columnWidth4 = (80, 70, 70, 70), select = 1)



        cmds.frameLayout("Scale:", collapsable = True, labelVisible=1, marginWidth=5,marginHeight=5,borderStyle='etchedOut' )
        cmds.columnLayout(adj=1)

        cmds.separator( height=10,style='in' )

        shrink_button = cmds.button(label = "shrink",h=25,command = "shrinkCon()")

        magnify_button = cmds.button(label = "magnify",h=25, command = "magnifyCon()")

        scale_slider = cmds.floatSliderButtonGrp(
            'scaleFSBG', label = 'curve scale : ', 
            field = True, minValue = -10, maxValue = 10,
             fieldMaxValue=10,value=1,
             buttonLabel='CurveScale',
             buttonCommand = 'changScale',
             columnWidth4=(80,70,70, 10))


        cmds.separator( height=10,style='in' )

        cmds.setParent( '..' )


        cmds.frameLayout("Translate:", collapsable = True, labelVisible = 1, marginWidth = 5, marginHeight = 5, borderStyle = 'stchedOut')
        cmds.separator(height = 10, style = 'in')
        tran_x_slider = cmds.floatSliderGrp(
                        'tran_x_FSG', label = 'X : ',
                        field = True, minValue = -10, maxValue = 10,
                        fieldMaxValue = 10, value = 0,
                        columnWidth3=(20,50,10))
        tran_y_slider = cmds.floatSliderGrp(
                        'tran_y_FSG', label = 'Y : ',
                        field = True, minValue = -10, maxValue = 10,
                        fieldMaxValue = 10, value = 0,
                        columnWidth3=(20,50,10))
        tran_z_slider = cmds.floatSliderGrp(
                        'tran_z_FSG', label = 'Z : ',
                        field = True, minValue = -10, maxValue = 10,
                        fieldMaxValue = 10, value = 0,
                        columnWidth3=(20,50,10))
        tran_button = cmds.button(label = "move",h=25, command = "changeTran()")

        cmds.separator(height = 10, style = 'in')

        cmds.frameLayout("Rotate:", collapsable = True, labelVisible = 1, marginWidth = 5, marginHeight = 5, borderStyle = 'stchedOut')
        cmds.separator(height = 10, style = 'in')
        rot_x_slider = cmds.floatSliderGrp(
                        'rot_x_FSG', label = 'X : ',
                        field = True, minValue = -10, maxValue = 10,
                        fieldMaxValue = 10, value = 0,
                        columnWidth3=(20,50,10))
        rot_y_slider = cmds.floatSliderGrp(
                        'rot_y_FSG', label = 'Y : ',
                        field = True, minValue = -10, maxValue = 10,
                        fieldMaxValue = 10, value = 0,
                        columnWidth3=(20,50,10))
        rot_z_slider = cmds.floatSliderGrp(
                        'rot_z_FSG', label = 'Z : ',
                        field = True, minValue = -10, maxValue = 10,
                        fieldMaxValue = 10, value = 0,
                        columnWidth3=(20,50,10))
        rot_button = cmds.button(label = "rotate",h=25, command = "changeRotate()")

        cmds.separator(height = 10, style = 'in')

        cmds.frameLayout("Shape:", collapsable = True, labelVisible = 1, marginWidth = 5, marginHeight = 5, borderStyle = 'stchedOut')
        cmds.separator(height = 10, style = 'in')
        shape_button = cmds.button(label = "changeShape", h = 25, command = "changeShape()")
        cmds.separator(height = 10, style = 'in')

        cmds.frameLayout("Color:", collapsable = True, labelVisible = 1, marginWidth = 5, marginHeight = 5, borderStyle = 'stchedOut')
        cmds.separator(height = 10, style = 'in')
        red_button = cmds.button(label = "red", h = 25, command = "redColorSet()")
        yellow_button = cmds.button(label = "yellow", h = 25, command = "yellowColorSet()")
        blue_button = cmds.button(label = "blue", h = 25, command = "self.blueColorSet")
        color_slider= cmds.colorIndexSliderGrp('cvColorCISG',label='curve Color:', min=1, max=32, value=1,columnWidth3=(80,50,10) )
        color_button = cmds.button(label = "setColor", h = 25, command = "self.changeColor")
        cmds.separator(height = 10, style = 'in')

        cmds.showWindow(main_window)

    def getSelectType(self):
        select_type = cmds.radioButtonGrp("all_select_type", q = True, select = True)
        if select_type == 1:
            SELECT_NUM = cmds.ls(sl = True)
        if select_type == 2:
            selCurve = cmds.ls(sl = True)
            # 需要找到层级下的曲线
            selchildren = cmds.listRelatives(selCurve, allDescendents = True) 
            SELECT_NUM = selCurve + selchildren
        if select_type == 3:
            SELECT_NUM = cmds.ls(type = "curve")

    def shrinkCon(self):
        CurveChange().conScale(0.8, 0.8, 0.8)

    def magnifyCon(self):
        CurveChange().conScale(self, 1.2, 1.2, 1.2)

    def changScale(self):
        scale_num = cmds.floatSliderButtonGrp('scaleFSBG', q = True, value = True)
        CurveChange().conScale(self, scale_num, scale_num, scale_num)

    def changeTran(self):
        tran_x_num = cmds.floatSliderGrp('tran_x_FSG', q = True, value = True)
        tran_y_num = cmds.floatSliderGrp('tran_y_FSG', q = True, value = True)
        tran_z_num = cmds.floatSliderGrp('tran_z_FSG', q = True, value = True)
        CurveChange().conTran(self, tran_x_num, tran_y_num, tran_z_num)

    def changeRotate(self):
        rot_x_num = cmds.floatSliderGrp('rot_x_FSG', q = True, value = True)
        rot_y_num = cmds.floatSliderGrp('rot_y_FSG', q = True, value = True)
        rot_z_num = cmds.floatSliderGrp('rot_z_FSG', q = True, value = True)
        CurveChange().conRotate(self, rot_x_num, rot_y_num, rot_z_num)

    def redColorSet(self):
        for i in SELECT_NUM:
            SetColor(i, 6)
    def yellowColorSet(self):
        for i in SELECT_NUM:
            CurveChange().SetColor(i, 17)
    def blueColorSet(self):
        for i in SELECT_NUM:
            CurveChange().SetColor(i, 13)

    def changeColor(self):
        color_value = cmds.colorIndexSliderGrp('cvColorCISG', q = True, value = True)
        for i in SELECT_NUM:
            CurveChange(i).SetColor(color_value)

    def changeShape(self):
        selObjShape = cmds.ls(sl = True)
        for i in range(1, len(selObjShape)):
            CurveChange().curveShape(selObjShape[0], selObjShape[i])

    def SetColor(self, selObj, val):
        # 改变颜色
        cmds.undoInfo(openChunk = True)
        try:
            shape = cmds.listRelatives(selObj, s = 1)
            if val == 0:
                cmds.setAttr(shape[0] + '.overrideEnabled', 0)
                cmds.setAttr(shape[0] + '.overrideColor', 0)
            else:
                cmds.setAttr(shape[0] + '.overrideEnabled', 1)
                cmds.setAttr(shape[0] + '.overrideColor', val)

        except Exception as e:
            raise e

