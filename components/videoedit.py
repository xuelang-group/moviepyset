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
from modules.utils import MyBarLogger

@app.afterInit
def initFront(_):
    app.modules.front.init("statics/editor")


def videoEdit(args):
    # args = context.args
    infile=args['inFile'][0]
    outfile=args['saveFile']
    subclip_start=args['subclipStart']
    subclip_end=args['subclipEnd']
    clip = VideoFileClip(infile).subclip(subclip_start,subclip_end)
    my_logger = MyBarLogger()
    clip.write_videofile(outfile, logger=my_logger)
    app.send({"out1": outfile})

if __name__ == "__main__":
    suanpan.run(app)
