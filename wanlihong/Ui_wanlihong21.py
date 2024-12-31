# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\WinProjects\pyqt_demo\wanlihong21.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 650)
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
        self.button_crop_image1 = QtWidgets.QPushButton(self.centralwidget)
        self.button_crop_image1.setGeometry(QtCore.QRect(50, 470, 150, 30))
        self.button_crop_image1.setObjectName("button_crop_image1")
        self.button_crop_image2 = QtWidgets.QPushButton(self.centralwidget)
        self.button_crop_image2.setGeometry(QtCore.QRect(250, 470, 150, 30))
        self.button_crop_image2.setObjectName("button_crop_image2")
        self.button_stitch = QtWidgets.QPushButton(self.centralwidget)
        self.button_stitch.setGeometry(QtCore.QRect(450, 470, 150, 30))
        self.button_stitch.setObjectName("button_stitch")
        self.button_switch_position = QtWidgets.QPushButton(self.centralwidget)
        self.button_switch_position.setGeometry(QtCore.QRect(650, 470, 150, 30))
        self.button_switch_position.setObjectName("button_switch_position")
        self.button_save_stitched = QtWidgets.QPushButton(self.centralwidget)
        self.button_save_stitched.setGeometry(QtCore.QRect(850, 470, 150, 30))
        self.button_save_stitched.setObjectName("button_save_stitched")
        self.label_image_stitched = QtWidgets.QLabel(self.centralwidget)
        self.label_image_stitched.setGeometry(QtCore.QRect(50, 520, 850, 100))
        self.label_image_stitched.setAlignment(QtCore.Qt.AlignCenter)
        self.label_image_stitched.setFrameShape(QtWidgets.QFrame.Box)
        self.label_image_stitched.setObjectName("label_image_stitched")
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
        MainWindow.setWindowTitle(_translate("MainWindow", "Image Stitching Tool"))
        self.button_upload_image1.setText(_translate("MainWindow", "Upload Image 1"))
        self.button_upload_image2.setText(_translate("MainWindow", "Upload Image 2"))
        self.label_image1.setText(_translate("MainWindow", "Image 1"))
        self.label_image2.setText(_translate("MainWindow", "Image 2"))
        self.button_crop_image1.setText(_translate("MainWindow", "Crop Image 1"))
        self.button_crop_image2.setText(_translate("MainWindow", "Crop Image 2"))
        self.button_stitch.setText(_translate("MainWindow", "Stitch Images"))
        self.button_switch_position.setText(_translate("MainWindow", "Switch Position"))
        self.button_save_stitched.setText(_translate("MainWindow", "Save Stitched Image"))
        self.label_image_stitched.setText(_translate("MainWindow", "Stitched Image"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
