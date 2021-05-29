# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


class custom_label(QLabel):
    def __init__(self, *args, **kwargs):
        super(custom_label, self).__init__(*args, **kwargs)
        self.label_x = 0
        self.label_y = 0
        self.mouse_x = None
        self.mouse_y = None

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.mouse_x = event.x()
        self.mouse_y = event.y()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self.mouse_x = None
        self.mouse_y = None

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        print('x={}, y={}'.format(int(event.x()), int(event.y())))


class image_label(QWidget):
    def __init__(self):
        super(image_label, self).__init__()
        self.topFiller = QWidget()
        self.topFiller.setMinimumSize(1526+100, 1023+100)
        self.image_label = custom_label(self.topFiller)
        pixmap = QPixmap("test.png")  # 按指定路径找到图片
        self.image_label.setPixmap(pixmap)  # 在label上显示图片
        self.image_label.setAlignment(Qt.AlignLeft)

        self.scroll = QScrollArea()
        self.scroll.setWidget(self.topFiller)
        vbox1 = QVBoxLayout()
        vbox1.addWidget(self.image_label)
        self.topFiller.setLayout(vbox1)

        vbox2 = QVBoxLayout()
        vbox2.addWidget(self.topFiller)
        self.scroll.setLayout(vbox2)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.scroll)
        self.setLayout(self.vbox)

    def set_topFiller_size(self):
        """根据image大小修改"""
        pass

    def show_image(self, image):  # 需要图像基础库
        image = image


# class image_label(QGraphicsView):
#     def __init__(self):
#         super(image_label, self).__init__()
#         # self.resize(300, 300)
#         #
#         # self.line = QGraphicsLineItem()
#         # self.line.setLine(0, 0, 100, 100)
#         #
#         # self.scene = QGraphicsScene()
#         # self.scene.setSceneRect(0, 0, 300, 300)
#         # self.scene.addItem(self.line)
#         #
#         # self.setScene(self.scene)
#         # self.setAlignment(Qt.AlignTop | Qt.AlignLeft)
#         self._item = QGraphicsPixmapItem()
#         self._scene = QGraphicsScene(self)
#         self.setScene(self._scene)
#         self._scene.addItem(self._item)