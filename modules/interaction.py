# coding=utf-8

import suanpan
from suanpan import app
from suanpan.app.modules.base import Module

from suanpan.path import safeMkdirsForFile
from utils import *

import utils
import json
import os
import sys
sys.path.append("./")
from components.videoedit import videoEdit

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

    # 自定义目录存放日志文件(想改成存在内存里)
    log_path = os.path.join(".", "configs", "latest",args['uuid'],"log.txt")
    safeMkdirsForFile(log_path)
    log_file_name = log_path
    sys.stdout=Logger(log_file_name)

    if args["type"]=="videoEditor": #正在开发多线程
        videoEdit(args)

    sys.stdout.flush()


@module.on("general.stop")
def general_stop():


'''
本地跑的demo:
context={"args":{"uuid": "2b2133b6dc4d46bf815259bd61fad38d","type": "videoEditor",
"inFile": ["C:/Users/yiyun.zy/Desktop/xuelangyun/moviepyset/sample1.mp4"],
"saveFile":"out.mp4","subclipStart": 10,"subclipEnd": 20}}

run_videoEditor(context)
'''
