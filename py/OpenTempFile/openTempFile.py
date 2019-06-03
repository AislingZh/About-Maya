# -*- coding:UTF-8 -*-
from PySide2 import QtWidgets, QtCore, QtGui
import json
import os
from maya import cmds
import pprint

DIRECTORY = os.environ.get('temp')
class openTempFile(dict):
    '''
    find,refresh,openFile, openDir
    '''
    def find(self, directory = DIRECTORY):

        if not os.path.exists((directory)):
            return
        self.clear()

        files = os.listdir(directory)
        mayaFiles = [f for f in files if f.endswith('.ma')]
        for ma in mayaFiles:
            name, ext = os.path.splitext(ma)
            path = os.path.join(directory, ma)
            self[name] = path

    def openFile(self,name):
        path = self[name]
        cmds.file(path, open = True, f = True)

    def openDir(self,path = DIRECTORY):
        os.startfile(path)

class openTempFileUI(QtWidgets.QDialog):

    def __init__(self):
        super(openTempFileUI, self).__init__()

        self.setWindowTitle("openTempFileWindow")

        self.library = openTempFile()

        self.buildUI()
        self.populate()


    def buildUI(self):
        # 创建master垂直的布局容器M
        layout = QtWidgets.QVBoxLayout(self)
        # #创建一个widget容器a
        # saveWidget = QtWidgets.QWidget()
        # #设置容器为水平布局
        # saveLayout = QtWidgets.QHBoxLayout(saveWidget)
        # #将a容器添加到主布局中
        # layout.addWidget(saveWidget)
        # #创建一个输入框
        # self.saveNameField = QtWidgets.QLineEdit()
        # #将输入框添加到水平布局中
        # saveLayout.addWidget(self.saveNameField)
        # #创建一个按钮
        # saveBtn = QtWidgets.QPushButton('save')
        # #saveBtn.clicked.connect(self.save)
        # saveLayout.addWidget(saveBtn)

        self.label = QtWidgets.QLabel('敬告：打开临时文件将会关闭当前文件，该步骤将不能返回！')
        layout.addWidget((self.label))


        self.listWidget = QtWidgets.QListWidget()
        layout.addWidget(self.listWidget)

        btnWidget = QtWidgets.QWidget()
        btnLayout = QtWidgets.QHBoxLayout(btnWidget)
        layout.addWidget(btnWidget)

        openBtn = QtWidgets.QPushButton('openFile')
        openBtn.clicked.connect(self.load)
        btnLayout.addWidget(openBtn)

        refreshBtn = QtWidgets.QPushButton('refresh')
        refreshBtn.clicked.connect(self.populate)
        btnLayout.addWidget(refreshBtn)

        openDirBtn = QtWidgets.QPushButton('openDirectory')
        openDirBtn.clicked.connect(self.loadDir)
        btnLayout.addWidget(openDirBtn)

    def populate(self):
        self.listWidget.clear()
        self.library.find()
        for name, info in self.library.items():
            item = QtWidgets.QListWidgetItem(name)
            self.listWidget.addItem(item)

    def load(self):
        currentItem = self.listWidget.currentItem()

        if not currentItem:
            return
        name = currentItem.text()
        self.library.openFile(name)

    def loadDir(self):
        self.library.openDir()

def showUI():
    ui = openTempFileUI()
    ui.show()
    return ui








