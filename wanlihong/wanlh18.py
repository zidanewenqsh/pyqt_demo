import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from Ui_wanlihong18 import Ui_MainWindow  # 导入编译后的 UI 文件类


class ImageAnnotationTool(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 初始化变量
        self.image1 = None
        self.image2 = None
        self.alpha = 0.5  # 初始透明度值
        self.points = []  # 存储标记的点
        self.lines = []  # 存储标记的线（由两点组成）

        # 绑定按钮信号和槽
        self.button_upload_image1.clicked.connect(self.upload_image1)
        self.button_upload_image2.clicked.connect(self.upload_image2)
        self.button_add_point.clicked.connect(self.enable_add_point)
        self.button_add_line.clicked.connect(self.enable_add_line)
        self.button_save_annotations.clicked.connect(self.save_annotations)

        self.adding_line = False  # 当前是否处于添加线模式

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

        # 添加标记
        for point in self.points:
            cv2.circle(overlap_image, point, 5, (0, 255, 0), -1)  # 绘制绿色点
        for line in self.lines:
            cv2.line(overlap_image, line[0], line[1], (255, 0, 0), 2)  # 绘制蓝色线

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

    def enable_add_point(self):
        """启用添加点模式"""
        self.adding_line = False
        self.setMouseTracking(True)

    def enable_add_line(self):
        """启用添加线模式"""
        self.adding_line = True
        self.setMouseTracking(True)

    def mousePressEvent(self, event):
        """鼠标点击事件，用于添加点或线"""
        if event.button() == Qt.LeftButton and self.image1 is not None and self.image2 is not None:
            x = event.x() - 50  # 偏移以适应 QLabel 的位置
            y = event.y() - 50
            if 0 <= x <= self.image1.shape[1] and 0 <= y <= self.image1.shape[0]:
                if self.adding_line and len(self.points) % 2 == 1:
                    # 添加线
                    self.lines.append((self.points[-1], (x, y)))
                    self.points.append((x, y))
                else:
                    # 添加点
                    self.points.append((x, y))
                self.display_overlap()

    def save_annotations(self):
        """保存带标记的图像"""
        if self.image1 is None or self.image2 is None:
            QMessageBox.warning(self, "Error", "Please upload both images first!")
            return

        # 生成重叠图像
        overlap_image = cv2.addWeighted(self.image1, self.alpha, self.image2, 1 - self.alpha, 0)
        for point in self.points:
            cv2.circle(overlap_image, point, 5, (0, 255, 0), -1)  # 绘制绿色点
        for line in self.lines:
            cv2.line(overlap_image, line[0], line[1], (255, 0, 0), 2)  # 绘制蓝色线

        # 保存图像
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Annotations", "", "Image Files (*.png *.jpg *.bmp)")
        if file_path:
            cv2.imwrite(file_path, overlap_image)
            QMessageBox.information(self, "Success", "Annotated image saved successfully.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageAnnotationTool()
    window.show()
    sys.exit(app.exec_())
