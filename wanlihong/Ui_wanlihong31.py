# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\WinProjects\pyqt_demo\wanlihong31.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 700)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.listwidget_order = QtWidgets.QListWidget(self.centralwidget)
        self.listwidget_order.setGeometry(QtCore.QRect(50, 50, 400, 500))
        self.listwidget_order.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)
        self.listwidget_order.setObjectName("listwidget_order")
        self.button_move_up = QtWidgets.QPushButton(self.centralwidget)
        self.button_move_up.setGeometry(QtCore.QRect(470, 200, 150, 30))
        self.button_move_up.setObjectName("button_move_up")
        self.button_move_down = QtWidgets.QPushButton(self.centralwidget)
        self.button_move_down.setGeometry(QtCore.QRect(470, 250, 150, 30))
        self.button_move_down.setObjectName("button_move_down")
        self.button_export_word = QtWidgets.QPushButton(self.centralwidget)
        self.button_export_word.setGeometry(QtCore.QRect(470, 400, 150, 30))
        self.button_export_word.setObjectName("button_export_word")
        self.button_load_template = QtWidgets.QPushButton(self.centralwidget)
        self.button_load_template.setGeometry(QtCore.QRect(470, 450, 150, 30))
        self.button_load_template.setObjectName("button_load_template")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "文书生成工具"))
        self.button_move_up.setText(_translate("MainWindow", "Move Up"))
        self.button_move_down.setText(_translate("MainWindow", "Move Down"))
        self.button_export_word.setText(_translate("MainWindow", "Export Word"))
        self.button_load_template.setText(_translate("MainWindow", "Load Template"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
