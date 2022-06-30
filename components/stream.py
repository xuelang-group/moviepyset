import logging
from PySide6 import QtCore

from suanpan.app import app

logging.basicConfig()

class Stream(QtCore.QObject):

    def __init__(self, callFunc, initFunc=None, inArgs=[], outArgs=[], paramArgs=[]):
        super().__init__()
        for inArg in inArgs:
            app.input(inArg)
        for outArg in outArgs:
            app.param(outArg)
        for paramArg in paramArgs:
            app.output(paramArg)
        app.afterInit(initFunc)
        app(callFunc)
    
    def run(self):
        app.start()

    def stop(self):
        app.close()
