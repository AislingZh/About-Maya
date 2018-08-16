#表情绑定，眼睛控制器镜像
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
