import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from Ui_wanlihong23 import Ui_MainWindow  # 导入编译后的 UI 文件类


class ImageStitchingTool(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 初始化变量
        self.image1 = None
        self.image2 = None
        self.logs = []  # 记录拼接检验过程日志

        # 绑定按钮信号和槽
        self.button_upload_image1.clicked.connect(self.upload_image1)
        self.button_upload_image2.clicked.connect(self.upload_image2)
        self.slider_stitch_position.valueChanged.connect(self.update_stitch_position)

    def upload_image1(self):
        """上传检材图像"""
        file_path, _ = QFileDialog.getOpenFileName(self, "Upload Image 1", "", "Image Files (*.png *.jpg *.bmp)")
        if file_path:
            self.image1 = cv2.imread(file_path)
            self.display_image(self.image1, self.label_image1)
            self.logs.append(f"Image 1 uploaded: {file_path}")

    def upload_image2(self):
        """上传样本图像"""
        file_path, _ = QFileDialog.getOpenFileName(self, "Upload Image 2", "", "Image Files (*.png *.jpg *.bmp)")
        if file_path:
            self.image2 = cv2.imread(file_path)
            self.display_image(self.image2, self.label_image2)
            self.logs.append(f"Image 2 uploaded: {file_path}")

    def display_image(self, image, label):
        """显示图像在 QLabel 中"""
        if image is not None:
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            height, width, channel = image_rgb.shape
            bytes_per_line = channel * width
            q_image = QImage(image_rgb.data, width, height, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            label.setPixmap(pixmap.scaled(label.width(), label.height(), Qt.KeepAspectRatio))
        else:
            label.clear()

    def update_stitch_position(self):
        """更新拼接线位置"""
        if self.image1 is not None and self.image2 is not None:
            position_ratio = self.slider_stitch_position.value() / 100  # 获取滑动条比例
            stitched_image = self.stitch_images(position_ratio)  # 按比例拼接图像
            if stitched_image is not None:
                self.display_image(stitched_image, self.label_image_stitched)
                self.logs.append(f"Stitch position adjusted: {position_ratio*100:.2f}%")
            else:
                QMessageBox.warning(self, "Error", "Failed to stitch images.")
        else:
            QMessageBox.warning(self, "Error", "Please upload both images before adjusting the stitch position.")

    def stitch_images(self, position_ratio):
        """根据拼接线比例拼接两张图像"""
        if self.image1 is not None and self.image2 is not None:
            # 确保两张图像高度一致
            height = min(self.image1.shape[0], self.image2.shape[0])
            image1_resized = cv2.resize(self.image1, (self.image1.shape[1], height))
            image2_resized = cv2.resize(self.image2, (self.image2.shape[1], height))

            # 按比例分割宽度
            split_width_image1 = int(image1_resized.shape[1] * position_ratio)
            split_width_image2 = int(image2_resized.shape[1] * (1 - position_ratio))

            # 确保拼接部分无越界
            stitched_image = np.hstack((
                image1_resized[:, :split_width_image1],
                image2_resized[:, -split_width_image2:]
            ))

            return stitched_image
        return None


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageStitchingTool()
    window.show()
    sys.exit(app.exec_())
