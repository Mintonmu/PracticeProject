import sys

from PySide2 import QtGui
from PySide2.QtCore import *
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWebEngineWidgets import QWebEngineView
from PySide2.QtWidgets import *

if __name__ == '__main__':
    app = QApplication(sys.argv)

    ui = QUiLoader().load('res/chart.ui')

    def loadFinished():
        def onLoadFinished(value):
            ui.webEngineView.page().runJavaScript("setValue({})".format(value))

        ui.horizontalScrollBar.setRange(0, 100)
        ui.horizontalScrollBar.valueChanged.connect(onLoadFinished)


    ui.webEngineView.loadFinished.connect(loadFinished)

    ui.show()
    sys.exit(app.exec_())
