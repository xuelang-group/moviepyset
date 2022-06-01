# coding=utf-8

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
    if args["type"]=="audioEditor": #多线程
        globals()['node'+args["uuid"]]=Job(target = audioEdit, kwargs=context)
        globals()['node'+args["uuid"]].start()


@module.on("general.stop")
def general_stop(context):
    args=context['args']
    stop_thread(globals()['node'+args["uuid"]])
