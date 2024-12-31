from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QFileDialog, QMessageBox
import cv2
from Ui_wanlihong1 import Ui_MainWindow  # 假设 Ui_MainWindow 已保存为 ui_mainwindow.py

class MainWindowExtended(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # 调用父类的 setupUi 初始化界面

        # 初始化图像变量
        self.image1 = None
        self.image2 = None

        # 信号与槽连接
        self.button_load_image1.clicked.connect(self.load_image1)
        self.button_load_image2.clicked.connect(self.load_image2)
        self.button_analyze.clicked.connect(self.analyze_similarity)

    def load_image1(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Load Image 1", "", "Image Files (*.png *.jpg *.bmp)")
        if file_path:
            pixmap = QPixmap(file_path)
            self.label_image1.setPixmap(pixmap.scaled(self.label_image1.size(), QtCore.Qt.KeepAspectRatio))
            self.image1 = cv2.imread(file_path)
            QMessageBox.information(self, "Image 1 Loaded", "Image 1 has been successfully loaded.")

    def load_image2(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Load Image 2", "", "Image Files (*.png *.jpg *.bmp)")
        if file_path:
            pixmap = QPixmap(file_path)
            self.label_image2.setPixmap(pixmap.scaled(self.label_image2.size(), QtCore.Qt.KeepAspectRatio))
            self.image2 = cv2.imread(file_path)
            QMessageBox.information(self, "Image 2 Loaded", "Image 2 has been successfully loaded.")

    def analyze_similarity(self):
        if self.image1 is None or self.image2 is None:
            QMessageBox.warning(self, "Error", "Please load both images before analyzing similarity.")
            return

        # 示例：使用 ORB 进行特征匹配
        orb = cv2.ORB_create()
        kp1, des1 = orb.detectAndCompute(self.image1, None)
        kp2, des2 = orb.detectAndCompute(self.image2, None)

        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(des1, des2)
        similarity_score = len(matches)

        self.label_result.setText(f"Result: Similarity = {similarity_score}")
        QMessageBox.information(self, "Analysis Complete", f"Similarity score: {similarity_score}")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindowExtended()
    window.show()
    sys.exit(app.exec_())
