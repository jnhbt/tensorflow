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
    return angles


def get_fonts(font_dir="./fonts"):
    fonts = []
    for font in os.listdir(font_dir):
        font = os.path.join(sys.path[0],font_dir,font)
        if os.path.exists(font):
            fonts.append(font)
    return fonts;

def gen_font_image(char,font_file,font_size=30,angle=0):
    image = Image.new("RGB",(font_size,font_size),"#ffffff")
    font = ImageFont.truetype(font_file,size=font_size)
    font_w,font_h = font.getsize(char)
    draw = ImageDraw.Draw(im=image)
    draw.text(((font_size-font_w)/2,(font_size-font_h)/2),char,fill="#000000",font=font)
    if angle != 0:
        image = rotate_image(image,angle)
    return image

def get_rotate_size(size,angle):
    radius =  math.pi*abs(angle)/180
    width,height = size
    #b*cos(radius)+b*sin(radius) = a
    # b = a/(sin(radius)+cos(radius))
    ratio = math.sin(radius)+math.cos(radius)
    if ratio > 0:
        width = int(width//ratio)
        height = int(height//ratio)
    return width,height

def rotate_image(image,angle=30):
    #将普通PIL.Image图像转成cv2图像
    image = cv2.cvtColor(np.asarray(image),cv2.COLOR_RGB2BGR)

    (h, w) = image.shape[:2]
    (cX, cY) = (w // 2, h // 2)
    # grab the rotation matrix (applying the negative of the
    # angle to rotate clockwise), then grab the sine and cosine
    # (i.e., the rotation components of the matrix)
    # -angle位置参数为角度参数负值表示顺时针旋转; 1.0位置参数scale是调整尺寸比例（图像缩放参数），建议0.75
    M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])

    # compute the new bounding dimensions of the image
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))

    # adjust the rotation matrix to take into account translation
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY

    # perform the actual rotation and return the image
    # borderValue 缺失背景填充色彩，此处为白色，可自定义
    dist =  cv2.warpAffine(image, M, (nW, nH), borderValue=(255, 255, 255))
    #将cv2图像转化成PIL.Image图像
    dist = Image.fromarray(cv2.cvtColor(dist,cv2.COLOR_BGR2RGB))
    dist = dist.resize((w,h),Image.ANTIALIAS)
    return dist

def batch_font_images(char,font_dir,img_dir,angles):
    if os.path.exists(img_dir) is False:
        os.mkdir(img_dir, 777)
    fonts = os.listdir(font_dir)
    pad_len = len(str(len(angles)*len(fonts)))
    num = 0;
    for font in fonts:
        for angle in angles:
            image = gen_font_image(char, font_dir + "/" + font, font_size, angle)
            num += 1
            image.save(img_dir + "/" + str(num).zfill(pad_len) + ".png")


if __name__ == "__main__":
    label_dict = labels.get_labels("./data/labels.txt")
    dist_dir = os.path.join(sys.path[0],"./dist")
    font_dir = os.path.join(sys.path[0],"./fonts")
    font_size = 50
    rotate = 30
    step = 1
    angles = get_angles(rotate,step)
    for (key,val) in label_dict.items():
        img_dir = dist_dir+"/"+key;
        batch_font_images(val,font_dir,img_dir,angles)
    # img_dir = dist_dir + "/test"
    # batch_font_images("你",font_dir,img_dir,angles)
    # image = gen_font_image("你", font_dir + "/STXINWEI.TTF",font_size)
    # image.show()


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

