# coding=utf-8

import abc
import os
import tempfile

import suanpan
from suanpan import asyncio, error, g
from suanpan import path as spath
from suanpan import runtime
from suanpan.app import app
from suanpan.app.arguments import Json, String, Int
from suanpan.log import logger
from suanpan.node import node
from suanpan.storage import storage


from moviepy.editor import *
from modules.utils import MyBarLogger

@app.afterInit
def initFront(_):
    app.modules.front.init("statics/videoeditor")


def videoEdit(args):
    # args = context.args
    infile=args['inFile']
    outfile=args['saveFile']
    subclip_start=args['subclipStart']
    subclip_end=args['subclipEnd']
    speed_factor=args['speedFactor']
    speed_duration=args['speedDuration']
    resize_newsize=args['resizeNewsize'] #can be (width,height), scale, A function of time returning one of these.
    resize_h=args['resizeWidth']
    resize_w=args['resizeHeight']    
    crop_x1=args['crop_x1']
    crop_y1=args['crop_y1']
    crop_x2=args['crop_x2']
    crop_y2=args['crop_y2']
    crop_w=args['crop_w']
    crop_h=args['crop_h']
    crop_x_center=args['crop_x_center']
    crop_y_center=args['crop_y_center']
    rot_angle=args['rotAngle']
    rot_unit=args['rotUnit']
    rot_resample=args['rotResample']
    mar_all=args['mar_all']
    mar_l=args['mar_l']
    mar_r=args['mar_r']
    mar_t=args['mar_t']
    mar_b=args['mar_b']
    mar_color=args['marColor']
    opacity=args['opacity']

    clip = VideoFileClip(infile)
    if subclip_start is not None and subclip_end is not None:
        clip=clip.subclip(subclip_start,subclip_end)
    if speed_factor is not None or speed_duration is not None:
        clip=clip.speedx(factor=speed_factor, final_duration=speed_duration)
    clip=clip.crop(x1=crop_x1, y1=crop_y1, x2=crop_x2, y2=crop_y2, width=crop_w, height=crop_h, x_center=crop_x_center, y_center=crop_y_center)
    if any([resize_newsize,resize_h,resize_w]):
        clip=clip.resize(newsize=resize_newsize, height=resize_h, width=resize_w)
    if any([rot_angle,rot_unit,rot_resample]):
        clip=clip.rotate(angle=rot_angle, unit=rot_unit, resample=rot_resample)
    if any([mar_all,mar_l,mar_r,mar_t,mar_b,mar_color,opacity]):
        clip=clip.margin(mar=mar_all, left=mar_l, right=mar_r, top=mar_t, bottom=mar_b, color=mar_color, opacity=opacity)

    my_logger = MyBarLogger()
    if any(['.mp4','.flv','.wmv','.rm','.avi','.webm','.rmvb']) in list(outfile):
        clip.write_videofile(outfile, logger=my_logger)
    elif any(['.gif']) in list(outfile):
        clip.write_gif(outfile, logger=my_logger)
    elif any(['.mp3','.wav','.m4v']) in list(outfile):
        clip.write_audiofile(outfile, logger=my_logger)
    app.send({"out1": outfile})

if __name__ == "__main__":
    suanpan.run(app)
