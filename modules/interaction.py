# coding=utf-8

from components.videdo_track_headblur import videoTrackHeadblur
from components.video_add_headsubtitles import addSubtitlesForHead
from components.video_add_tailsubtitles import addSubtitlesForTail
import suanpan
from suanpan import app
from suanpan.app.modules.base import Module

from suanpan.path import safeMkdirsForFile

from utils import *

import json
import os
import sys
sys.path.append("./")
from components.videoedit import *
from components.videoeffect import *
from components.videoconcat import *
from components.subtitlecomposite import *
from components.image_to_video import *
from components.video_audio import videoAudio
from components.video_image_concat import videoImageConcat
from components.video_image_edit import videoImageEdit
from components.video_txt_edit import videoTxtEdit

module = Module()


@module.fn
def init(editors):
    app.modules.enable("storage")
    app.modules.enable("params")
    return module.const("editors", editors)


@module.fn
def initFrontVE():
    app.sio.setStatic("statics/videoEditor")


# @module.on("general.saveConfig") 保存设置先和run合并
def saveConfig(args):
    LOCAL_LATEST = os.path.join(".", "configs", "latest",args['uuid'],"configurations.json")
    safeMkdirsForFile(LOCAL_LATEST)
    with open(LOCAL_LATEST, "w") as f:
        json.dump(args, f)





@module.on("general.run")
def run_videoEditor(context):
    args=context['args'] #or context.args看到时候那个跑的起
    saveConfig(args)

    if args["type"]=="videoEditor": #多线程
        globals()['node'+args["uuid"]]=Job(target = videoEdit, kwargs=context)
        globals()['node'+args["uuid"]].start()
    if args["type"]=="videoEffect": #多线程
        globals()['node'+args["uuid"]]=Job(target = videoEffect, kwargs=context)
        globals()['node'+args["uuid"]].start()
    if args["type"]=="videoConcat": #多线程
        globals()['node'+args["uuid"]]=Job(target = videoConcat, kwargs=context)
        globals()['node'+args["uuid"]].start()
    if args["type"]=="subtitleComposite": #多线程
        globals()['node'+args["uuid"]]=Job(target = subtitleComposite, kwargs=context)
        globals()['node'+args["uuid"]].start()

    if args["type"]=="imageToVideo": #多线程
        globals()['node'+args["uuid"]]=Job(target = imageToVideo, kwargs=context)
        globals()['node'+args["uuid"]].start()
    if args["type"]=="videoTrackHeadblur": #多线程
        globals()['node'+args["uuid"]]=Job(target = videoTrackHeadblur, kwargs=context)
        globals()['node'+args["uuid"]].start()
    if args["type"]=="addSubtitlesForHead": #多线程
        globals()['node'+args["uuid"]]=Job(target = addSubtitlesForHead, kwargs=context)
        globals()['node'+args["uuid"]].start()
    if args["type"]=="addSubtitlesForTail": #多线程
        globals()['node'+args["uuid"]]=Job(target = addSubtitlesForTail, kwargs=context)
        globals()['node'+args["uuid"]].start()
    if args["type"]=="videoAudio": #多线程
        globals()['node'+args["uuid"]]=Job(target = videoAudio, kwargs=context)
        globals()['node'+args["uuid"]].start()
    if args["type"]=="videoImageConcat": #多线程
        globals()['node'+args["uuid"]]=Job(target = videoImageConcat, kwargs=context)
        globals()['node'+args["uuid"]].start()
    if args["type"]=="videoImageEdit": #多线程
        globals()['node'+args["uuid"]]=Job(target = videoImageEdit, kwargs=context)
        globals()['node'+args["uuid"]].start()
    if args["type"]=="videoTxtEdit": #多线程
        globals()['node'+args["uuid"]]=Job(target = videoTxtEdit, kwargs=context)
        globals()['node'+args["uuid"]].start()

@module.on("general.stop")
def general_stop(context):
    args=context['args']
    stop_thread(globals()['node'+args["uuid"]])
