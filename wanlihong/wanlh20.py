import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from Ui_wanlihong20 import Ui_MainWindow  # 导入编译后的 UI 文件类


class ImageStitchingTool(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 初始化变量
        self.image1 = None
        self.image2 = None
        self.crop1 = None
        self.crop2 = None

        # 绑定按钮信号和槽
        self.button_upload_image1.clicked.connect(self.upload_image1)
        self.button_upload_image2.clicked.connect(self.upload_image2)
        self.button_crop_image1.clicked.connect(self.crop_image1)
        self.button_crop_image2.clicked.connect(self.crop_image2)
        self.button_stitch.clicked.connect(self.stitch_images)
        self.button_save_stitched.clicked.connect(self.save_stitched_image)

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

    def crop_image1(self):
        """裁剪检材图像"""
        if self.image1 is not None:
            x, y, w, h = 50, 50, 200, 200  # 假设固定裁剪区域
            self.crop1 = self.image1[y:y+h, x:x+w]
            self.display_image(self.crop1, self.label_image1)
        else:
            QMessageBox.warning(self, "Error", "Please upload Image 1 first!")

    def crop_image2(self):
        """裁剪样本图像"""
        if self.image2 is not None:
            x, y, w, h = 50, 50, 200, 200  # 假设固定裁剪区域
            self.crop2 = self.image2[y:y+h, x:x+w]
            self.display_image(self.crop2, self.label_image2)
        else:
            QMessageBox.warning(self, "Error", "Please upload Image 2 first!")

    def stitch_images(self):
        """拼接两张图像"""
        if self.crop1 is not None and self.crop2 is not None:
            stitched_image = np.hstack((self.crop1, self.crop2))
            self.display_image(stitched_image, self.label_image_stitched)
        else:
            QMessageBox.warning(self, "Error", "Please crop both images first!")

    def save_stitched_image(self):
        """保存拼接图像"""
        if self.crop1 is not None and self.crop2 is not None:
            stitched_image = np.hstack((self.crop1, self.crop2))
            file_path, _ = QFileDialog.getSaveFileName(self, "Save Stitched Image", "", "Image Files (*.png *.jpg *.bmp)")
            if file_path:
                cv2.imwrite(file_path, stitched_image)
                QMessageBox.information(self, "Success", "Stitched image saved successfully!")
        else:
            QMessageBox.warning(self, "Error", "No stitched image to save!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageStitchingTool()
    window.show()
    sys.exit(app.exec_())
