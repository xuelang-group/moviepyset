# coding=utf-8

import abc
import os
import tempfile

import suanpan
from suanpan import asyncio, error, g
from suanpan import path as spath
from suanpan import runtime
from suanpan.app import app
from suanpan.app.arguments import Json, String, Int
from suanpan.log import logger
from suanpan.node import node
from suanpan.storage import storage


from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.video.io.VideoFileClip import VideoFileClip

from modules.utils import MyBarLogger

@app.afterInit
def initFront(_):
    app.modules.front.init("statics/subtitleComposite")


def subtitleComposite(args):
    # args = context.args
    videoinfile=args['vinFile']
    subinfile=args['subinFile']
    outfile=args['saveFile']

    # subcolor=args['subcolor']
    font=args['font']
    fontsize=args['fontsize']
    
    # generator = lambda txt: TextClip(txt,font='SimHei',fontsize=60, color='white',stroke_color='black')
    generator = lambda txt: TextClip(txt,font=font,fontsize=fontsize, color='white',stroke_color='black')
    vclip = VideoFileClip(videoinfile)
    sub = SubtitlesClip(subinfile, generator).set_position(('center','bottom'), relative=True)
    final = CompositeVideoClip([vclip, sub])
    my_logger = MyBarLogger()
    final.write_videofile(outfile, fps=vclip.fps,logger=my_logger)

    app.send({"out1": outfile})

if __name__ == "__main__":
    suanpan.run(app)
