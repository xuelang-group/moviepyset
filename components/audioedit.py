# coding=utf-8

import abc
import os
import tempfile

import suanpan
from suanpan import asyncio, error, g
from suanpan import path as spath
from suanpan import runtime
from suanpan.app import app
from suanpan.app.arguments import Json, String, Int,ListOfString
from suanpan.log import logger
from suanpan.node import node
from suanpan.storage import storage

from moviepy.editor import *
# from modules.utils import MyBarLogger
from proglog import ProgressBarLogger


# class MyBarLogger(ProgressBarLogger):
#     # @module.on("general.checkStatus")
#     def callback(self, **changes):
#         bars = self.state.get('bars')
#         index = len(bars.values()) - 1
#         if index > -1:
#             bar = list(bars.values())[index]
#             progress = int(bar['index'] / bar['total'] * 100)
#             #print(bar)
#             print(progress)
#             #增加算盘独有的像前端传入数据的接口
#             # app.sio.emit("general.checkStatus",progress)
from modules.utils import MyBarLogger


@app.afterInit
def initFront(_):
    app.modules.front.init("statics/editor")


@app.input(String(key="inputData1", alias="inputData1"))
@app.param(String(key="param0", alias="inFile"))
@app.param(String(key="param1", alias="saveFile"))
@app.param(Int(key="param2", alias="subclip_start"))
@app.param(Int(key="param3", alias="subclip_end"))

@app.output(Json(key="outputData1", alias="out1"))
def audioEdit(context):
    # context={"args":{"uuid": "2b2133b6dc4d46bf815259bd61fad38d","type": "audioEditor",
    #                  "inFile": ["../xiaoxiao.mp3"],
    #                  "saveFile":"../out1.mp3","subclipStart": 0,"subclipEnd": 20}}
    args = context["args"]
    infile = args['inFile']
    outfile = args['saveFile']
    subclip_start = args['subclip_start']
    subclip_end = args['subclip_end']
    # logger.info(infile)
    # logger.info(outfile)
    # clip = VideoFileClip(infile).subclip(subclip_start,subclip_end)
    clip = AudioFileClip(infile).subclip(subclip_start, subclip_end)
    my_logger = MyBarLogger()
    clip.write_audiofile(outfile, logger=my_logger)
    app.send({"out1": outfile})


if __name__ == "__main__":
    suanpan.run(app)
    # audioEdit()
