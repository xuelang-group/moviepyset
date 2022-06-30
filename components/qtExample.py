import os
import sys
from PySide6 import QtCore, QtWidgets, QtGui
from components.stream import Stream, app
from suanpan.log import logger

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        # 初始化数据
        self.config = {
            "src": None,
            "tgt": None,
            "startTime": None,
            "endTime": None,
            "videoHeight": None,
            "videoWidth": None,
            "volume": None
        }

        # 初始化流计算线程
        self.thread = QtCore.QThread()
        self.app = Stream(self.callLoop, initFunc=self.initStream)
        self.app.moveToThread(self.thread)
        self.thread.started.connect(self.app.run)
        self.thread.start()
        
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

        # 尺寸配置
        self.videoHeight = QtWidgets.QLineEdit()
        self.videoWidth = QtWidgets.QLineEdit()
        self.videoHeight.setValidator(QtGui.QIntValidator())
        self.videoWidth.setValidator(QtGui.QIntValidator())
        self.videoHeight.textChanged.connect(self.setConfig("videoHeight"))
        self.videoWidth.textChanged.connect(self.setConfig("videoWidth"))
        self.sizeConfig = QtWidgets.QFormLayout()
        self.sizeConfig.addRow("尺寸调节", QtWidgets.QWidget())
        self.sizeConfig.addRow("宽：", self.videoWidth)
        self.sizeConfig.addRow("高：", self.videoHeight)

        # 声音配置
        self.volume = QtWidgets.QLineEdit()
        self.volume.setValidator(QtGui.QIntValidator())
        self.volume.textChanged.connect(self.setConfig("volume"))
        self.volumeConfig = QtWidgets.QFormLayout()
        self.volumeConfig.addRow("声音调节", QtWidgets.QWidget())
        self.volumeConfig.addRow("倍数：", self.volume)

        # 状态配置
        self.progress = QtWidgets.QProgressDialog('执行进度', '隐藏', 0, 10)

        # 执行按钮
        self.runButton = QtWidgets.QPushButton("运行")
        self.runButton.clicked.connect(self.completeConfig)

        # 配置页面
        self.layout = QtWidgets.QFormLayout()
        self.layout.addRow("源文件路径", self.selectSrcFile)
        self.layout.addRow("输出文件夹路径", self.selectTgtFolder)
        self.layout.addRow(self.cutConfig)
        self.layout.addRow(self.sizeConfig)
        self.layout.addRow(self.volumeConfig)
        self.layout.addRow(self.progress)
        self.layout.addRow(self.runButton)
        
        w = QtWidgets.QWidget()
        w.setLayout(self.layout)
        self.setCentralWidget(w)

    def callLoop(self, context):
        args = context.args
        # TODO: 收到输入数据并输出
        logger.info(f"收到数据：{args}")
        return "test"

    def initStream(self, context):
        args = context.args
        logger.info(f"初始化数据：{args}")
        # TODO: 下载配置文件并初始化配置

    # 文本变更
    def setConfig(self, name):
        return QtCore.Slot()(lambda: self.config.update({name: getattr(self, name).text()}))

    def getConfig(self, data):
        self.config = data["data"]
        print(self.config)
        if self.config["src"]:
            self.src.setText(self.config["src"])
        if self.config["tgt"]:
            self.tgt.setText(self.config["tgt"])
        if self.config["startTime"]:
            self.startTime.setText(self.config["startTime"])
        if self.config["endTime"]:
            self.endTime.setText(self.config["endTime"])
        if self.config["videoHeight"] is not None:
            self.videoHeight.setText(str(self.config["videoHeight"]))
        if self.config["videoWidth"] is not None:
            self.videoWidth.setText(str(self.config["videoWidth"]))
        if self.config["volume"] is not None:
            self.volume.setText(str(self.config["volume"]))

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
        dialog.setNameFilter('(*.jpg *.png)')
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

    @QtCore.Slot()
    def completeConfig(self, data):
        app.sendWithoutContext(str(self.config))


def main(*args, **kwargs):

    qApp = QtWidgets.QApplication([])

    mainWindow = MainWindow()
    mainWindow.resize(800, 600)
    mainWindow.setWindowTitle("视频编辑")
    mainWindow.show()

    r = qApp.exec()
    mainWindow.app.stop()
    sys.exit(r)