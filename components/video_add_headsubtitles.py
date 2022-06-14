# coding=utf-8

import abc
import os
from pydoc import cli
import tempfile
from tkinter.messagebox import NO

import suanpan
from suanpan import asyncio, error, g
from suanpan import path as spath
from suanpan import runtime
from suanpan.app import app
from suanpan.app.arguments import Json, String, Int, Bool, Float
from suanpan.log import logger
from suanpan.node import node
from suanpan.storage import storage


from moviepy.editor import *
from moviepy.video.tools.credits import credits1
#from modules.utils import MyBarLogger

from proglog import ProgressBarLogger
from pyparsing import col

@app.afterInit
def initFront(_):
    app.modules.front.init("statics/editor")


#视加入片头滚动给字幕

@app.input(String(key="inputData1", alias="inputData1"))
@app.param(String(key="param0", alias="inFile"))
@app.param(String(key="param1", alias="txt"))
@app.param(Float(key="param2", alias="txt_width"))
@app.param(String(key="param3", alias="txt_color"))
@app.param(String(key="param4", alias="font"))
@app.param(Float(key="param5", alias="font_size"))
@app.param(String(key="param6", alias="stroke_color"))
@app.param(Float(key="param7", alias="stroke_width"))
@app.param(Int(key="param8", alias="gap"))
@app.param(String(key="param9", alias="saveFile"))
@app.output(String(key="outputData1", alias="out1"))
def addSubtitlesForHead(context):
    args = context.args
    infile = args['inFile']
    outfile=args['saveFile']
    clip = VideoFileClip(infile) #加载视频文件
    txtpath = args['txt']
    txt_width = clip.size[0] if args['txt_width'] is None else args['txt_width'] 
    txt_color, font, font_size = args['txt_color'], args['font'], args['font_size']
    stroke_color, stroke_width, gap = args['stroke_color'], args['stroke_width'], args['gap']
    imageClip = credits1(txtpath, txt_width, stretch=30, color=txt_color, font=font, fontsize=font_size, stroke_color=stroke_color, stroke_width=stroke_width, gap=gap) #加载字幕文件
    w,h = clip.size
    x_speed = x_start = y_start = 0
    y_speed = 10
    print(clip.size, imageClip.size)
    imageClip = imageClip.fx(vfx.scroll, h,w,x_speed, y_speed, x_start, y_start) #设置滚动字幕以及位置、字幕速度
    finalclip = concatenate_videoclips([imageClip.set_duration(5), clip]) #合并视频和字幕
    finalclip.write_videofile(outfile)
    app.send({"out1": outfile})

    clip.close()
    finalclip.close()

if __name__ == "__main__":
    suanpan.run(app)
    # args = {"uuid": "2b2133b6dc4d46bf815259bd61fad38d", "type": "videoEditor",
    #         "inFile": "./sample2.mp4",
    #         "saveFile": "./subtitle_ly.mp4", "subclipStart": 10, "subclipEnd": 20}
    # addSubtitlesForHead(args)
    


