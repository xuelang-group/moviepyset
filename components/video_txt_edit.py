# coding=utf-8

import abc
import os
import tempfile

import suanpan
from suanpan import asyncio, error, g
from suanpan import path as spath
from suanpan import runtime
from suanpan.app import app
from suanpan.app.arguments import Json, String, Int, Bool
from suanpan.log import logger
from suanpan.node import node
from suanpan.storage import storage


from moviepy.editor import *
#from modules.utils import MyBarLogger

from proglog import ProgressBarLogger

@app.afterInit
def initFront(_):
    app.modules.front.init("statics/editor")


#视频中加入文字---（todo 某一帧，加多长时间（eg 一张图片里面的人名显示），显示的文字的位置，颜色、大小、字体等设置）

@app.input(String(key="inputData1", alias="inputData1"))
@app.param(Json(key="param0", alias="inFile"))
@app.param(String(key="param1", alias="txt"))
@app.param(Int(key="param2", alias="fontsize"))
@app.param(String(key="param3", alias="color"))
# @app.param(String(key="param4", alias="pos_x"))
# @app.param(String(key="param5", alias="pos_y"))
# @app.param(Bool(key="param6", alias="relative"))
# @app.param(Int(key="param7", alias="set_start"))
# @app.param(Int(key="param8", alias="set_duration"))
@app.param(String(key="param4", alias="saveFile"))
@app.output(String(key="outputData1", alias="out1"))
def videoTxtEdit(context):
    args = context.args
    logger.info(args['inputData1'])
    logger.info(type(args['inputData1']))
    # infile=args['inFile'][0]
    #args.inputData1 = "C:/Users/wkw307/Downloads/moviepyset-0525/videoedit1.mp4"
    #infile =args['inFile'][0]
    infile = args['inputData1']
    logger.info(infile)
    logger.info(type(infile))
    logger.info(args['inputData1'])
    outfile=args['saveFile']
    clip = VideoFileClip(infile)
    #
    # # Reduce the audio volume (volume x 0.8)
    # clip = clip.volumex(0.8)
    # Generate a text clip. You can customize the font, color, etc.

    txt, fontsize, color =args['txt'], args['fontsize'], args['color']

    logger.info(args['txt'])#目前还不能有空格

    # txt_clip = TextClip("My Holidays 2013",fontsize=70,color='white')
    # txt_clip = txt_clip.set_pos(('center','bottom'), relative=True).set_start().set_duration(10)
    txt_clip = TextClip(txt=txt, fontsize=fontsize, color=color)
    txt_clip = txt_clip.set_pos(('center', 'center'), relative=True).set_start(0).set_duration(10)

    # # Overlay the text clip on the first video clip
    video = CompositeVideoClip([clip, txt_clip])
    video.write_videofile(outfile)
    app.send({"out1": outfile})
    logger.info("success!!!")

if __name__ == "__main__":
    suanpan.run(app)
    # args = {"uuid": "2b2133b6dc4d46bf815259bd61fad38d", "type": "videoEditor",
    #         "inFile": ["../sample2.mp4"],
    #         "saveFile": "../out2_ly.mp4", "subclipStart": 10, "subclipEnd": 20}
    #videoWithTextEdit(args)

