
from cmath import log
from logging import LogRecord
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
        self._stop_signal = False
        self._triggerd = False
        self.process_array = []
    
    def run(self):
        # infile = self.config['src']
        # self.config['tgt'] = "" if self.config['tgt'] is None else self.config['tgt']
        # outfile = self.config['tgt'] +"/" +"output.mp4"
        # subclip_start = self.config['startTime']
        # subclip_end = self.config['endTime']
        # video_height = self.config['videoHeight']
        # video_width = self.config['videoWidth']
        # volume = self.config['volume']
        # self.final_clip = VideoFileClip(infile).subclip(subclip_start,subclip_end)
        # # final_clip.volumex(volume)
        # # final_clip.resize()
        # my_logger = MyBarLogger(self.progress)
        # self.final_clip.write_videofile(outfile, logger=my_logger) '{"first_name": "Michael"
        # tmpSring = '{"src": "D:/xuelangyun/my_project/moviepyset-ly_0609/liugenghong1.mp4", "tgt": "D:/xuelangyun/moviepyset/ouput", "startTime": "0, 'endTime': '10', 'videoHeight': None, 'videoWidth': None, 'volume': None}"
        logger.info("!!!!")
        logger.info(self.config)
        while True:
            if self._triggerd:
                self._triggerd = False
                try:
                    # if not self._stop_signal:
                    #     pass
                    # else:
                    #     complete = False
                    #     # logger.info("close !!")
                    #     # self.progress.emit(0)
                    #     # time.sleep()
                    #     # self.final_clip.close()
                    complete = True
                    # logger.info(self._stop_signal)
                    logger.info("start !!!")
                    logger.info(self.config)
                    # infile = "D:/xuelangyun/my_project/moviepyset-ly_0609/liugenghong1.mp4"
                    # self.config['tgt'] = "D:/xuelangyun/moviepyset/ouput"
                    # outfile = self.config['tgt'] +"/" +"output.mp4"
                    # subclip_start = 0
                    # subclip_end = 10
                    # video_height = 0
                    # video_width = 0
                    # volume = self.config['volume']

                    infile = self.config['src']
                    outfile = self.config['tgt'] +"/" +"output.mp4"
                    subclip_start = self.config['startTime']
                    subclip_end = self.config['endTime']
                    video_height = self.config['videoHeight']
                    video_width = self.config['videoWidth']
                    volume = self.config['volume']

                    # logger.info(type(volume))
                    self.final_clip = VideoFileClip(infile)
                    self.process_array.append(self.final_clip)
                    self.final_clip = self.final_clip.subclip(subclip_start,subclip_end)
                    self.process_array.append(self.final_clip)

                    # self.final_clip = self.final_clip.volumex(volume)
                    # self.process_array.append(self.final_clip)
                    # final_clip.resize()
                    my_logger = MyBarLogger(self.progress)
                    self.final_clip.write_videofile(outfile, logger=my_logger)
                    
                    # for _ in range(100):
                    #     if not self._stop_signal:
                    #         time.sleep(1)
                    #         self.progress.emit(self.count)
                    #         self.count += 1
                    #     else:
                    #         self._stop_signal = False
                    #         complete = False
                    #         self.count = 0
                    #         self.progress.emit(self.count)
                    #         break
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
