from Ui_wanlihong10 import Ui_MainWindow
import csv
import cv2
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt

class FeatureAnnotation(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 初始化属性
        self.image = None  # 上传的图像
        self.annotations = []  # 标注点 (X, Y)

        # 信号与槽
        self.button_load_image.clicked.connect(self.load_image)
        self.button_start_annotation.clicked.connect(self.start_annotation)
        self.button_save_annotation.clicked.connect(self.save_annotation)

    def load_image(self):
        """加载图像"""
        file_path, _ = QFileDialog.getOpenFileName(self, "Load Image", "", "Image Files (*.png *.jpg *.bmp)")
        if file_path:
            self.image = cv2.imread(file_path)
            self.show_image(self.image, self.image_label)
            QMessageBox.information(self, "Image Loaded", "Image successfully loaded.")
        else:
            QMessageBox.warning(self, "No Image Selected", "Please select an image file.")

    def start_annotation(self):
        """开始标注"""
        if self.image is None:
            QMessageBox.warning(self, "Error", "Please load an image before annotation.")
            return

        QMessageBox.information(self, "Annotation Mode", "Click on the image to mark feature points.")
        self.image_label.mousePressEvent = self.annotate_image

    # def annotate_image(self, event):
    #     """在图像上标注点"""
    #     x, y = event.pos().x(), event.pos().y()
    #     self.annotations.append((x, y))
    #     self.log_window.append(f"Annotation: ({x}, {y})")
    def annotate_image(self, event):
        """在图像上标注点并显示红点"""
        x, y = event.pos().x(), event.pos().y()
        self.annotations.append((x, y))
        self.log_window.append(f"Annotation: ({x}, {y})")

        # 绘制红点
        if self.image is not None:
            # 在原图上绘制点
            annotated_image = self.image.copy()
            for point_x, point_y in self.annotations:
                cv2.circle(annotated_image, (point_x, point_y), 5, (0, 0, 255), -1)

            # 更新显示
            self.show_image(annotated_image, self.image_label)

    def save_annotation(self):
        """保存标注结果到CSV文件"""
        if not self.annotations:
            QMessageBox.warning(self, "Error", "No annotations to save.")
            return

        file_path, _ = QFileDialog.getSaveFileName(self, "Save Annotations", "", "CSV Files (*.csv)")
        if file_path:
            with open(file_path, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Point Number", "X", "Y"])
                for i, (x, y) in enumerate(self.annotations, start=1):
                    writer.writerow([i, x, y])
            QMessageBox.information(self, "Annotations Saved", f"Annotations successfully saved to {file_path}.")
            self.log_window.append(f"Annotations saved to {file_path}.")

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
    window = FeatureAnnotation()
    window.show()
    sys.exit(app.exec_())
