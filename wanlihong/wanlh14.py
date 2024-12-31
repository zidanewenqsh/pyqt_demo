import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QPixmap, QImage
import cv2
import numpy as np
from PyQt5 import uic

# 导入UI文件编译后的类
from Ui_wanlihong14 import Ui_MainWindow

class ImageMeasurement(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # 调用UI文件中的setupUi方法进行初始化

        self.image1 = None
        self.image1_scaled = None
        self.feature_points = []  # 存储特征点

        # 连接信号和槽
        self.button_load_image.clicked.connect(self.load_image)
        self.slider_scale.valueChanged.connect(self.update_image_scale)
        self.button_adjust_point.clicked.connect(self.adjust_feature_point)

    def load_image(self):
        """加载图像并显示"""
        file_path, _ = QFileDialog.getOpenFileName(self, "Load Image", "", "Image Files (*.png *.jpg *.bmp)")
        if file_path:
            self.image1 = cv2.imread(file_path)
            self.image1_scaled = self.image1.copy()  # 缩放后的图像
            self.display_image(self.image1_scaled)

    def display_image(self, image):
        """将图像显示在QLabel中"""
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        h, w, _ = image_rgb.shape
        q_image = QImage(image_rgb.data, w, h, 3 * w, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)
        self.label_image.setPixmap(pixmap.scaled(self.label_image.width(), self.label_image.height(), Qt.KeepAspectRatio))

    def update_image_scale(self):
        """根据缩放滑块的值更新图像大小"""
        if self.image1 is not None:
            scale_factor = self.slider_scale.value() / 100
            height, width = self.image1.shape[:2]
            new_dimensions = (int(width * scale_factor), int(height * scale_factor))
            self.image1_scaled = cv2.resize(self.image1, new_dimensions, interpolation=cv2.INTER_LINEAR)
            self.display_image(self.image1_scaled)

    def adjust_feature_point(self):
        """微调特征点位置"""
        if self.feature_points:
            last_point = self.feature_points[-1]
            adjusted_point = (last_point[0] + 5, last_point[1] + 5)  # 微调特征点坐标
            self.feature_points[-1] = adjusted_point
            self.textEdit_results.append(f"Feature Point Adjusted to: {adjusted_point}")
            self.update_image_with_points()

    def update_image_with_points(self):
        """在图像上绘制特征点"""
        image_with_points = self.image1_scaled.copy()
        for point in self.feature_points:
            cv2.circle(image_with_points, point, 5, (0, 0, 255), -1)  # 在图像上绘制红色圆点
        self.display_image(image_with_points)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageMeasurement()
    window.show()
    sys.exit(app.exec_())
