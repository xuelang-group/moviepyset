# coding=utf-8

import abc
import os
import tempfile

import suanpan
from suanpan import asyncio, error, g
from suanpan import path as spath
from suanpan import runtime
from suanpan.app import app
from suanpan.app.arguments import Json, String, Int, Bool,Float
from suanpan.log import logger
from suanpan.node import node
from suanpan.storage import storage
from moviepy import video
from moviepy.editor import *


@app.afterInit
def initFront(_):
    app.modules.front.init("statics/editor")


#图片转视频

@app.input(String(key="inputData1", alias="inputData1"))
@app.param(String(key="param0", alias="image_folder"))
@app.param(String(key="param1", alias="image_endswith"))
@app.param(Float(key="param2", alias="fps"))
@app.param(String(key="param3", alias="saveFile"))
@app.output(String(key="outputData1", alias="out1"))
def imageToVideo(context):
    args = context.args
    #使用的图片必须是同一分辨率
    image_folder = args["image_folder"]
    image_endswith = args["image_endswith"]
    fps = args["fps"]
    image_files = [image_folder + '/' + img for img in os.listdir(image_folder) if img.endswith(image_endswith)]
    logger.info(image_files)
    #image_files = ["C:/Users/wkw307/Downloads/moviepyset-0525/imgs/1.jpg","C:/Users/wkw307/Downloads/moviepyset-0525/imgs/2.jpg"]
    #image_files = args["inFile"]
    outfile = args["saveFile"]
    try:
        clip = video.io.ImageSequenceClip.ImageSequenceClip(image_files, fps=fps)
        clip.write_videofile(outfile)
    except:
        logger.info("the image must has the same resolution !!!")
    app.send({"out1": outfile})

if __name__ == "__main__":
    suanpan.run(app)

