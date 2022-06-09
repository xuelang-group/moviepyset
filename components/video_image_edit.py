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


@app.afterInit
def initFront(_):
    app.modules.front.init("statics/editor")

#图片放在视频的哪个位置，持续多久，在哪里放，位置什么的
@app.input(String(key="inputData1", alias="inputData1"))
@app.param(String(key="param0", alias="inFile"))
@app.param(String(key="param1", alias="saveFile"))
@app.param(String(key="param2", alias="imagePath"))
# @app.param(String(key="param5", alias="pos_y"))
# @app.param(Bool(key="param6", alias="relative"))
# @app.param(Int(key="param7", alias="set_start"))
# @app.param(Int(key="param8", alias="set_duration"))

@app.output(String(key="outputData1", alias="out1"))

def videoImageEdit(context):
    args = context.args
    infile=args['inFile']
    outfile=args['saveFile']
    clip = VideoFileClip(infile)
    #选图片
    imagepath = args['imagePath']
    image_clip =ImageClip(imagepath).set_start(0).set_duration(5)
    image_clip.set_position(('center','center'))
    #合并
    final = CompositeVideoClip([clip,image_clip])

    final.write_videofile(outfile)
    app.send({"out1": outfile})

    final.close()

if __name__ == "__main__":
    suanpan.run(app)
    # args = {"uuid": "2b2133b6dc4d46bf815259bd61fad38d", "type": "videoEditor",
    #         "inFile": ["../sample2.mp4"],
    #         "saveFile": "../out2_image_ly.mp4", "subclipStart": 10, "subclipEnd": 20}
    # videoImageEdit(args)
