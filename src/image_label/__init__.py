# -*- coding: utf-8 -*-
import PyQt5.QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from inspect import isfunction
from loguru import logger
from utils.image import IMAGE, Rect, Point, Size


class custom_label(QLabel):
    def __init__(self, *args, **kwargs):
        super(custom_label, self).__init__(*args, **kwargs)
        # 用于move事件中,记录本次触发时的光标坐标
        self.mouse_mv_now_point = None
        # 用于move事件中,上次的光标坐标
        self.mouse_mv_last_point = None
        self.left_flag = False
        self.draw_flag = False
        self.draw_start_point = None
        self.draw_end_point = None
        self.draw_rect = None
        self.mouse_press_callback = []
        self.mouse_release_callback = []
        self.mouse_move_callback = []

        self.setMouseTracking(True)  # 设置鼠标跟踪
        QShortcut(QKeySequence(self.tr("Ctrl+A")), self, self.draw_cap_rect)

    def draw_cap_rect(self):
        self.draw_flag = True
        self.draw_start_point = self.get_mouse_in_label()
        logger.debug('触发ctrl+A, 监控鼠标位置, draw_flag=True, point={}', self.draw_start_point)

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.draw_flag:
            x = [self.draw_start_point.x, self.draw_end_point.x]
            y = [self.draw_start_point.y, self.draw_end_point.y]
            lt = Point(min(x), min(y))  # leftTop
            rb = Point(max(x), max(y))  # rightButtom
            painter = QPainter(self)
            painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
            rect = Rect.create_by_2_point(lt, rb)
            self.draw_rect = rect
            painter.drawRect(rect.x, rect.y, rect.width, rect.height)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.buttons() == Qt.LeftButton:
            self.left_flag = True
            self.mouse_mv_last_point = Point(event.x(), event.y())

        if event.buttons() == Qt.LeftButton and self.draw_flag:
            self.draw_end_point = Point(event.x(), event.y())
        self.run_mouse_press_callback()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self.run_mouse_release_callback()
        # 清空所有数据
        self.mouse_mv_now_point = None
        self.mouse_mv_last_point = None
        self.left_flag = False
        self.draw_flag = False
        self.draw_start_point = None
        self.draw_end_point = None
        self.update()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        # 记录本次移动时的光标坐标
        self.mouse_mv_now_point = Point(event.x(), event.y())
        if self.draw_flag:
            self.draw_end_point = Point(event.x(), event.y())
            self.update()  # update会触发paintEvent函数
        self.run_mouse_move_callback()

    def set_mouse_press_callback(self, fun):
        self.mouse_press_callback.append(fun)

    def run_mouse_press_callback(self):
        for callback in self.mouse_press_callback:
            if isfunction(callback):
                callback(self)

    def set_mouse_release_callback(self, fun):
        self.mouse_release_callback.append(fun)

    def run_mouse_release_callback(self):
        for callback in self.mouse_release_callback:
            if isfunction(callback):
                callback(self)

    def set_mouse_move_callback(self, fun):
        self.mouse_move_callback.append(fun)

    def run_mouse_move_callback(self):
        for callback in self.mouse_move_callback:
            if isfunction(callback):
                callback(self)

    def get_mouse_in_label(self) -> Point:
        """获取鼠标在label上的坐标"""
        return self.mouse_mv_now_point


class image_label(QWidget):
    def __init__(self):
        super(image_label, self).__init__()
        self.topFiller = QWidget(self)
        self.image_label = custom_label(self.topFiller)
        self.image_label.setAlignment(Qt.AlignLeft)

        self.scroll = QScrollArea(self)
        self.scroll.setWidget(self.topFiller)
        vbox1 = QVBoxLayout(self)
        vbox1.addWidget(self.image_label)
        vbox1.setContentsMargins(0, 0, 0, 0)
        self.topFiller.setLayout(vbox1)

        vbox2 = QVBoxLayout(self)
        vbox2.addWidget(self.topFiller)
        vbox2.setContentsMargins(0, 0, 0, 0)
        self.scroll.setLayout(vbox2)

        self.vbox = QVBoxLayout(self)
        self.vbox.addWidget(self.scroll)
        self.vbox.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.vbox)

        # 设置图片
        self.image = None
        self.image_label_move_callback()
        self.image_crop_callback()

    def set_topFiller_size(self):
        """根据image大小修改"""
        pass

    def show_image(self, image: IMAGE):
        self.image = image
        pixmap = self.image.cv_to_pixmap()
        self.topFiller.setMinimumSize(pixmap.size().width(), pixmap.size().height())
        self.image_label.setPixmap(pixmap)

    def image_label_move_callback(self):
        """左键拖拽image_label,控制滑动条移动图片"""

        def move_fun():
            def callback(label: custom_label):
                if label.left_flag:
                    move_x = label.mouse_mv_last_point.x - label.mouse_mv_now_point.x
                    move_y = label.mouse_mv_last_point.y - label.mouse_mv_now_point.y
                    self.scroll.verticalScrollBar().setValue(self.scroll.verticalScrollBar().value() + move_y)
                    self.scroll.horizontalScrollBar().setValue(self.scroll.horizontalScrollBar().value() + move_x)
                    label.mouse_mv_last_point.x = label.mouse_mv_now_point.x + move_x
                    label.mouse_mv_last_point.y = label.mouse_mv_now_point.y + move_y

            return callback

        self.image_label.set_mouse_move_callback(move_fun())

    def image_crop_callback(self):
        """选框中图片裁剪"""

        def cap_fun():
            def callback(label: custom_label):
                if label.draw_flag and label.left_flag:
                    self.image.crop_image(label.draw_rect).imshow()
            return callback

        self.image_label.set_mouse_release_callback(cap_fun())

    def connect_image_label(self):
        def mouse_fun():
            def fun():
                self.scroll.verticalScrollBar().setValue(self.scroll.verticalScrollBar().value() + 100)

            return fun

        self.image_label.mouse_press_fun = mouse_fun()
