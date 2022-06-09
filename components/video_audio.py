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


#视频替换音频

@app.input(String(key="inputData1", alias="inputData1"))
@app.param(Json(key="param0", alias="inVideoFile"))
@app.param(Json(key="param1", alias="inAudioFile"))
@app.param(String(key="param2", alias="saveAudioFile"))
@app.param(String(key="param3", alias="saveVideoFile"))
@app.param(Int(key="param4", alias="split_start"))
@app.param(Int(key="param5", alias="split_end"))
@app.output(String(key="outputData1", alias="out1"))
def videoAudio(context):
    args = context.args
    infile_video = args['inVideoFile'][0]
    infile_audio = args['inAudioFile'][0]
    outfile_audio = args['saveAudioFile']
    outfile_video = args['saveVideoFile']
    clip = VideoFileClip(infile_video)
    #提取音频
    clip.audio.write_audiofile(filename=outfile_audio)

    #删除视频中的音频
    video_without_audio = clip.without_audio()
    video_without_audio.write_videofile("../without_audio.mp4")
    #添加音频并循环--以视频长度为准
    split_start = args["split_start"]
    split_end = args["split_end"]
    audio_clip = AudioFileClip(infile_audio).subclip(split_start,split_end)
    audio_clip = afx.audio_loop(audio_clip, duration=video_without_audio.duration)
    video = video_without_audio.set_audio(audio_clip)
    video.write_videofile(filename=outfile_video)
    app.send({"out1": outfile_video})

if __name__ == "__main__":
    suanpan.run(app)

