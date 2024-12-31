import cv2
import numpy as np
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from Ui_wanlihong8 import Ui_MainWindow
class PerspectiveAlignment(QMainWindow, Ui_MainWindow):
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
        self.button_perspective_auto.clicked.connect(self.auto_perspective)
        self.button_perspective_manual.clicked.connect(self.enable_manual_perspective)
        self.button_clear_points.clicked.connect(self.clear_manual_points)

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

    def auto_perspective(self):
        """自动透视对齐"""
        if self.image1 is None or self.image2 is None:
            QMessageBox.warning(self, "Error", "Please load both images.")
            return

        # 假设通过特征点匹配获取四对点
        points1 = np.float32([[50, 50], [300, 50], [50, 300], [300, 300]])  # 图像1的点
        points2 = np.float32([[40, 60], [310, 40], [60, 310], [290, 290]])  # 图像2的点

        # 计算透视变换矩阵
        matrix = cv2.getPerspectiveTransform(points2, points1)
        result = cv2.warpPerspective(self.image2, matrix, (self.image1.shape[1], self.image1.shape[0]))
        self.show_image(result, self.image_label_2)

    def enable_manual_perspective(self):
        """启用手动透视模式"""
        QMessageBox.information(self, "Manual Perspective", "Click four corresponding points on both images.")

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

        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        qimage = QImage(rgb_image.data, rgb_image.shape[1], rgb_image.shape[0], rgb_image.strides[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimage)
        label.setPixmap(pixmap.scaled(label.width(), label.height(), Qt.KeepAspectRatio))

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = PerspectiveAlignment()
    window.show()
    sys.exit(app.exec_())
