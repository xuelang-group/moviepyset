
from cmath import log
from suanpan.log import logger
import time
from PySide6 import QtCore
from PySide6.QtCore import Signal
from components.util import MyBarLogger
from moviepy.editor import *
from components.stream import Stream, app
import json
class Video(QtCore.QObject):
    progress = Signal(int)
    terminal_signal = Signal(int)
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.count = 0
        self.process_array = []
    
    def run(self):
        try:
            logger.info(self.config)
            infile = "D:/xuelangyun/my_project/moviepyset-ly_0609/liugenghong1.mp4"
            self.config['tgt'] = "D:/xuelangyun/moviepyset/ouput"
            outfile = self.config['tgt'] +"/" +"output.mp4"
            subclip_start = 0
            subclip_end = 10
            video_height = 0
            video_width = 0
            volume = self.config['volume']
            self.final_clip = VideoFileClip(infile)
            self.process_array.append(self.final_clip)
            self.final_clip = self.final_clip.subclip(subclip_start,subclip_end)
            self.process_array.append(self.final_clip)
            # final_clip.volumex(volume)
            # final_clip.resize()
            my_logger = MyBarLogger(self.progress)
            self.final_clip.write_videofile(outfile, logger=my_logger)
            for ele in self.process_array:
                ele.close()
            
        finally:
            self.terminal_signal.emit(1)

    def stop(self):
        for ele in self.process_array:
            ele.close()
        self.terminal_signal.emit(1)
