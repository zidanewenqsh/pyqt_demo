import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from Ui_wanlihong24 import Ui_MainWindow  # 导入编译后的 UI 文件类


class FaceSimilarityTool(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 初始化变量
        self.image1 = None
        self.image2 = None
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        # 绑定按钮信号和槽
        self.button_upload_image1.clicked.connect(self.upload_image1)
        self.button_upload_image2.clicked.connect(self.upload_image2)
        self.button_calculate_similarity.clicked.connect(self.calculate_similarity)

    def upload_image1(self):
        """上传检材图像"""
        file_path, _ = QFileDialog.getOpenFileName(self, "Upload Image 1", "", "Image Files (*.png *.jpg *.bmp)")
        if file_path:
            self.image1 = cv2.imread(file_path)
            self.display_image(self.image1, self.label_image1)

    def upload_image2(self):
        """上传样本图像"""
        file_path, _ = QFileDialog.getOpenFileName(self, "Upload Image 2", "", "Image Files (*.png *.jpg *.bmp)")
        if file_path:
            self.image2 = cv2.imread(file_path)
            self.display_image(self.image2, self.label_image2)

    def display_image(self, image, label):
        """显示图像在 QLabel 中"""
        if image is not None:
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            height, width, channel = image_rgb.shape
            bytes_per_line = channel * width
            q_image = QImage(image_rgb.data, width, height, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            label.setPixmap(pixmap.scaled(label.width(), label.height(), Qt.KeepAspectRatio))

    def calculate_similarity(self):
        """计算两张人脸的相似度"""
        if self.image1 is None or self.image2 is None:
            QMessageBox.warning(self, "Error", "Please upload both images first!")
            return

        # 检测人脸
        face1 = self.detect_face(self.image1)
        face2 = self.detect_face(self.image2)

        if face1 is None or face2 is None:
            QMessageBox.warning(self, "Error", "Failed to detect faces in one or both images!")
            return

        # 计算相似度（使用直方图相似性）
        similarity = self.compare_faces(face1, face2)
        self.label_similarity_result.setText(f"Similarity: {similarity:.2f}%")

    def detect_face(self, image):
        """检测人脸并返回裁剪的标准化人脸区域"""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        if len(faces) > 0:
            x, y, w, h = max(faces, key=lambda rect: rect[2] * rect[3])  # 选择最大的人脸区域
            face = image[y:y+h, x:x+w]
            return cv2.resize(face, (128, 128))  # 标准化尺寸为 128x128
        return None

    def compare_faces(self, face1, face2):
        """计算两张人脸的相似度"""
        # 转换为灰度图
        gray1 = cv2.cvtColor(face1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(face2, cv2.COLOR_BGR2GRAY)

        # 计算直方图
        hist1 = cv2.calcHist([gray1], [0], None, [256], [0, 256])
        hist2 = cv2.calcHist([gray2], [0], None, [256], [0, 256])

        # 归一化直方图
        hist1 = cv2.normalize(hist1, hist1).flatten()
        hist2 = cv2.normalize(hist2, hist2).flatten()

        # 计算相似度（巴氏距离）
        score = cv2.compareHist(hist1, hist2, cv2.HISTCMP_BHATTACHARYYA)
        similarity = (1 - score) * 100  # 转换为百分比相似度

        return similarity


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FaceSimilarityTool()
    window.show()
    sys.exit(app.exec_())
