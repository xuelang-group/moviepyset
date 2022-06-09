import os

from moviepy.video.VideoClip import TextClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.io.VideoFileClip import VideoFileClip

# clip = VideoFileClip("C:/Users/wkw307/Downloads/moviepyset-0525/sample2.mp4")
# im_freeze = clip.to_ImageClip(20,with_mask=False).set_opacity(0.5)
# im_freeze.save_frame("../insert_image.png")

from PIL import Image
import os

def Reformat_Image(image_folder):
    max_size = [0, 0]
    image_files = [image_folder+'/'+img for img in os.listdir(image_folder) if img.endswith(".jpg")]
    for img_name in image_files:
        img = Image.open(img_name)
        if img.size[0] > max_size[0]:
            max_size[0] = img.size[0]
        if img.size[1] > max_size[1]:
            max_size[1] = img.size[1]
        global size1
        size1 = max_size[0]
        global size2
        size2 = max_size[1]

    num = 1
    for img_name2 in image_files:
        background = Image.new('RGBA', (max_size[0], max_size[1]), (255,255,255))
        img1 = Image.open(img_name2)
        img1 = img1.convert('RGBA')
        parameter1 = (size1 - img1.size[0])/2
        parameter2 = (size2 - img1.size[1])/2
        background.paste(img1, (int(parameter1), int(parameter2)))
        background.save("../after_imgs/targetImg_" + "{}".format(num) + ".png")
        num += 1

# image_folder = '../imgs'
# Reformat_Image(image_folder)
clip = VideoFileClip("C:/Users/wkw307/Downloads/moviepyset-0525/sample1.mp4")
txt_clip = TextClip("My Holidays 2013",fontsize=70,color='white')
txt_clip = txt_clip.set_pos(('center','bottom'), relative=True).set_start(0).set_duration(10)

    # # Overlay the text clip on the first video clip
video = CompositeVideoClip([clip, txt_clip])
video.write_videofile("tmmmppp.mp4")

#
# import os
# import moviepy.video.io.ImageSequenceClip
#
# def get_video(img_folder, fps):
#     image_files = [image_folder+'/'+img for img in os.listdir(image_folder) if img.endswith(".bmp")]
#     clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(image_files, fps=fps)
#     return clip
#     #clip.write_videofile('./video/Movie1.mp4')
#
# image_folder = '../after_imgs'
# video_dir = '../video_item1.mp4'
# fps=0.5
#
# get_video(image_folder, fps).write_videofile(video_dir)
