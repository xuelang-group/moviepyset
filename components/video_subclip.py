
from cmath import log
from logging import LogRecord
from suanpan.log import logger
import time
from PySide6 import QtCore
from PySide6.QtCore import Signal
from components.util import MyBarLogger
from moviepy.editor import *
from components.stream import Stream, app
from moviepy.audio.fx.volumex import volumex
import json
from datetime import datetime
class Video(QtCore.QObject):
    progress = Signal(int)
    terminal_signal = Signal(int)
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.count = 0
        self._stop_signal = False
        self._triggerd = False
        self.process_array = []
    
    def run(self):
        # logger.info(self.config)
        while True:
            if self._triggerd:
                self._triggerd = False
                try:
                    complete = True
                    # logger.info(self._stop_signal)
                    logger.info("start !!!")
                    logger.info(self.config)

                    infile = self.config['src']
                    #获取输入文件的后缀
                    file = os.path.splitext(infile)
                    _, type = file
                    filename = datetime.now().strftime('%Y%m%d_%H%M%S')
                    outfile = self.config['tgt'] +"/" + filename +"_output" + type
                    logger.info(outfile)
                    subclip_start = self.config['startTime']
                    subclip_end = self.config['endTime']
                    # video_height = self.config['videoHeight']
                    # video_width = self.config['videoWidth']
                    # volume =  self.config['volume']
                    self.final_clip = VideoFileClip(infile)
                    self.process_array.append(self.final_clip)
                    self.final_clip = self.final_clip.subclip(subclip_start,subclip_end)
                    self.process_array.append(self.final_clip)
                    # logger.info("!!!!")
                    my_logger = MyBarLogger(self.progress)
                    self.final_clip.write_videofile(outfile, logger=my_logger)
                    if complete:
                        app.sendWithoutContext(outfile)
                        return outfile
                except:
                    pass
                finally:
                    self.terminal_signal.emit(1)
            # else:
            #     pass

    def stop(self):
        self._stop_signal = True
        for ele in self.process_array:
            ele.close()
        self.terminal_signal.emit(1)
        # pass

    def trigger(self, config):
        self.config = config
        self._triggerd = True
        self._stop_signal = False
