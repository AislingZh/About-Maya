import maya.cmds as cmds
import maya.mel as mel
import maya.cmds as mc


WINDOW_NAME = "FACEUI"

SELECT_NUM = cmds.ls(sl = True)

def FACEUI():
    
    if cmds.window(WINDOW_NAME, exists = True):
        cmds.deleteUI(WINDOW_NAME, window = True)

    # super(CtrlEditUI, ).__init__()
    # CurveChange.__init__()

    main_window = cmds.window(WINDOW_NAME, title =  "FACE Edit", rtf = True,  menuBar=True)
    # main_layout = cmds.formLayout(parent = main_window)

    cmds.menu( label='Help', helpMenu=True )
    cmds.menuItem( 'Application..."', label='"About' )

    cmds.frameLayout("FaceA:", collapsable = True, labelVisible=1, marginWidth=5,marginHeight=5,borderStyle='etchedOut' )
    cmds.columnLayout(adj=1)
    
    Import_button = cmds.button(label = "Import_FaceA",h=25,command = "Import_FaceAtCon()")
    cmds.separator( height=10,style='in' )
    Mirror_button = cmds.button(label = "Mirror",h=25,command = "mirrorCon()")
    cmds.setParent( '..' )
    cmds.setParent( '..' )
    
    cmds.frameLayout("FaceB:", collapsable = True, labelVisible=1, marginWidth=5,marginHeight=5,borderStyle='etchedOut' )
    cmds.columnLayout(adj=1)
    
    Import_button = cmds.button(label = "Import_FaceB",h=25,command = "Import_FaceBtCon()") 

    
    cmds.separator( height=5,style='in' )
    cmds.separator( height=5,style='in' )

    Moth_button = cmds.button(label = "Moth_Mirror",h=25,command = "MothCon()")
    cmds.separator( height=10,style='in' )    
    Eye_button = cmds.button(label = "Eye_Mirror",h=25,command = "EyeCon()")

    cmds.separator( height=10,style='in' )


    cmds.showWindow(main_window)

def mirrorCon():
    selList = mc.ls(sl=True)
    pos = mc.xform(selList[0], q=True, ws=True, t=True)
    rotation = mc.xform(selList[0], q=True, ws=True, ro=True)
    scale = mc.getAttr(selList[0]+'.s')[0]
    name = selList[0].replace('_L_','_R_')
    if mc.objExists(name):
        mc.xform(name, ws=True, t=[-pos[0],pos[1],pos[2]])
        mc.xform(name, ws=True, ro=[rotation[0],-rotation[1],-rotation[2]])
        mc.setAttr(name+'.s',scale[0],scale[1],scale[2],type='double3')
    else:
        mc.confirmDialog( title='Confirm', message=u'没有找到名称为 %s 的物体！！！！！！！'%name, button='OK')   
        
def MothCon():
    selList = mc.ls(sl=True)
    pos = mc.xform(selList[0], q=True, ws=True, t=True)
    rotation = mc.xform(selList[0], q=True, ws=True, ro=True)
    scale = mc.getAttr(selList[0]+'.s')[0]
    name = selList[0].replace('L_','R_')
    if mc.objExists(name):
        mc.xform(name, ws=True, t=[-pos[0],pos[1],pos[2]])
        mc.xform(name, ws=True, ro=[rotation[0],-rotation[1],-rotation[2]])
        mc.setAttr(name+'.s',scale[0],scale[1],scale[2],type='double3')
    else:
        mc.confirmDialog( title='Confirm', message=u'没有找到名称为 %s 的物体！！！！！！！'%name, button='OK')   

def EyeCon():
    import maya.cmds as mc
    selList = mc.ls(sl=True)
    pos = mc.xform(selList[0], q=True, ws=True, t=True)
    rotation = mc.xform(selList[0], q=True, ws=True, ro=True)
    scale = mc.getAttr(selList[0]+'.s')[0]
    name = selList[0].replace('_L_','_R_')
    if mc.objExists(name):
        mc.xform(name, ws=True, t=[-pos[0],pos[1],pos[2]])
        mc.xform(name, ws=True, ro=[rotation[0] + 180,-rotation[1],-rotation[2]])
        mc.setAttr(name+'.s',scale[0],scale[1],scale[2],type='double3')
    else:
        mc.confirmDialog( title='Confirm', message=u'没有找到名称为 %s 的物体！！！！！！！'%name, button='OK')

def Import_FaceAtCon():
    cmds.file('Y:/OldFile/W_Projects/Phoenix/reference/各环节制作规范/绑定/PH_Face_Temp.mb', i=True, f=True)
    
def Import_FaceBtCon():
    cmds.file('Y:/OldFile/W_Projects/Phoenix/reference/各环节制作规范/绑定/PH_FaceB_Temp.mb', i=True, f=True)    
FACEUI()