import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from Ui_wanlihong7 import Ui_MainWindow
class ImageAlignment(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 初始化属性
        self.image1 = None  # 图像 1 数据
        self.image2 = None  # 图像 2 数据
        self.manual_points_1 = []  # 图像 1 手动对齐点
        self.manual_points_2 = []  # 图像 2 手动对齐点

        # 信号与槽
        self.button_load_image_1.clicked.connect(lambda: self.load_image(1))
        self.button_load_image_2.clicked.connect(lambda: self.load_image(2))
        self.button_auto_align.clicked.connect(self.auto_align)
        self.button_manual_align.clicked.connect(self.enable_manual_alignment)
        self.button_clear_points.clicked.connect(self.clear_manual_points)

        # 初始化手动对齐模式
        self.image_label_1.mousePressEvent = self.mark_point_image1
        self.image_label_2.mousePressEvent = self.mark_point_image2

    def load_image(self, image_number):
        """加载图像"""
        file_path, _ = QFileDialog.getOpenFileName(self, f"Load Image {image_number}", "", "Image Files (*.png *.jpg *.bmp)")
        if file_path:
            image = cv2.imread(file_path)
            if image_number == 1:
                self.image1 = image
                self.show_image(self.image1, self.image_label_1)
                QMessageBox.information(self, "Image 1 Loaded", "Image 1 successfully loaded.")
            elif image_number == 2:
                self.image2 = image
                self.show_image(self.image2, self.image_label_2)
                QMessageBox.information(self, "Image 2 Loaded", "Image 2 successfully loaded.")
        else:
            QMessageBox.warning(self, "No Image Selected", f"Please select an image file for Image {image_number}.")

    def auto_align(self):
        """自动对齐图像"""
        if self.image1 is None or self.image2 is None:
            QMessageBox.warning(self, "Error", "Please load both images before alignment.")
            return

        # 使用 ORB 提取特征并匹配
        orb = cv2.ORB_create()
        kp1, des1 = orb.detectAndCompute(self.image1, None)
        kp2, des2 = orb.detectAndCompute(self.image2, None)
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(des1, des2)

        # 选取匹配点
        points1 = np.float32([kp1[m.queryIdx].pt for m in matches])
        points2 = np.float32([kp2[m.trainIdx].pt for m in matches])

        # 计算仿射变换
        matrix, _ = cv2.estimateAffinePartial2D(points2, points1)
        aligned_image = cv2.warpAffine(self.image2, matrix, (self.image1.shape[1], self.image1.shape[0]))
        self.show_image(aligned_image, self.image_label_2)

    def enable_manual_alignment(self):
        """启用手动对齐模式"""
        QMessageBox.information(self, "Manual Alignment", "Click corresponding points on both images.")

    def mark_point_image1(self, event):
        """在图像 1 上标记点"""
        x = event.pos().x()
        y = event.pos().y()
        self.manual_points_1.append((x, y))
        self.log_window.append(f"Image 1 Point: ({x}, {y})")

    def mark_point_image2(self, event):
        """在图像 2 上标记点"""
        x = event.pos().x()
        y = event.pos().y()
        self.manual_points_2.append((x, y))
        self.log_window.append(f"Image 2 Point: ({x}, {y})")

    def clear_manual_points(self):
        """清除手动标记的点"""
        self.manual_points_1 = []
        self.manual_points_2 = []
        self.log_window.append("Cleared manual points.")

    def show_image(self, image, label):
        """在 QLabel 中显示图像"""
        if image is None:
            QMessageBox.warning(self, "Error", "No image to display.")
            return

        if len(image.shape) == 2:  # Grayscale image
            qimage = QImage(image.data, image.shape[1], image.shape[0], image.strides[0], QImage.Format_Grayscale8)
        else:  # Color image
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            qimage = QImage(rgb_image.data, rgb_image.shape[1], rgb_image.shape[0], rgb_image.strides[0], QImage.Format_RGB888)

        pixmap = QPixmap.fromImage(qimage)
        label.setPixmap(pixmap.scaled(label.width(), label.height(), Qt.KeepAspectRatio))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageAlignment()
    window.show()
    sys.exit(app.exec_())
