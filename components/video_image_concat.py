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
from moviepy import editor
from moviepy.editor import *
#from modules.utils import MyBarLogger

from proglog import ProgressBarLogger

@app.afterInit
def initFront(_):
    app.modules.front.init("statics/editor")
# class MyBarLogger(ProgressBarLogger):
#     #@module.on("general.checkStatus")
#     def callback(self, **changes):
#         bars = self.state.get('bars')
#         index = len(bars.values()) - 1
#         if index > -1:
#             bar = list(bars.values())[index]
#             progress = int(bar['index'] / bar['total'] * 100)
#             #print(bar)
#             print(progress)
#             #增加算盘独有的像前端传入数据的接口
#             #app.sio.emit("general.checkStatus",progress)



@app.input(String(key="inputData1", alias="inputData1"))
@app.param(String(key="param0", alias="inFile"))
@app.param(String(key="param1", alias="saveFile"))
@app.param(String(key="param2", alias="imagePath"))
@app.param(Int(key="param3", alias="start"))
@app.output(String(key="outputData1", alias="out1"))
#视频中间加入一张图片当作图片的某一帧
def videoImageConcat(context):
    args = context.args
    infile=args['inFile']
    outfile=args['saveFile']

    clip = VideoFileClip(infile)
    # tfreeze = 20 #插入的时间

    clip_before = clip.subclip(0, args['start'])
    clip_after = clip.subclip(args['start'], clip.duration)

    # im_freeze = clip.to_ImageClip(tfreeze,with_mask=False).set_opacity(0.5)
    # im_freeze.save_frame("../insert_image.png")

    #选图片
    image_clip = ImageClip(args['imagePath'])

    # painting_txt = (CompositeVideoClip([im_freeze, image_clip.set_pos('center')])
    #                 .add_mask()
    #                 .set_duration(3)
    #                 .crossfadein(0.5)
    #                 .crossfadeout(0.5))

    #合并
    final = concatenate_videoclips([clip_before,
                            image_clip.set_duration(5),
                            clip_after])
    logger.info(final.duration)
    final.write_videofile(outfile)
    app.send({"out1": outfile})

if __name__ == "__main__":
    suanpan.run(app)
    # args = {"uuid": "2b2133b6dc4d46bf815259bd61fad38d", "type": "videoEditor",
    #         "inFile": ["../sample2.mp4"],
    #         "saveFile": "../out3_image_ly.mp4", "subclipStart": 10, "subclipEnd": 20}
    # videoImageConcat(args)
