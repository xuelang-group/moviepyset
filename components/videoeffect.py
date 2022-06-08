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


from moviepy.editor import VideoFileClip, vfx
from modules.utils import MyBarLogger

@app.afterInit
def initFront(_):
    app.modules.front.init("statics/videoeditor")


def videoEffect(args):
    # args = context.args
    infile=args['inFile'][0]
    outfile=args['saveFile']

    newDu_accel_decel=args['newDuAccelDecel']
    abruptness=args['abruptness']
    soonness=args['soonness']

    RGB_blackwhite=args['RGBBlackwhite']  
    pres_lum=args['presLum'] 

    d_on=args['dOn']
    d_off=args['dOff']

    colorx_factor=args['colorxFactor']

    fadein_du=args['fadeinDu']
    fadein_color=args['fadeinColor']

    fadeout_du=args['fadeoutDu']
    fadeout_color=args['fadeoutColor']

    frz_time=args['frzTime']
    frz_duration=args['frzDuration']

    fzregion_time=args['fzregionTime']
    region=args['region']
    outside_region=args['outsideRegion']
    frzrg_mask=args['frzrgMask']

    gamma=args['gamma']

    hb_fx=args['hbFx']
    hb_fy=args['hbFy']
    r_zone=args['rZone']
    r_blur=args['rBlur']

    invertColors=args['invertColors']

    loop_num=args['loopNum']
    loop_du=args['loopDu']

    lum=args['lum']
    contrast=args['contrast']
    contrast_thr=args['contrastThr']

    cross=args['cross']

    and_otherClip=args['andOtherClip']

    or_otherClip=args['orOtherClip']

    mask_color=args['maskColor']
    mask_thr=args['maskThr']
    mask_s=args['maskS']

    mirrorX=args['mirrorX']

    mirrorY=args['mirrorY']

    saturation=args['saturation']
    black=args['black']

    scroll_w=args['scroll_w']
    scroll_h=args['scroll_h']
    x_speed=args['xSpeed']
    y_speed=args['ySpeed']
    x_start=args['xStart']
    y_start=args['yStart']

    ss_d=args['ssD']
    ss_nframes=args['ssNframes']

    timeMirror=args['timeMirror']

    timeSymmetrize=args['timeSymmetrize']

    clip = VideoFileClip(infile)
    if any([newDu_accel_decel,abruptness,soonness]):
        clip=vfx.accel_decel(clip,new_duration=newDu_accel_decel,abruptness=1.0, soonness=1.0)
    if any([RGB_blackwhite,pres_lum]):
        clip=vfx.blackwhite(clip,RGB=RGB_blackwhite, preserve_luminosity=RGB_blackwhite)
    if any([d_on,d_off]):
        clip=vfx.blink(clip,d_on=d_on,d_off=d_off)
    if any([colorx_factor]):
        clip=vfx.colorx(clip,factor=colorx_factor)
    if any([fadein_du]):
        clip=vfx.fadein(clip,duration=fadein_du, initial_color=fadein_color)
    if any([fadeout_du]):
        clip=vfx.fadeout(clip,duration=fadeout_du, initial_color=fadeout_color)
    if any([frz_duration,frz_time]):
        clip=vfx.freez(clip,clip, t=frz_time, freeze_duration=frz_duration)
    if any([frzrg_mask,fzregion_time,outside_region,region]):
        clip=vfx.freeze_region(clip,t=fzregion_time, region=region, outside_region=outside_region, mask=frzrg_mask)
    if any([gamma]):
        clip=vfx.gamma_corr(clip, gamma=gamma)
    if any([hb_fx,hb_fy,r_blur,r_zone]):
        clip=vfx.headblur(clip, fx=hb_fx, fy=hb_fy, r_zone=r_zone, r_blur=r_blur)
    if any([invertColors]):
        clip=vfx.invert_colors(clip)
    if any([loop_du,loop_num]):
        clip=vfx.loop(clip, n=loop_num, duration=loop_du)
    if any([lum,contrast,contrast_thr]):
        clip=vfx.lum_contrast(clip, lum=lum, contrast=contrast, contrast_thr=contrast_thr)
    if any([cross]):
        clip=vfx.make_loopable(clip,corss=cross)
    if any([and_otherClip]):
        otherClip=VideoFileClip(and_otherClip)
        clip=vfx.mask_and(clip,otherClip)
    if any([or_otherClip]):
        otherClip=VideoFileClip(or_otherClip)
        clip=vfx.mask_and(clip,otherClip)
    if any([mask_color,mask_s,mask_thr]):
        clip=vfx.mask_color(clip,color=mask_color, thr=mask_thr, s=mask_s)
    if any([mirrorX]):
        clip=vfx.mirror_x(clip)
    if any([mirrorY]):
        clip=vfx.mirror_y(clip)   
    if any([saturation,black]):
        clip=vfx.painting(clip,saturation=saturation,black=black)
    if any([scroll_h,scroll_w,x_speed,y_speed,x_start,y_start]):
        clip=vfx.scroll(clip,h=None, w=None, x_speed=0, y_speed=0, x_start=0, y_start=0)
    if any([ss_d,ss_nframes]):
        clip=vfx.supersample(clip,d=ss_d,nframes=ss_nframes)
    if any([timeMirror]):
        clip=vfx.time_mirror(clip)
    if any([timeSymmetrize]):
        clip=vfx.time_symmetrize(clip)

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
