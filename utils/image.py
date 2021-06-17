# -*- coding: utf-8 -*-
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
