# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function
import logging
import yaml
import copy
import json

from suanpan import g
from suanpan.storage import storage
from suanpan.path import safeMkdirsForFile
from suanpan.app import app
from suanpan.log import logger
from suanpan.app.modules.base import Module
import os
import sys
import time
import threading
from proglog import ProgressBarLogger

sys.path.append("./")
from components.videoedit import *
import inspect
import ctypes
module = Module()

class Job(threading.Thread):
 
    # def __init__(self, target,*args, **kwargs):
    def __init__(self, *args, **kwargs):
        super(Job, self).__init__(*args, **kwargs)
        self.__flag = threading.Event()   # 用于暂停线程的标识
        self.__flag.set()    # 设置为True
        self.__running = threading.Event()   # 用于停止线程的标识
        self.__running.set()   # 将running设置为True

    def run(self):
        while self.__running.isSet():
            self.__flag.wait()   # 为True时立即返回, 为False时阻塞直到内部的标识位为True后返回
            if self._target:
                self._target(*self._args, **self._kwargs)
                break   
      
    def pause(self):
        self.__flag.clear()   # 设置为False, 让线程阻塞
 
    def resume(self):
        self.__flag.set()  # 设置为True, 让线程停止阻塞
 
    def stop(self):
        self.__flag.set()    # 将线程从暂停状态恢复, 如何已经暂停的话
        self.__running.clear()    # 设置为False  



def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")
        
def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)
     

class MyBarLogger(ProgressBarLogger):
    @module.on("general.checkStatus")
    def callback(self, **changes):
        bars = self.state.get('bars')
        index = len(bars.values()) - 1
        if index > -1:
            bar = list(bars.values())[index]
            progress = int(bar['index'] / bar['total'] * 100)
            #print(bar)
            # print(progress)
            #增加算盘独有的像前端传入数据的接口
            app.sio.emit("general.checkStatus",progress)
  
# if __name__ == '__main__':
#     context={"args":{"uuid": "2b2133b6dc4d46bf815259bd61fad38d","type": "videoEditor","inFile": ["C:/Users/yiyun.zy/Desktop/xuelangyun/moviepyset/sample2.mp4"],"saveFile":"out.mp4","subclipStart": 0,"subclipEnd": 20}}
#     args=context["args"]
#     globals()['node'+args["uuid"]]=Job(target = videoEdit, kwargs=context)
#     globals()['node'+args["uuid"]].start()
    # time.sleep(2)
    # stop_thread(globals()['node'+args["uuid"]])

