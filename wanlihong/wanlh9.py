import cv2
import numpy as np
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from Ui_wanlihong9 import Ui_MainWindow
class FineAlignment(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 初始化属性
        self.image1 = None  # 原始图像1
        self.image2 = None  # 原始图像2
        self.aligned_image = None  # 对齐后的图像2

        # 信号与槽
        self.button_load_image_1.clicked.connect(lambda: self.load_image(1))
        self.button_load_image_2.clicked.connect(lambda: self.load_image(2))
        self.button_coarse_align.clicked.connect(self.coarse_align)
        self.button_enable_fine_tune.clicked.connect(self.enable_fine_tune)
        self.slider_translate_x.valueChanged.connect(self.fine_tune)
        self.slider_translate_y.valueChanged.connect(self.fine_tune)
        self.slider_rotate.valueChanged.connect(self.fine_tune)
        self.slider_scale.valueChanged.connect(self.fine_tune)

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

    def coarse_align(self):
        """粗对齐：ORB特征点匹配+仿射变换"""
        if self.image1 is None or self.image2 is None:
            QMessageBox.warning(self, "Error", "Please load both images.")
            return

        # ORB 特征点检测
        orb = cv2.ORB_create()
        kp1, des1 = orb.detectAndCompute(self.image1, None)
        kp2, des2 = orb.detectAndCompute(self.image2, None)

        # 特征点匹配
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
        matches = bf.match(des1, des2)

        # 提取匹配点
        points1 = np.float32([kp1[m.queryIdx].pt for m in matches])
        points2 = np.float32([kp2[m.trainIdx].pt for m in matches])

        # 计算仿射变换矩阵
        matrix, _ = cv2.estimateAffinePartial2D(points2, points1)
        self.aligned_image = cv2.warpAffine(self.image2, matrix, (self.image1.shape[1], self.image1.shape[0]))

        # 显示对齐后的图像
        self.show_image(self.aligned_image, self.image_label_2)

    def enable_fine_tune(self):
        """初始化微调滑块"""
        if self.aligned_image is None:
            QMessageBox.warning(self, "Error", "Please perform coarse alignment first.")
            return

        self.slider_translate_x.setValue(0)
        self.slider_translate_y.setValue(0)
        self.slider_rotate.setValue(0)
        self.slider_scale.setValue(100)

    def fine_tune(self):
        """根据滑块值微调对齐结果"""
        if self.aligned_image is None:
            QMessageBox.warning(self, "Error", "Please perform coarse alignment first.")
            return

        tx = self.slider_translate_x.value()  # X轴平移
        ty = self.slider_translate_y.value()  # Y轴平移
        angle = self.slider_rotate.value()  # 旋转角度
        scale = self.slider_scale.value() / 100.0  # 缩放比例

        # 构造仿射矩阵
        center = (self.image1.shape[1] // 2, self.image1.shape[0] // 2)
        rotation_matrix = cv2.getRotationMatrix2D(center, angle, scale)
        rotation_matrix[0, 2] += tx  # 添加X轴平移
        rotation_matrix[1, 2] += ty  # 添加Y轴平移

        # 应用变换
        fine_tuned_image = cv2.warpAffine(self.aligned_image, rotation_matrix, (self.image1.shape[1], self.image1.shape[0]))
        self.show_image(fine_tuned_image, self.image_label_2)

    def show_image(self, image, label):
        """在 QLabel 中显示图像"""
        if image is None:
            QMessageBox.warning(self, "Error", "No image to display.")
            return

        if len(image.shape) == 2:  # 灰度图像
            qimage = QImage(image.data, image.shape[1], image.shape[0], image.strides[0], QImage.Format_Grayscale8)
        else:  # 彩色图像
            rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            qimage = QImage(rgb_image.data, rgb_image.shape[1], rgb_image.shape[0], rgb_image.strides[0], QImage.Format_RGB888)

        pixmap = QPixmap.fromImage(qimage)
        label.setPixmap(pixmap.scaled(label.width(), label.height(), Qt.KeepAspectRatio))

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = FineAlignment()
    window.show()
    sys.exit(app.exec_())
