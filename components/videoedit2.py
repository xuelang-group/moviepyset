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
from modules.videoedit2 import socketapi as videoedit_module

app.modules.register("socketapi", videoedit_module)

@app.afterInit
def initFront(_):
    app.modules.front.init("statics/editor")

@app.input(String(key="inputData1"))
@app.param(Json(key="param0", alias="inFile"))
@app.param(String(key="param1", alias="saveFile"))
@app.param(String(key="param2", alias="subclipStart"))
@app.param(String(key="param3", alias="subclipEnd"))
@app.output(Json(key="outputData1"))
def videoEdit(context):
    args = context.args
    infile=args['inFile'][0]
    outfile=args['saveFile']
    subclip_start=args['subclipStart']
    subclip_end=args['subclipEnd']
    clip = VideoFileClip(infile).subclip(subclip_start,subclip_end)
    my_logger = MyBarLogger()
    clip.write_videofile(outfile, logger=my_logger)
    g.num=g.num+1
    logger.info(f"第{g.num}次")
    app.send({"out1": outfile})
    
if __name__ == "__main__":
    suanpan.run(app)
