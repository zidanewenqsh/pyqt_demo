import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from Ui_wanlihong17 import Ui_MainWindow  # 导入编译生成的 UI 文件类

class ImageOverlapTool(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 初始化变量
        self.image1 = None
        self.image2 = None
        self.alpha = 0.5  # 初始透明度值

        # 绑定按钮信号和槽
        self.button_upload_image1.clicked.connect(self.upload_image1)
        self.button_upload_image2.clicked.connect(self.upload_image2)
        self.slider_opacity.valueChanged.connect(self.update_opacity)
        self.button_reset.clicked.connect(self.reset_images)
        self.button_save_overlap.clicked.connect(self.save_overlap)

    def upload_image1(self):
        """上传检材图像"""
        file_path, _ = QFileDialog.getOpenFileName(self, "Upload Image 1", "", "Image Files (*.png *.jpg *.bmp)")
        if file_path:
            self.image1 = cv2.imread(file_path)
            self.display_overlap()

    def upload_image2(self):
        """上传样本图像"""
        file_path, _ = QFileDialog.getOpenFileName(self, "Upload Image 2", "", "Image Files (*.png *.jpg *.bmp)")
        if file_path:
            self.image2 = cv2.imread(file_path)
            self.display_overlap()

    def display_overlap(self):
        """显示图像重叠结果"""
        if self.image1 is None or self.image2 is None:
            return

        # 确保两张图像尺寸一致
        if self.image1.shape != self.image2.shape:
            QMessageBox.warning(self, "Error", "Images must have the same dimensions!")
            return

        # 创建重叠图像
        overlap_image = cv2.addWeighted(self.image1, self.alpha, self.image2, 1 - self.alpha, 0)
        self.display_image(overlap_image)

    def display_image(self, image):
        """显示图像在 QLabel 中"""
        if image is not None:
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            height, width, channel = image_rgb.shape
            bytes_per_line = channel * width
            q_image = QImage(image_rgb.data, width, height, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            self.label_image_overlap.setPixmap(pixmap.scaled(self.label_image_overlap.width(),
                                                             self.label_image_overlap.height(),
                                                             Qt.KeepAspectRatio))

    def update_opacity(self):
        """更新透明度值"""
        self.alpha = self.slider_opacity.value() / 100
        self.display_overlap()

    def reset_images(self):
        """重置图像和控件"""
        self.image1 = None
        self.image2 = None
        self.alpha = 0.5
        self.slider_opacity.setValue(50)
        self.label_image_overlap.clear()
        self.label_image_overlap.setText("Overlap Display")

    def save_overlap(self):
        """保存重叠图像"""
        if self.image1 is None or self.image2 is None:
            QMessageBox.warning(self, "Error", "Please upload both images first!")
            return

        # 生成重叠图像
        overlap_image = cv2.addWeighted(self.image1, self.alpha, self.image2, 1 - self.alpha, 0)

        # 保存图像
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Overlap", "", "Image Files (*.png *.jpg *.bmp)")
        if file_path:
            cv2.imwrite(file_path, overlap_image)
            QMessageBox.information(self, "Success", "Overlap image saved successfully.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageOverlapTool()
    window.show()
    sys.exit(app.exec_())
