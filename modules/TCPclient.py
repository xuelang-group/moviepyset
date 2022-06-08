from socket import *
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

def videoEdit(args):
    # args = context.args
    infile=args['inFile'][0]
    outfile=args['saveFile']
    subclip_start=args['subclipStart']
    subclip_end=args['subclipEnd']
    clip = VideoFileClip(infile).subclip(subclip_start,subclip_end)
    my_logger = MyBarLogger()
    clip.write_videofile(outfile, logger=my_logger)


class MyBarLogger(ProgressBarLogger):
    # @module.on("general.checkStatus")
    def callback(self, **changes):
        bars = self.state.get('bars')
        index = len(bars.values()) - 1
        if index > -1:
            bar = list(bars.values())[index]
            progress = int(bar['index'] / bar['total'] * 100)
            client.send((progress).to_bytes(length=1, byteorder='big')) #send bytes
            #print(bar)
            # print(progress)
            #增加算盘独有的像前端传入数据的接口
            # app.sio.emit("general.checkStatus",progress)

host_name=gethostname()
port_num=8000
client = socket(AF_INET, SOCK_STREAM)
client.connect((host_name, port_num))

context={"args":{"uuid": "2b2133b6dc4d46bf815259bd61fad38d","type": "videoEditor","inFile": ["C:/Users/yiyun.zy/Desktop/xuelangyun/moviepyset/sample2.mp4"],"saveFile":"out.mp4","subclipStart": 0,"subclipEnd": 20}}
args=context["args"]
# globals()['node'+args["uuid"]]=Job(target = videoEdit, kwargs=context)
# globals()['node'+args["uuid"]].start()
videoEdit(args)
msg = client.recv(1024) #接收服务端返回的数据，需要解码
print("got msg from server: "+ str(int.from_bytes(msg, byteorder='big')))

client.close()
