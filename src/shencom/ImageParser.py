#!/usr/bin/python
# -*- coding: UTF-8 -*-

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import numpy as np
import cv2
import random
import copy

class  ImageParser:
    def __init__(self,width, height,need_crop=True, margin=4):
        self.width = width
        self.height = height
        self.need_crop = need_crop
        self.margin = margin

    def fontToImage(self, font_path, char, rotate=0):
        # 黑色背景
        img = Image.new("RGB", (self.width, self.height), "black")
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(font_path, int(self.width * 0.7), )
        # 白色字体
        draw.text((0, 0), char, (255, 255, 255), font=font)
        if rotate != 0:
            img = img.rotate(rotate)
        data = list(img.getdata())
        sum_val = 0
        for i_data in data:
            sum_val += sum(i_data)
        if sum_val > 2:
            np_img = np.asarray(data, dtype='uint8')
            np_img = np_img[:, 0]
            np_img = np_img.reshape((self.height, self.width))
            cropped_box = self.findImageBBox(np_img)
            left, upper, right, lower = cropped_box
            np_img = np_img[upper: lower + 1, left: right + 1]
            if not self.need_crop:
                np_img = self.imageFillBg(np_img,self.width,self.height,self.margin)
            # cv2.imwrite(path_img, np_img)
            return np_img
        else:
            print("img doesn't exist.")

    @classmethod
    def findImageBBox(self,img):
        height = img.shape[0]
        width = img.shape[1]
        v_sum = np.sum(img, axis=0)
        h_sum = np.sum(img, axis=1)
        left = 0
        right = width - 1
        top = 0
        low = height - 1
        # 从左往右扫描，遇到非零像素点就以此为字体的左边界
        for i in range(width):
            if v_sum[i] > 0:
                left = i
                break
        # 从右往左扫描，遇到非零像素点就以此为字体的右边界
        for i in range(width - 1, -1, -1):
            if v_sum[i] > 0:
                right = i
                break
        # 从上往下扫描，遇到非零像素点就以此为字体的上边界
        for i in range(height):
            if h_sum[i] > 0:
                top = i
                break
        # 从下往上扫描，遇到非零像素点就以此为字体的下边界
        for i in range(height - 1, -1, -1):
            if h_sum[i] > 0:
                low = i
                break
        return (left, top, right, low)

    @classmethod
    def imageFillBg(self,cv2_img):
        # 确定有效字体区域，原图减去边缘长度就是字体的区域
        if self.margin is not None:
            width_min_margin = max(2, self.width - self.margin)
            height_min_margin = max(2, self.height - self.margin)
        else:
            width_min_margin = self.width
            height_min_margin = self.height

        #cur_height, cur_width = cv2_img.shape[:2]
        if len(cv2_img.shape) > 2:
            pix_dim = cv2_img.shape[2]
        else:
            pix_dim = None

        resized_img = self.resize(cv2_img)

        if self.auto_avoid_fill_bg:
            fill_bg = self.is_need_fill_bg(cv2_img)

        ## should skip horizontal stroke
        if not fill_bg:
            ret_img = cv2.resize(resized_img, (width_min_margin,height_min_margin))
        else:
            if pix_dim is not None:
                norm_img = np.zeros((height_min_margin,width_min_margin,
                                     pix_dim),
                                    np.uint8)
            else:
                norm_img = np.zeros((height_min_margin,width_min_margin),
                                    np.uint8)
            # 将缩放后的字体图像置于背景图像中央
            ret_img = self.put_img_into_center(norm_img, resized_img)

        if self.margin is not None:
            if pix_dim is not None:
                norm_img = np.zeros((self.height,
                                     self.width,
                                     pix_dim),
                                    np.uint8)
            else:
                norm_img = np.zeros((self.height,
                                     self.width),
                                    np.uint8)
            ret_img = self.put_img_into_center(norm_img, ret_img)
        return ret_img

    @classmethod
    def resize(self,cv2_img,max_width,max_height):
        cur_height, cur_width = cv2_img.shape[:2]
        ratio_w = float(max_width) / float(cur_width)
        ratio_h = float(max_height) / float(cur_height)
        ratio = min(ratio_w, ratio_h)

        new_size = (min(int(cur_width * ratio), max_width),
                    min(int(cur_height * ratio), max_height))

        new_size = (max(new_size[0], 1),
                    max(new_size[1], 1),)

        resized_img = cv2.resize(cv2_img, new_size)
        return resized_img

    @classmethod
    def is_need_fill_bg(self, cv2_img, th=0.5, max_val=255):
        image_shape = cv2_img.shape
        height, width = image_shape
        if height * 3 < width:
            return True
        if width * 3 < height:
            return True
        return False

    @classmethod
    def add_noise(cls, img):
        for i in range(20):  # 添加点噪声
            temp_x = np.random.randint(0, img.shape[0])
            temp_y = np.random.randint(0, img.shape[1])
            img[temp_x][temp_y] = 255
        return img

    @classmethod
    def add_erode(cls, img):
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        img = cv2.erode(img, kernel)
        return img

    @classmethod
    def add_dilate(cls, img):
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        img = cv2.dilate(img, kernel)
        return img

    @classmethod
    def aug_list(self, noise,dilate,erode,img_list=[]):
        aug_list = copy.deepcopy(img_list)
        for i in range(len(img_list)):
            im = img_list[i]
            if noise and random.random() < 0.5:
                im = self.add_noise(im)
            if dilate and random.random() < 0.5:
                im = self.add_dilate(im)
            elif erode:
                im = self.add_erode(im)
            aug_list.append(im)
        return aug_list


