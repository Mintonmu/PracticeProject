from PySide2.QtWidgets import QHBoxLayout, QApplication, QListWidget, QTextEdit, QSizePolicy, QListWidgetItem, QWidget, \
    QLineEdit, QMessageBox
from PySide2.QtCore import QSize
from PySide2.QtUiTools import QUiLoader
import sys
import requests

class MainForm():
    def __init__(self, app):
        self.app = app
        self.ui = QUiLoader().load('ui/main.ui')

        self.request_head = []
        self.request_body = []
        self.tab1 = self.ui.tab  # 获取请求头的组件
        self.tab2 = self.ui.tab_2  # 获取请求头的组件
        self.tab3 = self.ui.tab_3  # 获取数据头的组件
        self.tab4 = self.ui.tab_4  # 获取数据头的组件
        self.set_add_request_ui()  # 设置请求头组件

        self.add_request_weiget1()  # 默认添加一项
        self.add_request_weiget2()  # 默认添加一项
        self.set_button_event()  # 设置按钮事件

    def send_request(self):
        try:
            headers = {}
            data = {}
            for idx in range(self.li1.count()):  # 获取listWidget列表数量
                item = self.li1.item(idx)  # 根据下标获得每一项
                pWidget = self.li1.itemWidget(item)  # 转成listitemwidget
                # 获取每一项的布局
                # 从布局中获取每一项的widget
                qLineEdits = [pWidget.layout().itemAt(i).widget() for i in range(pWidget.layout().count())]

                if qLineEdits[0].text() != '':
                    # print('add')
                    headers[qLineEdits[0].text()] = qLineEdits[1].text()
            # print(headers)
            for idx in range(self.li2.count()):  # 获取listWidget列表数量
                item = self.li2.item(idx)  # 根据下标获得每一项
                pWidget = self.li2.itemWidget(item)  # 转成listitemwidget
                # 获取每一项的布局
                # 从布局中获取每一项的widget
                qLineEdits = [pWidget.layout().itemAt(i).widget() for i in range(pWidget.layout().count())]
                if qLineEdits[0].text() != '':
                    data[qLineEdits[0].text()] = qLineEdits[1].text()

            if self.ui.comboBox.currentIndex() == 0:
                # GET
                r = requests.get(self.ui.lineEdit.text(), headers=headers, data=data)

            else:
                # POST
                r = requests.post(self.ui.lineEdit.text(), headers=headers, data=data)
            r.encoding='utf8'
            if r.status_code != 200:
                raise Exception(r.status_code)
            self.ui.textEdit.clear()
            for key in r.headers:
                self.ui.textEdit.append(key + " : " + r.headers[key])

            self.ui.textEdit_2.clear()
            self.ui.textEdit_2.append(r.text)

        except Exception as e:
            QMessageBox.information(None, "错误", str(e))

    def set_data1(self, id):
        if id == 0:
            # 从edittext1读数据
            content = self.textEdit1.toPlainText()
            # 用&分割参数
            sp = content.split('&')
            # 再次分割 获取数据每一项
            self.request_head = [item.split('=') for item in sp]
            # 清除listWidget每一项
            self.li1.clear()
            for item in self.request_head:
                if len(item) == 2:
                    # 只有数据不添加
                    if item[0] != '':
                        self.add_request_weiget1(item[0], item[1])

        else:
            # 从 listview读数据
            stt = ''
            for idx in range(self.li1.count()):  # 获取listWidget列表数量
                item = self.li1.item(idx)  # 根据下标获得每一项
                pWidget = self.li1.itemWidget(item)  # 转成listitemwidget
                # 获取每一项的布局
                # 从布局中获取每一项的widget
                qLineEdits = [pWidget.layout().itemAt(i).widget() for i in range(pWidget.layout().count())]
                # 从请求数据中清除所有项
                self.request_head.clear()
                # 添加请求数据
                self.request_head.append([qLineEdits[0].text(), qLineEdits[1].text()])
                # 拼接请求参数
                stt += qLineEdits[0].text() + '=' + qLineEdits[1].text()
                if qLineEdits[0].text() != '':
                    if idx != self.li1.count() - 1:
                        stt += '&'
            # 设置textEdit数据
            self.textEdit1.setText(stt)

    def set_data2(self, id):
        if id == 0:
            # 从edittext1读数据
            content = self.textEdit2.toPlainText()
            sp = content.split('&')
            self.request_body = [item.split('=') for item in sp]
            self.li2.clear()
            for item in self.request_body:
                if len(item) == 2:
                    if item[0] != '':
                        self.add_request_weiget2(item[0], item[1])

        else:
            # 从 listview读数据
            stt = ''
            for idx in range(self.li2.count()):  # 获取listWidget列表数量
                item = self.li2.item(idx)  # 根据下标获得每一项
                pWidget = self.li2.itemWidget(item)  # 转成listitemwidget
                # 获取每一项的布局
                # 从布局中获取每一项的widget
                qLineEdits = [pWidget.layout().itemAt(i).widget() for i in range(pWidget.layout().count())]
                self.request_body.clear()
                self.request_body.append([qLineEdits[0].text(), qLineEdits[1].text()])
                if qLineEdits[0].text() != '':
                    stt += qLineEdits[0].text() + '=' + qLineEdits[1].text()
                if idx != self.li2.count() - 1:
                    stt += '&'
            self.textEdit2.setText(stt)

    def set_button_event(self):
        self.ui.add1.clicked.connect(self.add_request_weiget1)
        self.ui.del1.clicked.connect(self.del_request_weiget1)
        self.ui.add2.clicked.connect(self.add_request_weiget2)
        self.ui.del2.clicked.connect(self.del_request_weiget2)

        self.ui.tabWidget.tabBarClicked.connect(self.set_data1)
        self.ui.tabWidget_2.tabBarClicked.connect(self.set_data2)

        self.ui.send_req_btn.clicked.connect(self.send_request)

    # 删除请求list项
    def del_request_weiget1(self):
        self.li1.takeItem(self.li1.row(self.li1.currentItem()))

    # 删除请求list项
    def del_request_weiget2(self):
        self.li2.takeItem(self.li2.row(self.li2.currentItem()))  # 正确的从list中删除item的方式

    # 添加请求项
    def add_request_weiget1(self, t1='', t2=''):
        item = QListWidgetItem()

        item.setSizeHint(QSize(10, 40))
        self.li1.addItem(item)

        w = QWidget()
        layout = QHBoxLayout()

        e1 = QLineEdit(w)
        e1.setText(t1)

        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(10)
        sizePolicy2.setVerticalStretch(0)
        # sizePolicy1.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        e1.setSizePolicy(sizePolicy2)

        e2 = QLineEdit(w)
        e2.setText(t2)

        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(10)
        sizePolicy3.setVerticalStretch(0)
        # sizePolicy1.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        e2.setSizePolicy(sizePolicy3)

        layout.addWidget(e1)
        layout.addWidget(e2)

        w.setLayout(layout)
        self.li1.setItemWidget(item, w)

    # 添加请求项
    def add_request_weiget2(self, t1='', t2=''):
        item = QListWidgetItem()

        item.setSizeHint(QSize(10, 40))
        self.li2.addItem(item)

        w = QWidget()
        layout = QHBoxLayout()

        e1 = QLineEdit(w)
        e1.setText(t1)
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(10)
        sizePolicy2.setVerticalStretch(0)
        # sizePolicy1.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        e1.setSizePolicy(sizePolicy2)

        e2 = QLineEdit(w)
        e2.setText(t2)
        sizePolicy3 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(10)
        sizePolicy3.setVerticalStretch(0)
        # sizePolicy1.setHeightForWidth(self.comboBox.sizePolicy().hasHeightForWidth())
        e2.setSizePolicy(sizePolicy3)

        layout.addWidget(e1)
        layout.addWidget(e2)

        w.setLayout(layout)
        self.li2.setItemWidget(item, w)

    def set_add_request_ui(self):
        self.li1 = QListWidget()
        self.layout1 = QHBoxLayout()
        self.layout1.setContentsMargins(0, 0, 0, 0)
        self.layout1.addWidget(self.li1)
        self.tab1.setLayout(self.layout1)

        self.textEdit1 = QTextEdit()
        self.layout2 = QHBoxLayout()
        self.layout2.setContentsMargins(0, 0, 0, 0)
        self.layout2.addWidget(self.textEdit1)
        self.tab2.setLayout(self.layout2)

        self.li2 = QListWidget()
        self.layout3 = QHBoxLayout()
        self.layout3.setContentsMargins(0, 0, 0, 0)
        self.layout3.addWidget(self.li2)
        self.tab3.setLayout(self.layout3)

        self.textEdit2 = QTextEdit()
        self.layout4 = QHBoxLayout()
        self.layout4.setContentsMargins(0, 0, 0, 0)
        self.layout4.addWidget(self.textEdit2)
        self.tab4.setLayout(self.layout4)


if __name__ == '__main__':
    app = QApplication()

    form = MainForm(app)
    form.ui.show()

    sys.exit(app.exec_())
