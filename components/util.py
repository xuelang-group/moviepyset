import imp
from proglog import ProgressBarLogger
from suanpan.log import logger
import ctypes  
import inspect
import os
class MyBarLogger(ProgressBarLogger):
    def __init__(self, progress):
        self.progress = progress
        super(MyBarLogger, self).__init__()

    def callback(self, **changes):
        bars = self.state.get('bars')
        index = len(bars.values()) - 1
        if index > -1:
            bar = list(bars.values())[index]
            value = int(bar['index'] / bar['total'] * 100)
            self.progress.emit(value)
            logger.info(value)  
