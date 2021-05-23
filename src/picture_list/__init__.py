# -*- coding: utf-8 -*-
from .custom import CustomButton, CustomWidget
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize


class foldWidget(QListWidget):
    def __init__(self, *args, **kwargs):
        super(foldWidget, self).__init__(*args, **kwargs)
        self.btn_item = []
        for _ in range(5):
            item = QListWidgetItem(self)
            btn = CustomButton(item, 'image' + str(_), objectName='image_btn')
            self.setItemWidget(item, btn)
            self.btn_item.append(btn)
            btn.clicked.connect(btn.onClick_button)
        # for _ in range(3):
        #     # 开关
        #     item = QListWidgetItem(self)
        #     btn = CustomButton(item, '折叠', self, objectName='image_btn')
        #     self.setItemWidget(item, btn)
        #
        #     # 被折叠控件
        #     item = QListWidgetItem(self)
        #     # 通过按钮的选中来隐藏下面的item
        #     btn.toggled.connect(item.setHidden)
        #     self.setItemWidget(item, CustomWidget(item, self))
