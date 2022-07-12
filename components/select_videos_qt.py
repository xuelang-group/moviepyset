from ntpath import join
import os
import sys
import json
from turtle import title
from PySide6 import QtCore, QtWidgets, QtGui
from PySide6.QtCore import Qt, QRect
from components.stream import Stream, app
from suanpan import g
from suanpan.log import logger
from suanpan.storage import storage
from suanpan.utils.tools import safeMkdirsForFile

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # 初始化数据
        self.config = {
            "src": None
        }

        # 初始化流计算线程
        self.thread = QtCore.QThread()
        self.app = Stream(self.callLoop, initFunc=self.initStream)
        self.app.moveToThread(self.thread)
        self.thread.started.connect(self.app.run)
        self.thread.start()

        self.w = QtWidgets.QWidget()
        self.setCentralWidget(self.w)

        self.resize(800, 600)
        # 源文件获取插件
        self.fileSelector = QtWidgets.QPushButton("选择文件", self.w)
        self.fileSelector.setGeometry(QRect(280, 400, 100, 30))
        self.fileSelector.clicked.connect(self.btn1Clicked)

        self.src = QtWidgets.QPlainTextEdit (self.w)
        # self.src.resize(300, 30) #(x坐标,y坐标，按钮宽度,按钮高度)
        # self.src.move(300, 100)
        self.src.setGeometry(QRect(200, 100, 400, 250))

        self.selectSrcFile = QtWidgets.QHBoxLayout()
        self.selectSrcFile.addWidget(self.src)
        self.selectSrcFile.addWidget(self.fileSelector)


        # 保存配置按钮
        self.saveButton = QtWidgets.QPushButton("保存配置", self.w)
        self.saveButton.setGeometry(QRect(430, 400, 100, 30))
        self.saveButton.clicked.connect(self.saveConfig) #目前是输出所有config

    def callLoop(self, context):
        args = context.args
        # TODO: 收到输入数据并输出
        logger.info(f"收到数据：{args}")
        # return "test"

    def initStream(self, context):
        args = context.args
        logger.info(f"初始化数据：{args}")


    @QtCore.Slot()
    def btn1Clicked(self, data):
        dialog = QtWidgets.QFileDialog(self)
        dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        filePaths, _ = dialog.getOpenFileNames(
            self.w,
            "选择你要上传的文件",
            filter='(*.mp4 *.flv *.wmv *.rm *.avi *.webm *.rmvb)'
        )
        fileName = '\n'.join(filePaths)
        #print(fileName)
        self.src.setPlainText(fileName)
    
    @QtCore.Slot()
    def saveConfig(self, data):
        self.config["src"] = self.src.toPlainText()
        logger.info(self.config["src"].rstrip())
        app.sendWithoutContext(self.config["src"])
        
def main(*args, **kwargs):
    qApp = QtWidgets.QApplication([])
    mainWindow = MainWindow()
    mainWindow.resize(800, 600)
    mainWindow.setWindowTitle("视频文件名上传")
    mainWindow.show()
    r = qApp.exec()
    mainWindow.app.stop()
    sys.exit(r)

# if __name__ == '__main__':
#     qApp = QtWidgets.QApplication([])
#     mainWindow = MainWindow()
#     # mainWindow.resize(800, 600)
#     mainWindow.setWindowTitle("视频文件名上传")
#     mainWindow.show()

#     r = qApp.exec()
#     #mainWindow.app.stop()
#     sys.exit(r)