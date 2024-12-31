# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\WinProjects\pyqt_demo\wanlihong17.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.button_upload_image1 = QtWidgets.QPushButton(self.centralwidget)
        self.button_upload_image1.setGeometry(QtCore.QRect(50, 10, 150, 30))
        self.button_upload_image1.setObjectName("button_upload_image1")
        self.button_upload_image2 = QtWidgets.QPushButton(self.centralwidget)
        self.button_upload_image2.setGeometry(QtCore.QRect(220, 10, 150, 30))
        self.button_upload_image2.setObjectName("button_upload_image2")
        self.slider_opacity = QtWidgets.QSlider(self.centralwidget)
        self.slider_opacity.setGeometry(QtCore.QRect(400, 10, 300, 30))
        self.slider_opacity.setOrientation(QtCore.Qt.Horizontal)
        self.slider_opacity.setMinimum(0)
        self.slider_opacity.setMaximum(100)
        self.slider_opacity.setProperty("value", 50)
        self.slider_opacity.setObjectName("slider_opacity")
        self.label_image_overlap = QtWidgets.QLabel(self.centralwidget)
        self.label_image_overlap.setGeometry(QtCore.QRect(50, 50, 700, 400))
        self.label_image_overlap.setAlignment(QtCore.Qt.AlignCenter)
        self.label_image_overlap.setFrameShape(QtWidgets.QFrame.Box)
        self.label_image_overlap.setObjectName("label_image_overlap")
        self.button_reset = QtWidgets.QPushButton(self.centralwidget)
        self.button_reset.setGeometry(QtCore.QRect(50, 470, 150, 30))
        self.button_reset.setObjectName("button_reset")
        self.button_save_overlap = QtWidgets.QPushButton(self.centralwidget)
        self.button_save_overlap.setGeometry(QtCore.QRect(220, 470, 150, 30))
        self.button_save_overlap.setObjectName("button_save_overlap")
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
        MainWindow.setWindowTitle(_translate("MainWindow", "Image Overlap Tool"))
        self.button_upload_image1.setText(_translate("MainWindow", "Upload Image 1"))
        self.button_upload_image2.setText(_translate("MainWindow", "Upload Image 2"))
        self.label_image_overlap.setText(_translate("MainWindow", "Overlap Display"))
        self.button_reset.setText(_translate("MainWindow", "Reset"))
        self.button_save_overlap.setText(_translate("MainWindow", "Save Overlap"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())