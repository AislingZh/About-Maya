import maya.cmds as cmds
cmds.commandPort(name=":7002", sourceType="python")
cmds.commandPort(name=":7001", sourceType="mel")