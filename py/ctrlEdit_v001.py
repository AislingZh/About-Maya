# 对控制器进行修改
#   1.控制器大小，放大缩小
#   2.控制器位移，各个轴向的移动
#   3.控制器在原地的旋转
#   4.控制器颜色
#   5.控制器形状替换

import maya.cmds as cmds
import maya.mel as mel





    
WINDOW_NAME = "CtrlEditUi"

SELECT_NUM = cmds.ls(sl = True)

def CtrlEditUI():
    
    if cmds.window(WINDOW_NAME, exists = True):
        cmds.deleteUI(WINDOW_NAME, window = True)

    # super(CtrlEditUI, ).__init__()
    # CurveChange.__init__()

    main_window = cmds.window(WINDOW_NAME, title =  "Curve Edit", rtf = True,  menuBar=True)
    # main_layout = cmds.formLayout(parent = main_window)

    cmds.menu( label='Help', helpMenu=True )
    cmds.menuItem( 'Application..."', label='"About' )




    cmds.rowLayout(numberOfColumns=3, columnAttach = (1, "right", 2), columnWidth = (1, 100))
    cmds.text(label="mirror temp:   ", w=200 )
    cmds.textField("mirTemp", w = 150, text="h_")

    cmds.setParent( '..' )

    cmds.rowLayout(numberOfColumns=3, columnAttach = (1, "both", 2), columnWidth = (50, 100))
    cmds.text(label="镜像控制器:   " , w=200)
    cmds.button(label="左→右", h = 20, w=150, command = "mirrorCtrlsL_to_R()")
    cmds.button(label="右→左", h = 20, w=150, command = "mirrorCtrlsR_to_L()")
    
    cmds.setParent( '..' )
    cmds.radioButtonGrp("all_select_type", label = 'Select type:', labelArray3=['select', 'hierarchy', 'all'], numberOfRadioButtons = 3, columnWidth4 = (80, 70, 70, 70), select = 1)
    
    cmds.setParent( '..' )
    cmds.frameLayout("Scale:", collapsable = True, labelVisible=1, marginWidth=5,marginHeight=5,borderStyle='etchedOut' )
    cmds.columnLayout(adj=1)

    cmds.separator( height=10,style='in' )

    shrink_button = cmds.button(label = "Shrink",h=25,command = "shrinkCon()")

    magnify_button = cmds.button(label = "Magnify",h=25, command = "magnifyCon()")

    scale_slider = cmds.floatSliderButtonGrp(
         'scaleFSBG', label = 'Curve scale : ', 
         field = True, minValue = 0, maxValue = 10,
         fieldMaxValue=10,value=1,
         buttonLabel='CurveScale',
         buttonCommand = "changScale()",
         columnWidth4=(80,70,70, 10))


    cmds.separator( height=10,style='in' )

    cmds.setParent( '..' )
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
    tran_button = cmds.button(label = "Move",h=25, command = "changeTran()")

    cmds.separator(height = 10, style = 'in')

    cmds.setParent( '..' )
    cmds.setParent( '..' )

    cmds.frameLayout("Rotate:", collapsable = True, labelVisible = 1, marginWidth = 5, marginHeight = 5, borderStyle = 'stchedOut')
    cmds.separator(height = 10, style = 'in')
    rot_x_slider = cmds.floatSliderGrp(
                    'rot_x_FSG', label = 'X : ',
                    field = True, minValue = -360, maxValue = 360,
                    fieldMaxValue = 360, value = 0,
                    columnWidth3=(20,50,10))
    rot_y_slider = cmds.floatSliderGrp(
                    'rot_y_FSG', label = 'Y : ',
                    field = True, minValue = -360, maxValue = 360,
                    fieldMaxValue = 360, value = 0,
                    columnWidth3=(20,50,10))
    rot_z_slider = cmds.floatSliderGrp(
                    'rot_z_FSG', label = 'Z : ',
                    field = True, minValue = -360, maxValue = 360,
                    fieldMaxValue = 360, value = 0,
                    columnWidth3=(20,50,10))
    rot_button = cmds.button(label = "Rotate",h=25, command = "changeRotate()")

    cmds.separator(height = 10, style = 'in')
    cmds.frameLayout("Shape:", collapsable = True, labelVisible = 1, marginWidth = 5, marginHeight = 5, borderStyle = 'stchedOut')
    cmds.separator(height = 10, style = 'in')
    shape_button = cmds.button(label = "ChangeShape", h = 25, command = "changeShape()")
    cmds.separator(height = 10, style = 'in')

    cmds.setParent( '..' )
    cmds.setParent( '..' )

    cmds.frameLayout("Color:", collapsable = True, labelVisible = 1, marginWidth = 5, marginHeight = 5, borderStyle = 'stchedOut')
    cmds.separator(height = 10, style = 'in')
    red_button = cmds.button(label = "red", h = 25, command = "redColorSet()")
    yellow_button = cmds.button(label = "Yellow", h = 25, command = "yellowColorSet()")
    blue_button = cmds.button(label = "Blue", h = 25, command = "blueColorSet()")
    color_slider= cmds.colorIndexSliderGrp('cvColorCISG',label='Curve Color:', min=1, max=32, value=1,columnWidth3=(80,50,10) )
    color_button = cmds.button(label = "SetColor", h = 25, command = "changeColor()")
    cmds.separator(height = 10, style = 'in')

    # cmds.setParent( '..' )
    # cmds.setParent( '..' )
    # cmds.rowLayout(numberOfColumns=3, columnAttach = (1, "right", 2), columnWidth = (1, 100))
    # cmds.text(label="mirror temp:   ", w=200 )
    # cmds.textField("mirTemp", w = 150, text="_h")

    # cmds.setParent( '..' )

    # cmds.rowLayout(numberOfColumns=3, columnAttach = (1, "both", 2), columnWidth = (50, 100))
    # cmds.text(label="镜像控制器:   " , w=200)
    # cmds.button(label="左→右", h = 20, w=150, command = "")
    # cmds.button(label="右→左", h = 20, w=150, command = "")

    cmds.showWindow(main_window)


    
def shrinkCon():
    conScale(0.8, 0.8, 0.8)

def magnifyCon():
    conScale(1.2, 1.2, 1.2)

def changScale():
    scale_num = cmds.floatSliderButtonGrp('scaleFSBG', q = True, value = True)
    conScale(scale_num, scale_num, scale_num)

def changeTran():
    tran_x_num = cmds.floatSliderGrp('tran_x_FSG', q = True, value = True)
    tran_y_num = cmds.floatSliderGrp('tran_y_FSG', q = True, value = True)
    tran_z_num = cmds.floatSliderGrp('tran_z_FSG', q = True, value = True)
    conTran(tran_x_num, tran_y_num, tran_z_num)

def changeRotate():
    rot_x_num = cmds.floatSliderGrp('rot_x_FSG', q = True, value = True)
    rot_y_num = cmds.floatSliderGrp('rot_y_FSG', q = True, value = True)
    rot_z_num = cmds.floatSliderGrp('rot_z_FSG', q = True, value = True)
    conRotate(rot_x_num, rot_y_num, rot_z_num)

def redColorSet():
    _doColor(13)
def yellowColorSet():
    _doColor(17)
def blueColorSet():
    _doColor(6)

def changeColor():
    color_value = cmds.colorIndexSliderGrp('cvColorCISG', q = True, value = True)
    _doColor(color_value - 1)

def conScale(x = None, y = None, z =None):
    ops = {'objectSpace':True, 'absolute':True}
    _doTransform(cmds.scale, x, y, z, ops)

def conTran(x = None, y = None, z = None):
    ops = {'relative':True, 'objectSpace':True, 'worldSpaceDistance':True}
    _doTransform(cmds.move, x, y, z, ops)

def conRotate(x = None, y = None, z = None):
    ops = {'translate':True, 'objectSpace':True, 'absolute':True}
    _doTransform(cmds.rotate, x, y, z, ops);

def _doTransform(func, x, y, z, ops):
    cmds.undoInfo(openChunk=True)
    try:
        UpdateSelObj()
        for i in SELECT_NUM:
            j = cmds.listRelatives(i, parent = True)
            cmds.select(j, r=True )
            mel.eval('selectCurveCV ("all");')
            func(x, y, z, **ops)
            cmds.select(clear = True)
    except:
        print 'something wrong…'
        cmds.undoInfo(closeChunk=True)
    cmds.undoInfo(closeChunk=True)

def changeShape():
    # 替换形状
    cmds.undoInfo(openChunk = True)
    try:
        UpdateSelObj()
        if len(SELECT_NUM) > 1:
            for i in range(1,len(SELECT_NUM)):
                cmds.connectAttr(SELECT_NUM[0] + '.worldSpace[0]', SELECT_NUM[i] + '.create', f=True)
                cmds.refresh()
                cmds.disconnectAttr(SELECT_NUM[0] + '.worldSpace[0]', SELECT_NUM[i] + '.create')
        else:
            print 'Please Ctrls......'
    except Exception as e:
        raise e


def _doColor(val):
    # 改变颜色
    cmds.undoInfo(openChunk = True)
    try:
        UpdateSelObj()
        for i in SELECT_NUM:
            if val == 0:
                cmds.setAttr(i + '.overrideEnabled', 0)
                cmds.setAttr(i + '.overrideColor', 0)
            else:
                cmds.setAttr(i + '.overrideEnabled', 1)
                cmds.setAttr(i + '.overrideColor', val)
    except Exception as e:
        raise e

def UpdateSelObj():
    try:
        global SELECT_NUM
        selObj = cmds.ls(sl = True)
        select_type = cmds.radioButtonGrp("all_select_type", q = True, select = True)
        if len(selObj) > 0:
            if select_type == 1:
                SELECT_NUM = cmds.listRelatives(selObj, shapes = True)
            if select_type == 2:
                # 需要找到层级下的曲线
                SELECT_NUM = cmds.listRelatives(selObj, allDescendents = True, type = "nurbsCurve") 
            if select_type == 3:
                SELECT_NUM = cmds.ls(type = "nurbsCurve")
    except Exception as e:
        raise e

def mirrorCtrlsR_to_L():
    mirTemp = cmds.textField("mirTemp", q = True, text = True)
    mirStrA = mirTemp.replace('h', 'R')
    mirStrB = mirTemp.replace('h', 'L')
    mirrorCtrls(mirStrA, mirStrB)

def mirrorCtrlsL_to_R():
    mirTemp = cmds.textField("mirTemp", q = True, text = True)
    mirStrA = mirTemp.replace('h', 'R')
    mirStrB = mirTemp.replace('h', 'L')
    mirrorCtrls(mirStrB, mirStrA)

#通过控制器的set来获取所有的控制器曲线，再进行镜像
def mirrorCtrls(strA, strB):
    cmds.undoInfo(openChunk=True)
    try:
        masterCtrlSetName = 'CTRL_SET'
        if cmds.objExists(masterCtrlSetName):
            setMemberList = cmds.listConnections(masterCtrlSetName+'.dagSetMembers', s=True, d=False)
            for member in setMemberList:
                if strA in member and member.replace(strA, strB) in setMemberList:
                    pointNumA = cmds.getAttr(member+'.controlPoints', size=True)
                    pointNumB = cmds.getAttr(member.replace(strA, strB)+'.controlPoints', size=True)
                    if pointNumA==pointNumB:
                        for point in range(pointNumA):
                            pos = cmds.pointPosition(member+'.cv['+str(point)+']', w=True)
                            cmds.move(-pos[0], pos[1], pos[2], member.replace(strA, strB)+'.cv['+str(point)+']', a=True)
        else:
            message = QtGui.QMessageBox(self)
            message.setText(u'错误：\n'+masterCtrlSetName+u'不存在，请检查文件是否损坏！！！')
            message.setWindowTitle('Error!')
            message.setIcon(QtGui.QMessageBox.Warning)
            button = QtGui.QPushButton()
            button.setText('OK')
            message.addButton(button, QtGui.QMessageBox.DestructiveRole)
            message.setDefaultButton(button)
            message.exec_()
            return
        cmds.undoInfo(closeChunk=True)
    except:
        print 'something wrong…'
        cmds.undoInfo(closeChunk=True)
CtrlEditUI()