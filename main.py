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


test_color = [
    '''QWidget{background-color:#ffffff;}''',
    '''QWidget{background-color:#000000;}''',
    '''QWidget{background-color:#00ff00;}''',
    '''QWidget{background-color:#0000ff;}''',
    '''QWidget{background-color:#ff0000;}''',
]


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
        self.main_layout.setStretch(1, 6)
        self.main_layout.setSpacing(0)

        self.init_picture_list()

    def init_picture_list(self):
        self.picture_list = pictureListWidget(self.SystemConfig)

        self.picture_list_btn_clicked(self.picture_list.btn_item)
        self.picture_list_layout.addWidget(self.picture_list)

        self.picture_list_widget.setLayout(self.picture_list_layout)

    def read_configuration_file(self):
        if not check_file(self.load_file_name):
            pass

    # picture_list中的按钮回调事件
    def picture_list_btn_clicked(self, picture_list):
        for index, btn in enumerate(picture_list):
            def onClick_fun():
                i = index

                def fun():
                    self.image_widget.setStyleSheet(test_color[i])
                return fun
            btn.onClick_fun = onClick_fun()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MainUi()
    myWin.show()
    sys.exit(app.exec_())