from Ui_wanlihong11 import Ui_MainWindow

import cv2
import numpy as np
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt  # 确保导入 Qt 模块
class FacialComparison(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 初始化
        self.image1 = None
        self.image2 = None
        self.annotations_1 = []
        self.annotations_2 = []

        # 信号与槽
        self.button_load_image_1.clicked.connect(lambda: self.load_image(1))
        self.button_load_image_2.clicked.connect(lambda: self.load_image(2))
        self.button_start_comparison.clicked.connect(self.compare_features)

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

    def compare_features(self):
        """比较五官比例"""
        if not self.annotations_1 or not self.annotations_2:
            QMessageBox.warning(self, "Error", "Please annotate features on both images.")
            return

        # 等大对齐
        scale_factor = self.calculate_scale_factor()
        aligned_image2 = cv2.resize(self.image2, None, fx=scale_factor, fy=scale_factor)

        # 计算比例
        proportions_1 = self.calculate_proportions(self.annotations_1)
        proportions_2 = self.calculate_proportions(self.annotations_2)

        # 显示结果
        self.result_display.append("Image 1 Proportions: " + str(proportions_1))
        self.result_display.append("Image 2 Proportions: " + str(proportions_2))
        self.result_display.append("Differences: " + str(np.abs(np.array(proportions_1) - np.array(proportions_2))))

    def calculate_scale_factor(self):
        """计算缩放比例以对齐图像大小"""
        # 示例假设通过眼间距对齐
        eye_distance_1 = np.linalg.norm(np.array(self.annotations_1[0]) - np.array(self.annotations_1[1]))
        eye_distance_2 = np.linalg.norm(np.array(self.annotations_2[0]) - np.array(self.annotations_2[1]))
        return eye_distance_1 / eye_distance_2

    def calculate_proportions(self, annotations):
        """计算五官比例"""
        eye_distance = np.linalg.norm(np.array(annotations[0]) - np.array(annotations[1]))
        nose_to_mouth = np.linalg.norm(np.array(annotations[2]) - np.array(annotations[3]))
        return [eye_distance, nose_to_mouth, eye_distance / nose_to_mouth]

    def show_image(self, image, label):
        """在 QLabel 中显示图像"""
        if image is None:
            return
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        qimage = QImage(rgb_image.data, rgb_image.shape[1], rgb_image.shape[0], rgb_image.strides[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimage)
        label.setPixmap(pixmap.scaled(label.width(), label.height(), Qt.KeepAspectRatio))

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = FacialComparison()
    window.show()
    sys.exit(app.exec_())
