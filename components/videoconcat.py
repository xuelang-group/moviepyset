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
    app.modules.front.init("statics/videoconcat")


def videoConcat(args):
    cliplist=[]
    outfile=args['saveFile']
    for i ,x in enumerate(args['inFile']):
        globals()['clip'+str(i)]=VideoFileClip(x)
        cliplist.append(globals()['clip'+str(i)])
 
    final= concatenate_videoclips(cliplist)
    my_logger = MyBarLogger()
    final.write_videofile(outfile, logger=my_logger)

    app.send({"out1": outfile})

if __name__ == "__main__":
    suanpan.run(app)
