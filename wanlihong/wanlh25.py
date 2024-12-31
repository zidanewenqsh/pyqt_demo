
import sys
import cv2
import numpy as np
import face_recognition
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from Ui_wanlihong25 import Ui_MainWindow  # 导入编译后的 UI 文件类


class FaceLikelihoodTool(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 初始化变量
        self.image1 = None
        self.image2 = None

        # 绑定按钮信号和槽
        self.button_upload_image1.clicked.connect(self.upload_image1)
        self.button_upload_image2.clicked.connect(self.upload_image2)
        self.button_calculate_likelihood.clicked.connect(self.calculate_likelihood)

    def upload_image1(self):
        """上传检材图像"""
        file_path, _ = QFileDialog.getOpenFileName(self, "Upload Image 1", "", "Image Files (*.png *.jpg *.bmp)")
        if file_path:
            self.image1 = face_recognition.load_image_file(file_path)
            self.display_image(cv2.imread(file_path), self.label_image1)

    def upload_image2(self):
        """上传样本图像"""
        file_path, _ = QFileDialog.getOpenFileName(self, "Upload Image 2", "", "Image Files (*.png *.jpg *.bmp)")
        if file_path:
            self.image2 = face_recognition.load_image_file(file_path)
            self.display_image(cv2.imread(file_path), self.label_image2)

    def display_image(self, image, label):
        """显示图像在 QLabel 中"""
        if image is not None:
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            height, width, channel = image_rgb.shape
            bytes_per_line = channel * width
            q_image = QImage(image_rgb.data, width, height, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            label.setPixmap(pixmap.scaled(label.width(), label.height(), Qt.KeepAspectRatio))

    def calculate_likelihood(self):
        """计算人脸似然率"""
        if self.image1 is None or self.image2 is None:
            QMessageBox.warning(self, "Error", "Please upload both images first!")
            return

        # 提取人脸特征向量
        encodings1 = face_recognition.face_encodings(self.image1)
        encodings2 = face_recognition.face_encodings(self.image2)

        if len(encodings1) == 0 or len(encodings2) == 0:
            QMessageBox.warning(self, "Error", "Failed to detect faces in one or both images!")
            return

        # 计算欧氏距离
        distance = np.linalg.norm(encodings1[0] - encodings2[0])
        likelihood = max(0, 1 - distance / 0.6)  # 转换为似然率，假设阈值为 0.6

        # 显示似然率
        self.label_likelihood_result.setText(f"Likelihood: {likelihood * 100:.2f}%")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FaceLikelihoodTool()
    window.show()
    sys.exit(app.exec_())