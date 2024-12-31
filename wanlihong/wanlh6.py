import sys
import cv2
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from Ui_wanlihong6 import Ui_MainWindow  # 假设简化版 UI 文件已生成为 Python 文件

class ImagePreprocessing(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 初始化属性
        self.original_image = None
        self.processed_image = None

        # 信号与槽
        self.button_load_image.clicked.connect(self.load_image)
        self.preprocessing_options.addItems(["Grayscale", "Brightness", "Sharpen", "Denoise", "Rotate", "Scale"])

    def load_image(self):
        """加载图像文件"""
        file_path, _ = QFileDialog.getOpenFileName(self, "Load Image", "", "Image Files (*.png *.jpg *.bmp)")
        if file_path:
            self.original_image = cv2.imread(file_path)
            self.processed_image = self.original_image.copy()
            self.show_image(self.original_image, self.original_image_label)
            self.show_image(self.processed_image, self.processed_image_label)
            QMessageBox.information(self, "Image Loaded", "Image successfully loaded.")
        else:
            QMessageBox.warning(self, "No Image Selected", "Please select an image file to load.")

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
    window = ImagePreprocessing()
    window.show()
    sys.exit(app.exec_())
