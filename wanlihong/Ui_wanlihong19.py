# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\WinProjects\pyqt_demo\wanlihong19.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.button_upload_image1 = QtWidgets.QPushButton(self.centralwidget)
        self.button_upload_image1.setGeometry(QtCore.QRect(50, 10, 150, 30))
        self.button_upload_image1.setObjectName("button_upload_image1")
        self.button_upload_image2 = QtWidgets.QPushButton(self.centralwidget)
        self.button_upload_image2.setGeometry(QtCore.QRect(250, 10, 150, 30))
        self.button_upload_image2.setObjectName("button_upload_image2")
        self.label_image1 = QtWidgets.QLabel(self.centralwidget)
        self.label_image1.setGeometry(QtCore.QRect(50, 50, 400, 400))
        self.label_image1.setAlignment(QtCore.Qt.AlignCenter)
        self.label_image1.setFrameShape(QtWidgets.QFrame.Box)
        self.label_image1.setObjectName("label_image1")
        self.label_image2 = QtWidgets.QLabel(self.centralwidget)
        self.label_image2.setGeometry(QtCore.QRect(500, 50, 400, 400))
        self.label_image2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_image2.setFrameShape(QtWidgets.QFrame.Box)
        self.label_image2.setObjectName("label_image2")
        self.button_add_point = QtWidgets.QPushButton(self.centralwidget)
        self.button_add_point.setGeometry(QtCore.QRect(50, 470, 150, 30))
        self.button_add_point.setObjectName("button_add_point")
        self.button_add_line = QtWidgets.QPushButton(self.centralwidget)
        self.button_add_line.setGeometry(QtCore.QRect(250, 470, 150, 30))
        self.button_add_line.setObjectName("button_add_line")
        self.button_undo = QtWidgets.QPushButton(self.centralwidget)
        self.button_undo.setGeometry(QtCore.QRect(450, 470, 150, 30))
        self.button_undo.setObjectName("button_undo")
        self.button_screenshot = QtWidgets.QPushButton(self.centralwidget)
        self.button_screenshot.setGeometry(QtCore.QRect(650, 470, 150, 30))
        self.button_screenshot.setObjectName("button_screenshot")
        self.button_save_log = QtWidgets.QPushButton(self.centralwidget)
        self.button_save_log.setGeometry(QtCore.QRect(850, 470, 150, 30))
        self.button_save_log.setObjectName("button_save_log")
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
        MainWindow.setWindowTitle(_translate("MainWindow", "Image Comparison Tool"))
        self.button_upload_image1.setText(_translate("MainWindow", "Upload Image 1"))
        self.button_upload_image2.setText(_translate("MainWindow", "Upload Image 2"))
        self.label_image1.setText(_translate("MainWindow", "Image 1"))
        self.label_image2.setText(_translate("MainWindow", "Image 2"))
        self.button_add_point.setText(_translate("MainWindow", "Add Point"))
        self.button_add_line.setText(_translate("MainWindow", "Add Line"))
        self.button_undo.setText(_translate("MainWindow", "Undo"))
        self.button_screenshot.setText(_translate("MainWindow", "Screenshot"))
        self.button_save_log.setText(_translate("MainWindow", "Save Log"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
