from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QMainWindow, QApplication, QShortcut
import sys
import os
import numpy as np
import threading
import cv2
import datetime

buffer = ''


class ImageLabel(QLabel):
    '''获取用户裁剪坐标点，画线
        Attributes:
            points:用户点击的裁剪点
        '''

    def __init__(self, parent=None):
        super(ImageLabel, self).__init__(parent)
        self.points = []

    # normal function
    def show_image(self, image):
        # 参数image为np.array类型
        rgb_image = cv2.cvtColor(image.copy(), cv2.COLOR_BGR2RGB)
        rgb_image = cv2.resize(rgb_image, (self.width(), self.height()))
        label_image = QImage(rgb_image.data, rgb_image.shape[1], rgb_image.shape[0], QImage.Format_RGB888)
        self.setPixmap(QPixmap(label_image))

    def reselect(self):
        self.points.clear()
        self.update()

    def get_points(self):
        return self.points

    # slot function
    # 根据点过的点来画图
    def paintEvent(self, event):
        QLabel.paintEvent(self, event)
        painter = QPainter()
        painter.begin(self)

        pen = QPen(Qt.red, 4, Qt.DashDotLine)  # 虚线画笔
        painter.setPen(pen)

        for k in range(len(self.points)):
            if k + 1 != len(self.points):
                painter.drawLine(self.points[k][0], self.points[k][1], self.points[k + 1][0], self.points[k + 1][1])
            else:
                painter.drawLine(self.points[k][0], self.points[k][1], self.points[0][0], self.points[0][1])
        painter.end()

    # 鼠标移动时候获取坐标
    def mouseMoveEvent(self, event):
        x = event.x()
        y = event.y()
        text = "x:{0},y:{1}".format(x, y)
        print(text)
        # self.ui.label_2.setText(text)

    def keyPressEvent(self, event):
        print(event.key())
        if event.key() == Qt.Key_Escape:
            self.close()

    def event(self, event):
        print(1)
        if event.type() == QEvent.KeyPress and event.key() == Qt.Key_Tab:
            self.key = '捕获tab'
            self.update()
            return True
        return QWidget.event(self, event)
    # 开启标记功能时，获取点击坐标
    # def mouseReleaseEvent(self, event):
    #     if len(self.points) < 4:
    #         global_point = event.globalPos()
    #         local_point = self.mapFromGlobal(global_point)
    #
    #         point_x = local_point.x()
    #         point_y = local_point.y()
    #         self.points.append([point_x, point_y])
    #
    #         self.update()  # 获取鼠标点击的点之后，通知画线


class cropWindow(QWidget):
    ok_signal = pyqtSignal()

    def __init__(self, image):
        super(cropWindow, self).__init__()
        self.pannel_height = 400
        self.pannel_width = 600
        self.button_height = 64
        self.button_width = 64

        self.image = image
        # 设置宽高比
        w_h_ratio = self.pannel_width * 1.0 / self.pannel_height
        print("w_h_ration", w_h_ratio)
        self.image = cv2.resize(self.image, ((int)(self.image.shape[0] * w_h_ratio), self.image.shape[0]))
        # self.image = image

        self.image_label = ImageLabel(self)
        self.image_label.setFixedHeight(self.pannel_height)
        self.image_label.setFixedWidth(self.pannel_width)
        self.image_label.show_image(self.image)

        # button
        self.ok_button = QPushButton(self)
        self.ok_button.setFixedWidth(self.button_width)
        self.ok_button.setFixedHeight(self.button_height)
        self.ok_button.setToolTip("ok")
        self.ok_button.setText("ok")
        self.ok_button.setIcon(QIcon("./icons/ok.png"))
        self.ok_button.clicked.connect(self.on_ok_button)

        self.reselect_button = QPushButton(self)
        self.reselect_button.setFixedHeight(self.button_height)
        self.reselect_button.setFixedWidth(self.button_width)
        self.reselect_button.setText("reset")
        self.reselect_button.setIcon(QIcon("./icons/reset.png"))
        self.reselect_button.setToolTip("cancel")
        self.reselect_button.clicked.connect(self.on_reselect_button)

        # layout
        self.h_layout = QHBoxLayout()
        self.h_layout.addWidget(self.ok_button)
        self.h_layout.addWidget(self.reselect_button)

        self.v_layout = QVBoxLayout()
        self.v_layout.addWidget(self.image_label)
        self.v_layout.addLayout(self.h_layout)

        self.setLayout(self.v_layout)
        self.setFixedWidth(630)
        self.setFixedHeight(590)

        # QShortcut(QKeySequence(self.tr("Ctrl+A")), self, self.image_label.test)

    # normal function
    def get_image(self):
        return self.image

    # 根据左上、左下，右下，右上的顺序排序
    def order_points(self, points):
        # 求中心点的坐标
        center = [0, 0]
        for point in points:
            center[0] += point[0]
            center[1] += point[1]
        center[0] = center[0] / 4
        center[1] = center[1] / 4
        print(center)
        # 根据中心点x坐标，大于为左，小于为右
        left = []
        right = []
        for point in points:
            if point[0] > center[0]:
                right.append(point)
            else:
                left.append(point)
        print("left", left, "right", right)

        # 区分左边坐标的上下，y坐标大于中心坐标为下，否则为上
        bl = []
        tl = []
        for l in left:
            if l[1] > center[1]:
                bl = l
            else:
                tl = l
        # 同理区分右上，右下
        br = []
        tr = []
        for r in right:
            if r[1] > center[1]:
                br = r
            else:
                tr = r

        return [tl, bl, br, tr]

    def mapfromLoal(self, points):
        # 从局部点投影到原图，并且将4个点的顺序，按照左上、左下，右下，右上的顺序排序
        points_origanal = []
        print("in map shape:", self.image.shape)
        print("before largen", points)
        y_ratio = np.float32(self.image.shape[0] / self.image_label.height())
        x_ratio = np.float32(self.image.shape[1] / self.image_label.width())
        for point in points:
            points_origanal.append([point[0] * x_ratio, point[1] * y_ratio])

        order_points = self.order_points(points_origanal)
        print("order", order_points)
        return order_points
        # return points_origanal

    # slot function
    def on_ok_button(self):
        if len(self.image_label.get_points()) != 4:  # 判断是否选取完
            reply = QMessageBox.warning(self,
                                        "提示",
                                        "请选取四个点",
                                        QMessageBox.Ok)
            return

        reply = QMessageBox.warning(self,
                                    "提示",
                                    "你确定截取好了吗",
                                    QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            points = self.image_label.get_points()
            # 单适应变换
            points_origanal = self.mapfromLoal(points)
            src_point = np.float32(points_origanal)
            print("src_point", src_point)
            # 想要变换成图像的大小
            dsize = (self.image.shape[1], self.image.shape[0])
            dst_point = np.float32([[0, 0], [0, dsize[1] - 1], [dsize[0] - 1, dsize[1] - 1], [dsize[0] - 1, 0]])
            print("dst_point", dst_point)
            h, s = cv2.findHomography(src_point, dst_point, cv2.RANSAC, 10)
            self.image = cv2.warpPerspective(self.image, h, dsize, borderMode=cv2.BORDER_REPLICATE)
            cv2.imwrite("warp.jpg", self.image)
            self.ok_signal.emit()
            # self.close()

    def on_reselect_button(self):
        self.image_label.reselect()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("截图")
    window = cropWindow(cv2.imread("test.png"))
    window.show()
    sys.exit(app.exec_())





