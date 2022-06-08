from proglog import ProgressBarLogger
from moviepy.editor import *
import threading

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

# def videoEdit(args):
#     # args = context.args
#     # infile=args['inFile'][0]
#     # outfile=args['saveFile']
#     # subclip_start=args['subclipStart']
#     # subclip_end=args['subclipEnd']
#     # clip = VideoFileClip(infile).subclip(subclip_start,subclip_end)
#     # #my_logger = MyBarLogger()
#     #clip.write_videofile(outfile)
#     while True:
#         socketio.sleep(2)
#         t = random.randint(1, 100)
#         print(t)
#         socketio.emit('server_response', {'data': t}, namespace='/test_conn')
#     # clip.write_videofile(outfile, logger=my_logger)


class MyBarLogger(ProgressBarLogger):
    # @module.on("general.checkStatus")
    def callback(self, **changes):
        bars = self.state.get('bars')
        index = len(bars.values()) - 1
        if index > -1:
            bar = list(bars.values())[index]
            progress = int(bar['index'] / bar['total'] * 100)
            socketio.sleep(0.1)
            print(progress)
            socketio.emit('server_response', {'data': progress}, namespace='/test_conn')
            # client.send((progress).to_bytes(length=1, byteorder='big')) #send bytes
            #print(bar)

            #增加算盘独有的像前端传入数据的接口
            # app.sio.emit("general.checkStatus",progress)


#!/usr/bin/env python
# -*- coding: utf-8 -*-
from werkzeug import *
from flask import Flask, render_template
from flask_socketio import SocketIO
from threading import Lock
import random


async_mode = None
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)
thread = None
thread_lock = Lock()
context={"args":{"uuid": "2b2133b6dc4d46bf815259bd61fad38d","type": "videoEditor","inFile": ["C:/Users/yiyun.zy/Desktop/xuelangyun/moviepyset/sample1.mp4"],"saveFile":"C:/Users/yiyun.zy/Desktop/xuelangyun/moviepyset/out.mp4","subclipStart": 0,"subclipEnd": 20}}
args=context["args"]
@app.route('/')
def index():
    return render_template('index.html', async_mode=socketio.async_mode)

@socketio.on('connect', namespace='/test_conn')
def test_connect():
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(target = videoEdit)

def videoEdit():
    # args = context.args
    infile=args['inFile'][0]
    outfile=args['saveFile']
    subclip_start=args['subclipStart']
    subclip_end=args['subclipEnd']
    clip = VideoFileClip(infile).subclip(subclip_start,subclip_end)
    my_logger = MyBarLogger()
    #clip.write_videofile(outfile)
    # while True:
    #     socketio.sleep(2)
    #     t = random.randint(1, 100)
    #     print(t)
    #     socketio.emit('server_response', {'data': t}, namespace='/test_conn')
    #
    clip.write_videofile(outfile, logger=my_logger)

# def background_thread():
#     while True:
#         socketio.sleep(2)
#         t = random.randint(1, 100)
#         socketio.emit('server_response', {'data': t}, namespace='/test_conn')

@socketio.on('disconnect', namespace='/chat')
def test_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app, debug=True)