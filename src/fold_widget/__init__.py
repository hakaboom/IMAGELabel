# -*- coding: utf-8 -*-
from .custom import CustomButton, CustomWidget
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize


class foldWidget(QListWidget):
    def __init__(self, SystemConfig, *args, **kwargs):
        super(foldWidget, self).__init__()
        self.SystemConfig = SystemConfig
        self.btn_item = []
        for _ in range(5):
            item = QListWidgetItem(self)
            btn = CustomButton(item, 'image' + str(_), objectName='image_btn')
            self.setItemWidget(item, btn)
            self.btn_item.append(btn)
            btn.clicked.connect(btn.onClick_button)
