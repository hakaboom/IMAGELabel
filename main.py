from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QSize
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import *
from src.fold_widget import foldWidget as pictureListWidget
from src.image_label import image_label as imageLabel
from src.system.configuration import SystemConfig
from utils import check_file
import sys
import json
import os
from loguru import logger


class MainUi(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainUi, self).__init__()
        self.SystemConfig = SystemConfig()
        self.resize(960, 540)
        self.work_path = os.path.dirname(os.path.realpath('static'))
        self.main_widget = QWidget()  # 创建窗口主部件
        self.main_layout = QHBoxLayout()  # 创建主部件的网格布局
        self.main_widget.setLayout(self.main_layout)  # 设置窗口主部件布局为网格布局

        self.setCentralWidget(self.main_widget)  # 设置窗口主部件
        # 设置窗口标题
        self.setWindowTitle("test")  # 设置窗口名

        # 工具栏
        self.picture_list = None
        self.picture_list_widget = QWidget()
        self.picture_list_widget.setObjectName('picture_list_widget')
        self.picture_list_layout = QVBoxLayout()
        self.picture_list_layout.setObjectName('picture_list_layout')

        # 图像栏
        self.image_widget = imageLabel()
        self.main_layout.addWidget(self.picture_list_widget)
        self.main_layout.addWidget(self.image_widget)

        self.main_layout.setStretch(0, 1)
        self.main_layout.setStretch(1, 10)
        self.main_layout.setSpacing(0)

        self.init_picture_list()

    def init_picture_list(self):
        self.picture_list = pictureListWidget(self.SystemConfig, self.image_widget)
        self.picture_list_layout.addWidget(self.picture_list)
        self.picture_list_widget.setLayout(self.picture_list_layout)


import sys, os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import (QApplication, QWidget, QSplitter, QVBoxLayout,
                            QGroupBox, QScrollArea, QRadioButton, QCheckBox,
                            QLabel)
from PyQt5.QtGui import QPixmap,QPalette
from PyQt5.QtCore import Qt


class Demo(QWidget):
    def __init__(self, parent=None):
        super(Demo, self).__init__(parent)
        self.setWindowTitle('实战PyQt5: QScrollArea Demo!')
        # 设置窗口大小
        self.resize(480, 360)
        self.initUi()

    def initUi(self):
        mainLayout = QVBoxLayout(self)

        hSplitter = QSplitter(Qt.Horizontal)

        saLeft = QScrollArea(self)
        disp_img = QLabel(self)
        disp_img.setPixmap(QPixmap('./cache/test.jpg'))

        saLeft.setBackgroundRole(QPalette.Dark)
        saLeft.setWidget(disp_img)

        # saRight = QScrollArea(self)
        # # 滚动区域的Widget
        # scrollAreaWidgetContents = QWidget()
        # vLayout = QVBoxLayout(scrollAreaWidgetContents)
        # vLayout.addWidget(self.createFirstExclusiveGroup())
        # vLayout.addWidget(self.createSecondExclusiveGroup())
        # vLayout.addWidget(self.createNonExclusiveGroup())
        # scrollAreaWidgetContents.setLayout(vLayout)
        # saRight.setWidget(scrollAreaWidgetContents)

        hSplitter.addWidget(saLeft)
        # hSplitter.addWidget(saRight)

        mainLayout.addWidget(hSplitter)
        self.setLayout(mainLayout)

    def createFirstExclusiveGroup(self):
        groupBox = QGroupBox('Exclusive Radio Buttons', self)

        radio1 = QRadioButton('&Radio Button 1', self)
        radio1.setChecked(True)
        radio2 = QRadioButton('R&adio button 2', self)
        radio3 = QRadioButton('Ra&dio button 3', self)

        vLayout = QVBoxLayout(groupBox)
        vLayout.addWidget(radio1)
        vLayout.addWidget(radio2)
        vLayout.addWidget(radio3)
        vLayout.addStretch(1)

        groupBox.setLayout(vLayout)

        return groupBox

    def createSecondExclusiveGroup(self):
        groupBox = QGroupBox('E&xclusive Radio Buttons', self)
        groupBox.setCheckable(True)
        groupBox.setChecked(True)

        radio1 = QRadioButton('Rad&io button1', self)
        radio1.setChecked(True)
        radio2 = QRadioButton('Radi&o button2', self)
        radio3 = QRadioButton('Radio &button3', self)
        chkBox = QCheckBox('Ind&ependent checkbox', self)

        vLayout = QVBoxLayout(groupBox)
        vLayout.addWidget(radio1)
        vLayout.addWidget(radio2)
        vLayout.addWidget(radio3)
        vLayout.addWidget(chkBox)
        vLayout.addStretch(1)

        groupBox.setLayout(vLayout)

        return groupBox

    def createNonExclusiveGroup(self):
        groupBox = QGroupBox('No-Exclusive Checkboxes', self)
        groupBox.setFlat(True)

        chBox1 = QCheckBox('&Checkbox 1')
        chBox2 = QCheckBox('C&heckbox 2')
        chBox2.setChecked(True)
        tristateBox = QCheckBox('Tri-&state buttton')
        tristateBox.setTristate(True)
        tristateBox.setCheckState(Qt.PartiallyChecked)

        vLayout = QVBoxLayout(groupBox)
        vLayout.addWidget(chBox1)
        vLayout.addWidget(chBox2)
        vLayout.addWidget(tristateBox)
        vLayout.addStretch(1)

        groupBox.setLayout(vLayout)

        return groupBox


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = Demo()
    myWin.show()
    sys.exit(app.exec_())
