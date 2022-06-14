# coding=utf-8

import abc
import os
import tempfile
import suanpan
from suanpan import asyncio, error, g
from suanpan import path as spath
from suanpan import runtime
from suanpan.app import app
from suanpan.app.arguments import Json, String, Int, Float
from suanpan.log import logger
from suanpan.node import node
from suanpan.storage import storage
from moviepy.editor import *
from moviepy.video.tools.interpolators import Trajectory
from moviepy.video.tools.tracking import manual_tracking
# from modules.utils import MyBarLogger

@app.afterInit
def initFront(_):
    app.modules.front.init("statics/editor")

@app.input(String(key="inputData1", alias="inputData1"))
@app.param(String(key="param0", alias="inFile"))
@app.param(String(key="param1", alias="saveFile"))
@app.param(Int(key="param2", alias="blur_radius"))
@app.param(Float(key="param3", alias="fps"))
@app.param(String(key="param4", alias="tmptxt"))
@app.output(String(key="outputData1", alias="out1"))
#视频中人脸追踪以及马赛克
def videoTrackHeadblur(context):
    args = context.args
    infile=args['inFile']
    outfile=args['saveFile']
    # 手动跟踪标记头部
    # autoTrack()
    fps = clip.fps if args['fps'] is None else args['fps']
    blur_radius = args['blur_radius']
    tmptxt = args['tmptxt']
    clip = VideoFileClip(infile)#加载视频文件
    manual_tracking(clip, fps=fps, savefile=tmptxt)#手动跟踪标记头部，并保存
    #加载跟踪标记,并转换到Trajectory插值fx(t), fy(t)
    trajectory = Trajectory.from_file(tmptxt)
    # 在视频剪辑中的时点位置，模糊头部
    finalclip = clip.fx(vfx.headblur, trajectory.xi, trajectory.yi, blur_radius)
    finalclip.write_videofile(outfile)
    app.send({"out1": outfile})
    clip.close()
    finalclip.close()

if __name__ == "__main__":
    suanpan.run(app)
    # args = {"uuid": "2b2133b6dc4d46bf815259bd61fad38d", "type": "videoEditor",
    #         "inFile": "./孤独的美食家12.mp4",
    #         "saveFile": "./subtitle_ly.mp4", "subclipStart": 10, "subclipEnd": 20}
    # videoTrackHeadblur(args)
