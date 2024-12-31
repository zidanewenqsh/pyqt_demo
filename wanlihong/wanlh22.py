import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from Ui_wanlihong22 import Ui_MainWindow  # 导入编译后的 UI 文件类


class ImageStitchingTool(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 初始化变量
        self.image1 = None
        self.image2 = None
        self.crop1 = None
        self.crop2 = None
        self.stitch_position = 0.5  # 默认拼接位置为中间

        # 绑定按钮信号和槽
        self.button_upload_image1.clicked.connect(self.upload_image1)
        self.button_upload_image2.clicked.connect(self.upload_image2)
        self.slider_stitch_position.valueChanged.connect(self.update_stitch_position)
        self.button_save_screenshot.clicked.connect(self.save_screenshot)

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

    def update_stitch_position(self):
        """更新拼接位置"""
        if self.image1 is not None and self.image2 is not None:
            position_ratio = self.slider_stitch_position.value() / 100
            self.stitch_position = position_ratio
            stitched_image = self.stitch_images()
            self.display_image(stitched_image, self.label_image_stitched)

    def stitch_images(self):
        """根据拼接位置拼接图像"""
        if self.image1 is not None and self.image2 is not None:
            height1, width1, _ = self.image1.shape
            height2, width2, _ = self.image2.shape

            # 确保高度一致
            height = min(height1, height2)
            image1_resized = cv2.resize(self.image1, (width1, height))
            image2_resized = cv2.resize(self.image2, (width2, height))

            # 计算拼接点
            split_width = int(self.stitch_position * width1)
            stitched_image = np.hstack((image1_resized[:, :split_width], image2_resized[:, split_width:]))

            return stitched_image
        return None

    def save_screenshot(self):
        """保存拼接结果截图"""
        stitched_image = self.stitch_images()
        if stitched_image is not None:
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
