# -*- coding: utf-8 -*-
import os

import cv2
from baseImage import IMAGE as _image
from baseImage import Rect, Point, Size
from PyQt5.QtGui import QImage, QPixmap


class IMAGE(_image):
    def cv_to_pixmap(self):
        height, width, depth = self.shape
        cvimg = self.cvtColor(cv2.cv2.COLOR_BGR2RGB)
        image = QImage(cvimg.data, width, height, width * depth, QImage.Format_RGB888)
        pixmap = QPixmap(image)
        return pixmap


def read_directory_all_pictures(directory_name):
    # 读取path路径下的所有图片
    image_array = []
    for file_name in os.listdir(directory_name):
        # 获取文件后缀名
        file_suffix = os.path.splitext(file_name)[1]
        if file_suffix in ['.jpg', '.png']:
            image_path = '{}/{}'.format(directory_name, file_name)
            result = {
                'image': IMAGE(image_path),
                'file_path': image_path,
                'file_name': file_name
            }
            image_array.append(result)
        else:
            print('该文件格式不支持读取, file_name={}'.format(file_name))
    return image_array
