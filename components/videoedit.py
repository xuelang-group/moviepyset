# coding=utf-8

import abc
import os
import tempfile

import suanpan
from proglog import ProgressBarLogger
from suanpan import asyncio, error, g
from suanpan import path as spath
from suanpan import runtime
from suanpan.app import app
from suanpan.app.arguments import Json, String, Int
from suanpan.log import logger
from suanpan.node import node
from suanpan.storage import storage


from moviepy.editor import *


@app.afterInit
def initFront(_):
    app.modules.front.init("statics/editor")
class MyBarLogger(ProgressBarLogger):

    def callback(self, **changes):
        bars = self.state.get('bars')
        index = len(bars.values()) - 1
        if index > -1:
            bar = list(bars.values())[index]
            progress = int(bar['index'] / bar['total'] * 100)
            #print(bar)
            print(progress)
            #增加算盘独有的像前端传入数据的接口
            app.sio.emit("test_pro",progress)


def videoEdit(args):
    #args = context.args
    infile=args['inFile'][0]
    outfile=args['saveFile']
    subclip_start=args['subclipStart']
    subclip_end=args['subclipEnd']

    # infile="../sample1.mp4"
    # outfile="../hebing.mp4"
    # subclip_start=0
    # subclip_end=10

    clip = VideoFileClip(infile).subclip(subclip_start,subclip_end)
    my_logger = MyBarLogger()
    clip.write_videofile(outfile, logger=my_logger)
    #clip.write_videofile(outfile)
    app.send({"out1": outfile})

if __name__ == "__main__":
    suanpan.run(app)
    # args = ""
    # videoEdit(args)
