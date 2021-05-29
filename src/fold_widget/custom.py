# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize


class CustomWidget(QWidget):
    def __init__(self, item, *args, **kwargs):
        super(CustomWidget, self).__init__(*args, **kwargs)
        self.oldSize = None
        self.item = item
        layout = QFormLayout(self)
        layout.addRow('我是label', QLineEdit(self))
        layout.addRow('点击', QCheckBox('隐藏下面的按钮', self, toggled=self.hideChild))
        self.button = QPushButton('我是被隐藏的', self)
        layout.addRow(self.button)

    def hideChild(self, v):
        self.button.setVisible(not v)
        # 这里很重要 当隐藏内部子控件时 需要重新计算高度
        self.adjustSize()

    def resizeEvent(self, event):
        # 解决item的高度问题
        super(CustomWidget, self).resizeEvent(event)
        self.item.setSizeHint(QSize(self.minimumWidth(), self.height()))


class CustomButton(QPushButton):
    # 按钮作为开关

    def __init__(self, item, *args, **kwargs):
        super(CustomButton, self).__init__(*args, **kwargs)
        self.item = item
        self.onClick_fun = None
        # self.setCheckable(True)  # 设置可选中

    def resizeEvent(self, event):
        # 解决item的高度问题
        super(CustomButton, self).resizeEvent(event)
        self.item.setSizeHint(QSize(self.minimumWidth(), self.height()))

    def onClick_button(self):
        if callable(self.onClick_fun):
            self.onClick_fun()