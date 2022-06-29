# coding=utf-8

from suanpan.app import app
from suanpan.app.modules.base import Module
from suanpan.log import logger

socketapi = Module()

@socketapi.fn
def appProgress(data):
    app.sio.emit("app.progress", data)


@socketapi.on("app.get.config")
def appGetConfig(context):
    args = context.args
    logger.info(args)
    return {
            "src": r"C:\Users\yanqing.yqh\Pictures\63109.jpg",
            "tgt": r"C:\Users\yanqing.yqh\Pictures",
            "startTime": "0",
            "endTime": "10",
            "height": 100,
            "width": 100,
            "volume": 20
        }

@socketapi.on("app.set.config")
def appSetConfig(context):
    args = context.args
    logger.info(args)
    return args

@socketapi.on("app.run")
def appRun(context):
    args = context.args
    logger.info(args)
    return args

@socketapi.on("app.stop")
def appStop(context):
    args = context.args
    logger.info(args)
    return args

@socketapi.on("app.check.status")
def appCheckStatus(context):
    args = context.args
    logger.info(args)
    return args
