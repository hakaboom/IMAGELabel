# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from inspect import isfunction


class custom_label(QLabel):
    def __init__(self, *args, **kwargs):
        super(custom_label, self).__init__(*args, **kwargs)
        self.label_x = 0
        self.label_y = 0
        # 用于move事件中,记录本次触发时的光标坐标
        self.mouse_mv_now_x = 0
        self.mouse_mv_now_y = 0
        # 用于move事件中,上次的光标坐标
        self.mouse_mv_last_x = 0
        self.mouse_mv_last_y = 0
        self.left_flag = False
        self.mouse_press_callback = []
        self.mouse_release_callback = []
        self.mouse_move_callback = []

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.label_x = event.x()
        self.label_y = event.y()
        self.mouse_mv_now_x = event.x()
        self.mouse_mv_now_y = event.y()
        self.left_flag = True
        self.run_mouse_press_callback()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self.label_x = 0
        self.label_y = 0
        self.mouse_mv_now_x = 0
        self.mouse_mv_now_y = 0
        self.mouse_mv_last_x = 0
        self.mouse_mv_last_y = 0
        self.left_flag = False
        self.run_mouse_release_callback()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        # 记录本次移动时的光标坐标
        self.mouse_mv_last_x, self.mouse_mv_last_y = event.x(), event.y()
        # print(event.x(), event.y())
        self.run_mouse_move_callback()
        # 结束事件时,


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


class image_label(QWidget):
    def __init__(self):
        super(image_label, self).__init__()
        self.topFiller = QWidget()
        self.image_label = custom_label(self.topFiller)
        pixmap = QPixmap("test.png")  # 按指定路径找到图片
        self.topFiller.setMinimumSize(pixmap.size().width(), pixmap.size().height())
        self.image_label.setPixmap(pixmap)  # 在label上显示图片
        self.image_label.setAlignment(Qt.AlignLeft)

        self.scroll = QScrollArea()
        self.scroll.setWidget(self.topFiller)
        vbox1 = QVBoxLayout()
        vbox1.addWidget(self.image_label)
        vbox1.setContentsMargins(0, 0, 0, 0)
        self.topFiller.setLayout(vbox1)

        vbox2 = QVBoxLayout()
        vbox2.addWidget(self.topFiller)
        vbox2.setContentsMargins(0, 0, 0, 0)
        self.scroll.setLayout(vbox2)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.scroll)
        self.vbox.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.vbox)

        self.image_label_move_callback()

    def set_topFiller_size(self):
        """根据image大小修改"""
        pass

    def show_image(self, image):
        image = image

    def image_label_move_callback(self):
        """左键拖拽image_label,控制滑动条移动图片"""
        def move_fun():
            def callback(label: custom_label):
                if label.left_flag:
                    move_x = label.mouse_mv_now_x - label.mouse_mv_last_x
                    move_y = label.mouse_mv_now_y - label.mouse_mv_last_y
                    self.scroll.verticalScrollBar().setValue(self.scroll.verticalScrollBar().value() + move_y)
                    self.scroll.horizontalScrollBar().setValue(self.scroll.horizontalScrollBar().value() + move_x)
                    label.mouse_mv_now_x, label.mouse_mv_now_y = label.mouse_mv_last_x + move_x, \
                                                                 label.mouse_mv_last_y + move_y
            return callback
        self.image_label.set_mouse_move_callback(move_fun())

    def connect_image_label(self):
        def mouse_fun():
            def fun():
                self.scroll.verticalScrollBar().setValue(self.scroll.verticalScrollBar().value() + 100)
            return fun

        self.image_label.mouse_press_fun = mouse_fun()
