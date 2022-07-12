from concurrent.futures import process
import imp
import json
from multiprocessing import set_forkserver_preload
import os
import sys
from typing import final
from unittest import result
from PySide6 import QtCore, QtWidgets, QtGui
from pandas import value_counts
from requests import patch
from components.stream import Stream, app
from suanpan.log import logger
from suanpan.storage import storage
from moviepy.editor import *
from proglog import ProgressBarLogger
from components.video_subclip import Video
from components.util import MyBarLogger
from PySide6.QtCore import Signal
from suanpan import g
from suanpan.utils.tools import safeMkdirsForFile

# key = os.path.join(storage.configKey, "param.json")
# path = os.path.join(g.tempStore, key)
# if not os.path.exists(path):
#     open(path, 'w')

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
        # 初始化数据
        self.config = {
            "src": None,
            "tgt": None,
            "startTime": None,
            "endTime": None
        }
        self.key = os.path.join(storage.configKey, "param.json")
        self.path = os.path.join(g.tempStore, self.key)
        logger.info(self.path)

        #LOCAL_LATEST = os.path.join(".", "configs", "latest",args['uuid'],"configurations.json")
        #safeMkdirsForFile(LOCAL_LATEST)
        try: 
            if not os.path.exists(self.path):
                safeMkdirsForFile(self.path)
                #open(self.path, 'w')
        except:
            logger.info("create param.json failed !!!")

        # 初始化流计算线程
        self.thread = QtCore.QThread()
        self.app = Stream(self.callLoop, initFunc=self.initStream)
        self.app.moveToThread(self.thread)
        self.thread.started.connect(self.app.run)
        self.thread.start()

        self.thread_video = QtCore.QThread()
        self.video = Video(self.config)
        self.video.moveToThread(self.thread_video)
        self.video.progress.connect(self.updateProgress)
        self.thread_video.started.connect(self.video.run)
        self.video.terminal_signal.connect(self.complete)
        self.thread_video.start()


        # 源文件获取插件
        self.src = QtWidgets.QLineEdit()
        self.fileSelector = QtWidgets.QPushButton("选择文件")
        self.fileSelector.clicked.connect(self.selectFile)
        self.selectSrcFile = QtWidgets.QHBoxLayout()
        self.selectSrcFile.addWidget(self.src)
        self.selectSrcFile.addWidget(self.fileSelector)

        # 输出文件夹获取插件
        self.tgt = QtWidgets.QLineEdit()
        self.folderSelector = QtWidgets.QPushButton("选择文件夹")
        self.folderSelector.clicked.connect(self.selectFolder)
        self.selectTgtFolder = QtWidgets.QHBoxLayout()
        self.selectTgtFolder.addWidget(self.tgt)
        self.selectTgtFolder.addWidget(self.folderSelector)

        # 剪辑配置
        self.startTime = QtWidgets.QLineEdit()
        self.endTime = QtWidgets.QLineEdit()
        self.startTime.textChanged.connect(self.setConfig("startTime"))
        self.endTime.textChanged.connect(self.setConfig("endTime"))
        self.cutConfig = QtWidgets.QFormLayout()
        self.cutConfig.addRow("剪辑配置", QtWidgets.QWidget())
        self.cutConfig.addRow("开始时间：", self.startTime)
        self.cutConfig.addRow("结束时间：", self.endTime)


        # 状态配置
        self.progress = QtWidgets.QProgressDialog('执行进度','隐藏', 0 , 100)

        # 执行按钮
        self.runButton = QtWidgets.QPushButton("运行")
        self.runButton.clicked.connect(self.completeConfig) #目前是输出所有config

        # 保存配置按钮
        self.saveButton = QtWidgets.QPushButton("保存配置")
        self.saveButton.clicked.connect(self.saveConfig) #目前是输出所有config
        

        # 配置页面
        self.layout = QtWidgets.QFormLayout()
        self.layout.addRow("源文件路径", self.selectSrcFile)
        self.layout.addRow("输出文件夹路径", self.selectTgtFolder)
        self.layout.addRow(self.cutConfig)
        # self.layout.addRow(self.sizeConfig)
        # self.layout.addRow(self.volumeConfig)
        self.layout.addRow(self.progress)
        self.layout.addRow(self.runButton)
        self.layout.addRow(self.saveButton)

        w = QtWidgets.QWidget()
        w.setLayout(self.layout)
        self.setCentralWidget(w)

    def callLoop(self, context):
        args = context.args  #解析输入的数据
        # TODO: 收到输入数据并输出
        logger.info(f"收到数据：{args}")
        self.config["src"] = args['inputData1']
        # result = self.video_clip()
        # return str(self.config["src"])
        # logger.info("hello")

    def initStream(self, context):
        args = context.args
        logger.info(f"初始化数据：{args}")
        try:
            with open(self.path) as f:
                config = json.load(f)
                self.getConfig(config)
        except:
            pass

    # 文本变更
    def setConfig(self, name):
        return QtCore.Slot()(lambda: self.config.update({name: getattr(self, name).text()}))
        
    def getConfig(self, data):
        self.config = data
        if self.config["src"]:
            self.src.setText(self.config["src"])
        if self.config["tgt"]:
            self.tgt.setText(self.config["tgt"])
        if self.config["startTime"]:
            self.startTime.setText(self.config["startTime"])
        if self.config["endTime"]:
            self.endTime.setText(self.config["endTime"])
        # if self.config["videoHeight"] is not None:
        #     self.videoHeight.setText(str(self.config["videoHeight"]))
        # if self.config["videoWidth"] is not None:
        #     self.videoWidth.setText(str(self.config["videoWidth"]))
        # if self.config["volume"] is not None:
        #     self.volume.setText(str(self.config["volume"]))

    def getStatus(self, data):
        self.appStatus = data["data"]
        if self.appStatus:
            self.runButton.setText("停止")
        else:
            self.progress.setValue(0)
            self.runButton.setText("运行")

    # 弹窗选择文件夹
    @QtCore.Slot()
    def selectFolder(self):
        if self.config["tgt"] is not None and os.path.isdir(self.config["tgt"]):
            tgtVideoDir = self.config["tgt"]
        else:
            tgtVideoDir = QtCore.QDir.currentPath()
        dialog = QtWidgets.QFileDialog(self)
        dialog.setWindowTitle('Select Output Folder')
        dialog.setDirectory(tgtVideoDir)
        dialog.setFileMode(QtWidgets.QFileDialog.Directory)
        dialog.setOption(QtWidgets.QFileDialog.ShowDirsOnly, True)
        dialog.setViewMode(QtWidgets.QFileDialog.Detail)
        dirname = None
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            dirname = dialog.selectedFiles()
        if dirname:
            self.config["tgt"] = str(dirname[0])
            self.tgt.setText(self.config["tgt"])

    # 弹窗选择文件
    @QtCore.Slot()
    def selectFile(self):
        if self.config["src"] is not None and os.path.isfile(self.config["src"]):
            srcVideoDir = os.path.dirname(self.config["src"])
        else:
            srcVideoDir = QtCore.QDir.currentPath()
        dialog = QtWidgets.QFileDialog(self)
        dialog.setWindowTitle('Open Video file')
        dialog.setNameFilter('(*.mp4 *.flv *.wmv *.rm *.avi *.webm *.rmvb)')
        dialog.setDirectory(srcVideoDir)
        dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)

        filename = None
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            filename = dialog.selectedFiles()
        if filename:
            self.config["src"] = str(filename[0])
            self.src.setText(self.config["src"])

    @QtCore.Slot()
    def setProgress(self, data):
        self.progress.setValue(data)

    # @QtCore.Slot()
    # def completeConfig(self, data): 
    #     logger.info(self.config) 
    #     # 创建执行视频编辑的线程
    #     if self.runButton.text()=="运行":
    #         # self.thread_video = QtCore.QThread()
    #         self.video = Video(self.config)
    #         self.video.moveToThread(self.thread_video)
    #         self.video.progress.connect(self.updateProgress)
    #         self.video.terminal_signal.connect(self.complete)
    #         # self.thread_video.started.connect(self.video.run)
    #         # self.thread_video.finished.connect(self.complete)
    #         self.thread_video.start()
    #         self.video.run()
    #         self.runButton.setText("停止")
    #     else:
    #         self.video.stop()
    #         self.updateProgress(0)
    #         self.runButton.setText("运行")

    def complete(self):
        self.runButton.setText("运行")
        self.updateProgress(0)

    @QtCore.Slot()
    def completeConfig(self, data): 
        logger.info(self.config) 
        # 创建执行视频编辑的线程
        if self.runButton.text()=="运行":
            self.video.trigger(self.config)
            self.runButton.setText("停止")
        else:
            self.video.stop()
            self.progress.setValue(0)
            self.runButton.setText("运行")
    
    def updateProgress(self, value):
        self.progress.setValue(value)

    @QtCore.Slot()
    def saveConfig(self, data):
        with open(self.path, "w") as f:
            json.dump(self.config, f)
        storage.upload(self.key.replace("\\", "/"), self.path)
        

def main(*args, **kwargs):
    qApp = QtWidgets.QApplication([])
    mainWindow = MainWindow()
    mainWindow.resize(800, 600)
    mainWindow.setWindowTitle("视频编辑")
    mainWindow.show()
    r = qApp.exec()
    mainWindow.app.stop()
    sys.exit(r)