from PyQt5 import sip, QtGui
from PyQt5.QtCore import QDateTime, Qt
from PyQt5.QtGui import QScreen, QGuiApplication
from PyQt5.QtWidgets import *

import sys


class Demo(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("hidden")
        self.x, self.y = 0, 0
        screenRect = QApplication.desktop().screenGeometry()
        self.w, self.h = screenRect.width(), screenRect.height()

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        print(event)

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)

    de = Demo()

    de.show()

    #
    screen = QGuiApplication.primaryScreen()

    # 文件名
    filePathName = 'full-'
    filePathName += QDateTime.currentDateTime().toString("yyyy-MM-dd hh-mm-ss-zzz")
    filePathName += '.jpg'

    # 获取根窗口
    this_windows = QApplication.desktop().winId()

    x, y = 0, 0
    w, h = 100, 100
    screen.grabWindow(this_windows, x, y, w, h).save(filePathName, 'jpg')

    QLabel()
    QButton()

    sys.exit(app.exec_())

