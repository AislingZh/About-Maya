#镜像左右手脚的轴向
#用法：镜像手部，L -> R 选择 L_WristIKFKEnd_jnt 然后运行脚本
#      镜像脚，L -> R 选择 L_ToesIKFK_jnt 然后运行脚本
import maya.cmds as cmds
basejnt = cmds.ls(sl = True)
jntAll = cmds.listRelatives(basejnt, allDescendents = True, type = "joint")
for i in jntAll:
    if("OffsetGRP" in i):
        joValue = cmds.getAttr(i +".jointOrient")[0]
        j = i.replace("L_", "R_")
        cmds.setAttr(j +".jointOrient" , joValue[0], joValue[1], joValue[2])