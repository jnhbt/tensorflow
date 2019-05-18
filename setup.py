#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import os
import random
import cv2
import numpy as np
from PIL import Image,ImageFont,ImageDraw
import math
import codecs as cs
sys.path.append(os.path.join(sys.path[0],"./src"))

from shencom import labels
from shencom.ImageParser import ImageParser

def get_angles(rotate=30,step=1):
    angles = []
    if rotate > 0 & rotate <= 45:
        for i in range(0, rotate + 1, step):
            angles.append(i)
        for i in range(-rotate, 0, step):
            angles.append(i)
    return angles;


def get_fonts(font_dir="./fonts"):
    fonts = []
    for font in os.listdir(font_dir):
        font = os.path.join(sys.path[0],font_dir,font)
        if os.path.exists(font):
            fonts.append(font)
    return fonts;

def gen_font_image(char,font_file,font_size=30,rotate=0):
    image = Image.new("RGB",(font_size,font_size),"#ffffff")
    width,height = get_rotate_size((font_size,font_size),rotate)
    print(width,height,rotate)
    font = ImageFont.truetype(font_file,size=width)
    draw = ImageDraw.Draw(im=image)
    draw.text(((font_size-width)/2,(font_size-height)/2),char,fill="#000000",font=font)
    if rotate != 0:
        image = rotate_image(image,rotate)
    return image

def get_rotate_size(size,angle):
    radius =  math.pi*angle/180
    width,height = size
    ratio = abs(math.cos(radius));
    if ratio > 0:
        width = math.floor(width*ratio)
        height = math.floor(height*ratio)
    return width,height

def rotate_image(image,rotate=30):
    front_img = image.convert("RGBA")
    front_img = front_img.rotate(rotate)
   # front_img.show()
    bg = Image.new('RGBA', front_img.size, (255, 255, 255, 255))
    dist = Image.composite(front_img, bg, mask=front_img)
    dist.convert(image.mode)
    return dist

def batch_font_images(char,font_dir,img_dir,angles):
    if os.path.exists(img_dir) is False:
        os.mkdir(img_dir, 777)
    fonts = os.listdir(font_dir)
    pad_len = len(str(len(angles)*len(fonts)))
    for font in fonts:
        for i,angle in enumerate(angles):
            image = gen_font_image(char, font_dir + "/" + font, font_size, angle)
            image.save(img_dir + "/" + str(i+1).zfill(pad_len) + ".png")


if __name__ == "__main__":
    label_dict = labels.get_labels("./data/labels.txt")
    dist_dir = os.path.join(sys.path[0],"./dist")
    font_dir = os.path.join(sys.path[0],"./fonts")
    font_size = 50
    rotate = 30
    step = 1
    angles = get_angles(rotate,step)
    # for (key,val) in label_dict.items():
    #     img_dir = dist_dir+"/"+key;
    #     batch_font_images(val,font_dir,img_dir,angles)
    img_dir = dist_dir + "/test" ;
    batch_font_images("你",font_dir,img_dir,angles)


 #   image.rotate(30)
    # label_dict = labels.get_labels("./data/labels.txt")
    # # key_list = []
    # # val_list = []
    # # for (key, val) in label_dict.items():
    # #     key_list.append(key)
    # #     val_list.append(val)
    # #
    # # chars = dict(zip(val_list, key_list))
    # rotate = 30;
    # if rotate < 0:
    #     rotate = - rotate
    # font_dir = "./fonts";
    # test_ratio = 0.2
    # img_dir = "./test";
    # width = height = 30
    # angles = get_angles(rotate);
    # #font_paths = get_fonts()
    # parser = ImageParser(width,height)
    # num = 5
    # i = 0;
    # for (key,val) in label_dict.items():
    #     i = i+1
    #     img_list = []
    #     for font in os.listdir(font_dir):
    #         font = os.path.join(sys.path[0], font_dir, font)
    #         if rotate == 0:
    #             image = parser.fontToImage(font,val)
    #             img_list.append(image)
    #         else:
    #             for i in angles:
    #                 image = parser.fontToImage(font,val,rotate)
    #                 img_list.append(image)
    #
    #     test_num = len(img_list) * test_ratio
    #     random.shuffle(img_list)  # 图像列表打乱
    #
    #     count = 0;
    #     for img in img_list:
    #         if count < test_num:
    #             char_dir = os.path.join(img_dir, key)
    #         else:
    #             char_dir = os.path.join(img_dir, key)
    #
    #         if not os.path.isdir(char_dir):
    #             os.makedirs(char_dir)
    #
    #         path_image = os.path.join(char_dir, "%d.png" % count)
    #         cv2.imwrite(path_image, img)
    #         count += 1
    #     if i>= 5:
    #         break

