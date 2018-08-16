#在原骨骼和精简的骨骼之间做父子约束和缩放约束
import maya.cmds as cmds
basejnt = cmds.ls(sl = True)
jntAll = cmds.listRelatives(basejnt, allDescendents = True, type = "joint")
grp = cmds.group( em=True, name="CW_Constraints_GRP")
cmds.parent(grp, "Deformers_GRP")
for i in jntAll:
    j = i[3:]
    parentCon = cmds.parentConstraint(j, i)
    cmds.parent(parentCon, grp)
    scaleCon = cmds.scaleConstraint(j, i)
    cmds.parent(scaleCon, grp)