#镜像set driven key
#
#可以选择driver是否镜像，若不镜像则为原物体
#可以选择镜像的轴向的正负

import maya.cmds as cmds

class MirrorSDK(object):
    """docstring for MirrorSDK"""

    WINDOW_NAME = "MirrorSDKUI"
    
    def mirrorUI(self):
        if cmds.window(self.WINDOW_NAME, exists = True):
            cmds.deleteUI(self.WINDOW_NAME, window = True)

        main_window = cmds.window(self.WINDOW_NAME, title =  "MirrorSDKUI", w = 320, h = 200, sizeable = 1)
        
        cmds.columnLayout(w = 250, columnOffset = ("left", 10))
        cmds.columnLayout(h =3)
        cmds.setParent( '..' ) 

        cmds.columnLayout(w = 270, columnOffset = ("left", 2))
        cmds.setParent( '..' )

        cmds.rowLayout( numberOfColumns = 2, columnAttach=(1, 'right', 2), columnWidth = (30, 120) )

        selcurveButton = cmds.button("currentDriven", label = "select current driven", h = 25, command = self.SelCurrentDNF)
        currentDNF = cmds.textField("currentDrivenName", text = "", en = 1, w = 160 )

        cmds.setParent( '..' )

        cmds.rowLayout( numberOfColumns = 2, columnAttach=(1, 'right', 2), columnWidth = (30, 120),)

        seljntButton = cmds.button("mirrorDriven", label = "select mirror driven", h = 25, command=self.SelMirrorDNF)
        mirrorDNF = cmds.textField("mirrorDrivenName", text = "", en = 1, w = 160 )

        cmds.setParent( '..' )
        cmds.rowLayout( numberOfColumns = 1, columnAttach=(1, 'both', 0), columnWidth3=(80, 75, 150) )

        cmds.radioButtonGrp("driverMirror", label = 'DriverMirror:', labelArray2=['Yes', 'No'], columnWidth3 = (120, 50, 30), numberOfRadioButtons = 2, select = 1)
        cmds.setParent( '..' )

        cmds.setParent( '..' )
        cmds.rowLayout( numberOfColumns = 1, columnAttach=(1, 'both', 0), columnWidth3=(80, 75, 150) )

        cmds.radioButtonGrp("mirrorDiretion", label = 'MirrorDiretion:', labelArray2=['forward', 'opposite'], numberOfRadioButtons = 2, columnWidth3 = (120, 50, 30), select = 1)
        cmds.setParent( '..' )

        cmds.columnLayout( w = 270, columnOffset = ("left", 20))

        creatcon_button = cmds.button(label = "Mirror con", align = "Mirror", w = 250, h = 30, command = "")
        cmds.setParent( '..' )
        
        cmds.showWindow(main_window)

    def selectObj(self, objName):

        obj = cmds.ls(sl = True)
        if len(obj) != 1:
            return
        cmds.textField(objName, e = True, text = obj[0])

    def SelCurrentDNF(self):
        self.selectObj("currentDrivenName")

    def SelMirrorDNF(self):
        self.selectObj("mirrorDrivenName")

    def DoMirror(self):
        mirrDir = cmds.radioButtonGrp("mirrorDiretion", q = True, select = True) #镜像的轴向
        QDriver = cmds.radioButtonGrp("driverMirror", q = True, select = True) #Driver是否需要镜像
        currentObj = cmds.textField("currentDrivenName", q = True, text = True) #当前选择的物体
        mirrObj = cmds.textField("mirrorDrivenName", q = True, text = True) #需要被镜像的物体
        atts = "translateX translateY translateZ rotateX rotateY rotateZ scaleX scaleY scaleZ visibility"
        attsList = atts.split(" ")

        

MirrorSDK().mirrorUI()