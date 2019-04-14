# ------------------------------------------------------------------------------------------------------------//
# ------------------------------------------------------------------------------------------------------------//
# 	SCRIPT:	ZHY_RootMotionForUE4.py
# 	VERSION: 0.5
# 	AUTHOR:	Aislingzh
# 			Aislingzh@qq.com
# 	DATE:		02 14, 2019
	

# 	DESCRIPTION:	 
# 			一制作ue4的根骨骼运动

# ------------------------------------------------------------------------------------------------------------//	
# ------------------------------------------------------------------------------------------------------------//
##制作ue4根骨骼动画（RootMotion）
##利用约束把质心骨骼的动画数据烘焙到位于原点的根骨骼上，translate 上烘焙x和Z轴，rotate上烘焙y轴
##
# ------------------------------------------------------------------------------------------------------------//


import maya.cmds as cmds
import maya.mel as mel
class ZHY_RootMotionForUE4(object):
    
    WINDOW_NAME = "ZHY_RootMotionForUE4"

    def __init__(self):


        if cmds.window(self.WINDOW_NAME, exists = True):
            cmds.deleteUI(self.WINDOW_NAME, window = True)
        
        main_window = cmds.window(self.WINDOW_NAME, title =  "ZHY_RootMotionForUE4", rtf = True,  menuBar=True)

        cmds.menu( label='Help', helpMenu=True )
        cmds.menuItem( 'Application..."', label='"About' )

        cmds.columnLayout(adj=1)
        cmds.frameLayout( label='constraint axes:' )

        cmds.checkBoxGrp("translateAxes", numberOfCheckBoxes=3, label='translate', labelArray3=['X', 'Y', 'Z'], valueArray3 = [True, False, True], enable1 = False, enable3 = False )
        cmds.checkBoxGrp("rotateAxes", numberOfCheckBoxes=3, label='rotate', labelArray3=['X', 'Y', 'Z'], valueArray3 = [False, True, False], enable1 = False, enable3 = False )

        cmds.separator( height=5,style='in' )


        cmds.setParent( '..' )

        # cmds.frameLayout("Export:", collapsable = True, labelVisible=1, marginWidth=5,marginHeight=5,borderStyle='etchedOut' )
        cmds.columnLayout(adj=1)
        cmds.separator( height=5,style='in' )

        startNum = cmds.playbackOptions(q = True , ast = True)
        cmds.intFieldGrp("StartFrame", numberOfFields=1, label='StartFrame', value1=startNum )
        endNum = cmds.playbackOptions(q = True , aet = True)
        cmds.intFieldGrp("EndFrame", numberOfFields=1, label='EndFrame', value1=endNum )

        Anim_button = cmds.button(label = "Bake anim",h=25,command = self.Constraints )
        cmds.separator( height=10,style='in' )    


        cmds.showWindow(main_window)
    
    def Constraints(self, *args):
        # creat a loc
        # creat constrain rootM to loc, all 
        # bake anim for loc
        # rootm --> parent -w
        # rootm delete keyfarme
        # creat constrain loc to root ,tx,tz, rz
        # parent(rootm, root) 
        # creat constrain loc to root ,all

        # startNum = cmds.playbackOptions(q = True , ast = True)
        # endNum = cmds.playbackOptions(q = True , aet = True)

        # returnMess = cmds.confirmDialog( title='Confirm', message='烘焙时间轴为' + str(startNum) + '-' + str(endNum), button=['Yes','No'], defaultButton='Yes', cancelButton='No', dismissString='No' )
        # if returnMess == "No":
        #     return
        startNum = cmds.intFieldGrp("StartFrame", q = True, value1 = True)
        endNum = cmds.intFieldGrp("EndFrame", q = True, value1 = True)
        cmds.currentUnit( time='ntsc', linear='centimeter')
        cmds.currentTime( startNum )

        locPos = cmds.spaceLocator()
        cmds.parentConstraint( 'Root_M', locPos, mo = True)
        

        cmds.bakeResults( locPos, simulation=True, t = (startNum, endNum), hierarchy= "below",  sb = 1, dic = True, pok = True, ral = False, rwl = False, cp = True)

        cmds.parent( 'Root_M', world=True )
        keyframelist = cmds.ls(type='animCurveTL')+cmds.ls(type='animCurveTA')+cmds.ls(type='animCurveTU')
        for i in keyframelist:
            if not ('Root_M' not in i):
                cmds.delete(i)
        
        t = cmds.checkBoxGrp("translateAxes", q = True, value2 = True)
        if  t:
            trans = []
        else:
            trans = ["y"]
        
        r = cmds.checkBoxGrp("rotateAxes", q = True, value2 = True)
        if r:
            rot = ["x","z"]
        else:
            rot = ["x", "y", "z"]

        parentConA = cmds.parentConstraint( locPos, 'Root', st=trans, sr=rot, mo = True)
        cmds.bakeResults( 'Root', simulation=True, t = (startNum, endNum), hierarchy= "below",  sb = 1, dic = True, pok = True, ral = False, rwl = False, cp = True)
        cmds.delete(parentConA)

        cmds.parent( 'Root_M', 'Root' )
        parentConB = cmds.parentConstraint( locPos, 'Root_M', mo = True)
        cmds.bakeResults( 'Root_M', simulation=True, t = (startNum, endNum), hierarchy= "below",  sb = 1, dic = True, pok = True, ral = False, rwl = False, cp = True)
        cmds.delete(parentConB)
        cmds.delete(locPos)



ZHY_RootMotionForUE4()