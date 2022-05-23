# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function

import yaml
import copy
import json
from suanpan import g
from suanpan.storage import storage
from suanpan.path import safeMkdirsForFile
import os,sys
import time
# LOCAL_FILE_PATH = "./configs/filePath.yaml"

# def loadConfig(path): 保存配置（和运行合一起，暂弃这些）
#     with open(path, "r", encoding="utf-8") as f:
#         config = yaml.safe_load(f)
#     return config

# path="configs/videoEditor.yaml"
# for i in loadConfig(path).values():
#     print(i)

# def loadCompConfig(path):
#     filePath = loadConfig(path)
#     configs = []

class Logger(object):
    def __init__(self, file_name, stream=sys.stdout): #之前是"Default.log"
        self.terminal = stream
        self.log = open(file_name, "a")
    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)
    def flush(self):
        self.terminal.flush()  # 不启动缓冲,实时输出
        self.log.flush()
    def close(self):
        self.log.close()        

# def saveStatus(args): 放在general.run里了
#     # 自定义目录存放日志文件
#     log_path = os.path.join(".", "configs", "latest",args['uuid'],"log.txt")
#     safeMkdirsForFile(log_path)
#     # if not os.path.exists(log_path):
#     #     os.makedirs(log_path)
#     # 日志文件名按照程序运行时间设置
#     # log_file_name = log_path + 'log-' + time.strftime("%Y%m%d-%H%M%S", time.localtime()) + '.log'
#     log_file_name = log_path
#     # 记录正常的 print 信息
#     sys.stdout = Logger(log_file_name)
    
#     # # 记录 traceback 异常信息
#     # sys.stderr = Logger(log_file_name)
  
