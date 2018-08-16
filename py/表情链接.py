import maya.cmds as cmds
import maya.mel as mel

def ConnetAttr(fir,sec):
    cmds.connectAttr(fir + ".translate", sec + ".translate")
    cmds.connectAttr(fir + ".rotate", sec + ".rotate")
    cmds.connectAttr(fir + ".scale", sec + ".scale")

def setConstraint(one , two, three = None):
    if three is None:
        cons = cmds.parentConstraint( one, two, mo=True, w=1.0 )
    else:
        cons = cmds.parentConstraint( one, two, three, mo=True, w=1.0 )
        cmds.setAttr(cons[0] + ".interpType", 2)


selObj = cmds.ls(sl = True)
DObj = cmds.duplicate( rr=True )
cmds.move(0, 0, 50, relative = True, objectSpace=True, worldSpaceDistance=True)
cmds.setAttr("Face_DrvCtr_grp.visibility", 1)
cmds.parent(DObj, "Face_DrvCtr_grp")
cmds.select("Face_DrvCtr_grp")

mel.eval('searchReplaceNames '+"Facial"+' '+"DrvCtr"+' "hierarchy";')


ConnetAttr("Facial_Jaw_ctr", "DrvCtr_Jaw_ctr")

setConstraint("DrvCtr_Face_Translate_ctr", "DrvCtr_Jaw_ctr", "DrvCtr_L_Cheek08_offset")
setConstraint("DrvCtr_Face_Translate_ctr", "DrvCtr_Jaw_ctr", "DrvCtr_R_Cheek08_offset")
ConnetAttr("DrvCtr_L_Cheek08_offset", "Facial_L_Cheek08_offset")
ConnetAttr("DrvCtr_R_Cheek08_offset", "Facial_R_Cheek08_offset")

setConstraint("DrvCtr_Face_Translate_ctr", "DrvCtr_Jaw_ctr", "DrvCtr_MouthExtCornerDrvL_extra")
setConstraint("DrvCtr_Face_Translate_ctr", "DrvCtr_Jaw_ctr", "DrvCtr_MouthExtCornerDrvR_extra")
ConnetAttr("DrvCtr_MouthExtCornerDrvL_extra", "Facial_MouthExtCornerDrvL_extra")
ConnetAttr("DrvCtr_MouthExtCornerDrvR_extra", "Facial_MouthExtCornerDrvR_extra")


setConstraint("DrvCtr_Jaw_ctr", "DrvCtr_Dw_LipParent_offset")
ConnetAttr("DrvCtr_Dw_LipParent_offset", "Facial_Dw_LipParent_offset")