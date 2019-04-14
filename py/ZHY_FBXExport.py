
# ------------------------------------------------------------------------------------------------------------//
# ------------------------------------------------------------------------------------------------------------//
# 	SCRIPT:	ZHY_FBXExport.py
# 	VERSION: 0.5
# 	AUTHOR:	Aislingzh
# 			Aislingzh@qq.com
# 	DATE:		01 07, 2019
	

# 	DESCRIPTION:	 
# 			一FBX文件导出

# ------------------------------------------------------------------------------------------------------------//	
# ------------------------------------------------------------------------------------------------------------//

# ------------------------------------------------------------------------------------------------------------//
#FBX文件导出
# 分导出版本，unity版和ue4版

#1.导出不带动画的绑定文件，用于在引擎里做为骨骼参考的文件
#2.导出动画文件，仅带有做blendshape的模型+全套骨骼 + 骨骼和BS动画数据
#ps:
# a.导出前检查场景文件的尺寸和动画帧率；
# b.导出前清理场景文件 
# ------------------------------------------------------------------------------------------------------------//

import maya.mel as mel
import maya.cmds as cmds

class ZHY_FBXExport(object):

    WINDOW_NAME = "Export"


    def __init__(self):


        if cmds.window(self.WINDOW_NAME, exists = True):
            cmds.deleteUI(self.WINDOW_NAME, window = True)
        
        main_window = cmds.window(self.WINDOW_NAME, title =  "ZHY_FBXExport", rtf = True,  menuBar=True)

        cmds.menu( label='Help', helpMenu=True )
        cmds.menuItem( 'Application..."', label='"About' )

        cmds.columnLayout(adj=1)


        cmds.radioButtonGrp("Export_type", label = 'Export type:', labelArray2=['To Unity', 'To UE4'], numberOfRadioButtons = 2, columnWidth4 = (10, 70, 70, 70), select = 1)
        cmds.separator( height=5,style='in' )


        cmds.setParent( '..' )

        # cmds.frameLayout("Export:", collapsable = True, labelVisible=1, marginWidth=5,marginHeight=5,borderStyle='etchedOut' )
        cmds.columnLayout(adj=1)
        cmds.separator( height=5,style='in' )
        
        Rig_button = cmds.button(label = "ExportRigFile(不带动画文件)",h=25,command = self.ExportRigFile) 

        
        cmds.separator( height=5,style='in' )
        cmds.separator( height=5,style='in' )

        cmds.intFieldGrp("StartFrame", numberOfFields=1, label='StartFrame', value1=0 )
        endNum = cmds.playbackOptions(q = True , aet = True)
        cmds.intFieldGrp("EndFrame", numberOfFields=1, label='EndFrame', value1=endNum )

        Anim_button = cmds.button(label = "ExportAnimFile(动画文件)",h=25,command = self.ExportAnimFile )
        cmds.separator( height=10,style='in' )    


        cmds.showWindow(main_window)
    
    def ExportRigFile(self, *args):
        # 导出不带动画的绑定文件

        slObjA = cmds.ls(sl = True)
        if len(slObjA) <= 0:
            cmds.confirmDialog(t=u'敬告！！！', m=u'请选择 SkinJnt_Grp 和 Geometry_Grp ', b=[u'好的'], db=u'好的')
            return

        mel.eval('FBXProperty Export|IncludeGrp|Animation -v false;')
        self.DoExport()

    def ExportAnimFile(self, *args):
        # 导出骨骼动画文件

        try:
            slObjB = cmds.ls(sl = True)
            if len(slObjB) <= 0:
                cmds.confirmDialog(t=u'敬告！！！', m=u'请选择 SkinJnt_Grp 和 Geometry_Grp中含有BS节点的模型 ', b=[u'好的'], db=u'好的')
                return
            startFrame = cmds.intFieldGrp("StartFrame", q = True, value1 = True)
            endFrame = cmds.intFieldGrp("EndFrame", q = True, value1 = True)

            #fbx导出设置，动画 ，ps: 烘焙动画前先设置场景的动画帧率；
            mel.eval('FBXProperty Export|IncludeGrp|Animation -v true;')
            mel.eval('FBXExportBakeComplexAnimation -v true;')

            startMel = "FBXExportBakeComplexStart  -v " + str(startFrame) 
            mel.eval(startMel)
            startMel = "FBXExportBakeComplexEnd  -v " + str(endFrame) 
            mel.eval(startMel)

            mel.eval('FBXExportBakeComplexStep -v 1;')
            self.DoExport()
        except Exception as e:
            raise e

    # def ExportAddFaceFile(self, *args):
    #     pass
    #     print ("导出骨骼动画文件")

    # def ExportBodyFile(self, *args):
    #     pass
    #     print ("导出带blendshape的动画文件")   

    def ClearFile(self, *args):
        # 清理文件

        mel.eval('hyperShadePanelMenuCommand("hyperShadePanel1", "deleteUnusedNodes");')
    
    def CheackWorkUnits(self, *args):
        # 检查工作尺寸

        try:
            Export_type = cmds.radioButtonGrp("Export_type", q = True, select = True)

            if Export_type == 1:
                #设置场景帧率和尺寸 ntsc: 30 fps ; pal: 25 fps ; centimeter ; meter 
                cmds.currentUnit( time='ntsc', linear='meter')
                # fbx导出设置，文件单位转化,FBXExportConvertUnitString [mm|dm|cm|m|km|In|ft|yd|mi];
                mel.eval('FBXExportConvertUnitString m;')
                # print("Unity 模式")
            elif Export_type == 2:
                #设置场景帧率和尺寸 ntsc: 30 fps ; pal: 25 fps ; centimeter ; meter 
                cmds.currentUnit( time='pal', linear='centimeter')
                mel.eval('FBXExportConvertUnitString cm;')
                # print("UE4 模式")
        except Exception as e:
            raise e

    def ExportSetting(self):
        try:
            #fbx导出设置，导出版本 
            mel.eval('FBXExportFileVersion -v FBX201400;')

            #fbx导出设置，导出文件的向上轴向 
            mel.eval('FBXExportUpAxis Y;')

            #fbx导出设置，导出是否包含子文件 
            # mel.eval('FBXProperty Export|IncludeGrp|InputConnectionsGrp|IncludeChildren -v true;')
            mel.eval('FBXExportInputConnections -v true;')
            

            #fbx导出设置，导出是否包连入的文件 
            mel.eval('FBXProperty Export|IncludeGrp|InputConnectionsGrp|InputConnections -v false;')

            #fbx导出设置，导出时Deformation的设置 
            mel.eval('FBXProperty Export|IncludeGrp|Animation|Deformation -v true;')
            mel.eval('FBXProperty Export|IncludeGrp|Animation|Deformation|Skins -v true;')
            mel.eval('FBXProperty Export|IncludeGrp|Animation|Deformation|Shape -v true;')

            #fbx导出设置，导出是否包含约束 
            mel.eval('FBXProperty Export|IncludeGrp|Animation|ConstraintsGrp|Constraint -v false;')

        except Exception as e:
            raise e

    
    def DoExport(self):
        # 执行导出
        try:
            self.CheackWorkUnits()
            self.ClearFile()
            self.ExportSetting()
            Dialog = cmds.fileDialog2(fileFilter = "FBX export (*.fbx)" , startingDirectory = "D:/")
            cmds.file(Dialog[0] , force=True, pr=True, type="FBX export", es = True)
        except Exception as e:
            raise e


ZHY_FBXExport()
