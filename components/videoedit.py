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
# from modules.utils import MyBarLogger

@app.afterInit
def initFront(_):
    app.modules.front.init("statics/editor")


@app.input(String(key="inputData1", alias="inputData1"))
@app.param(Json(key="param0", alias="inFile"))
@app.param(String(key="param1", alias="saveFile"))
@app.param(Int(key="param2", alias="subclip_start"))
@app.param(Int(key="param3", alias="subclip_end"))
@app.output(String(key="outputData1", alias="out1"))
def videoEdit(context):
    args = context.args
    infile=args['inFile'][0]
    outfile=args['saveFile']
    subclip_start=args['subclip_start']
    subclip_end=args['subclip_end']
    clip = VideoFileClip(infile).subclip(subclip_start,subclip_end)
    #my_logger = MyBarLogger()
    #clip.write_videofile(outfile, logger=my_logger)
    clip.write_videofile(outfile)
    app.send({"out1": outfile})
    clip.close()

if __name__ == "__main__":
    suanpan.run(app)
