# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\WinProjects\pyqt_demo\wanlihong24.ui'
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
        self.button_upload_image2.setGeometry(QtCore.QRect(250, 10, 150, 30))
        self.button_upload_image2.setObjectName("button_upload_image2")
        self.label_image1 = QtWidgets.QLabel(self.centralwidget)
        self.label_image1.setGeometry(QtCore.QRect(50, 50, 300, 400))
        self.label_image1.setAlignment(QtCore.Qt.AlignCenter)
        self.label_image1.setFrameShape(QtWidgets.QFrame.Box)
        self.label_image1.setObjectName("label_image1")
        self.label_image2 = QtWidgets.QLabel(self.centralwidget)
        self.label_image2.setGeometry(QtCore.QRect(400, 50, 300, 400))
        self.label_image2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_image2.setFrameShape(QtWidgets.QFrame.Box)
        self.label_image2.setObjectName("label_image2")
        self.button_calculate_similarity = QtWidgets.QPushButton(self.centralwidget)
        self.button_calculate_similarity.setGeometry(QtCore.QRect(250, 470, 300, 30))
        self.button_calculate_similarity.setObjectName("button_calculate_similarity")
        self.label_similarity_result = QtWidgets.QLabel(self.centralwidget)
        self.label_similarity_result.setGeometry(QtCore.QRect(250, 520, 300, 30))
        self.label_similarity_result.setAlignment(QtCore.Qt.AlignCenter)
        self.label_similarity_result.setFrameShape(QtWidgets.QFrame.Panel)
        self.label_similarity_result.setObjectName("label_similarity_result")
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
        MainWindow.setWindowTitle(_translate("MainWindow", "Face Similarity Tool"))
        self.button_upload_image1.setText(_translate("MainWindow", "Upload Image 1"))
        self.button_upload_image2.setText(_translate("MainWindow", "Upload Image 2"))
        self.label_image1.setText(_translate("MainWindow", "Image 1"))
        self.label_image2.setText(_translate("MainWindow", "Image 2"))
        self.button_calculate_similarity.setText(_translate("MainWindow", "Calculate Similarity"))
        self.label_similarity_result.setText(_translate("MainWindow", "Similarity: N/A"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())