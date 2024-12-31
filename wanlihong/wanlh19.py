import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from Ui_wanlihong19 import Ui_MainWindow  # 导入编译后的 UI 文件类


class ImageComparisonTool(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 初始化变量
        self.image1 = None
        self.image2 = None
        self.points = []  # 存储点标记
        self.lines = []  # 存储线标记
        self.logs = []  # 记录操作日志

        # 绑定按钮信号和槽
        self.button_upload_image1.clicked.connect(self.upload_image1)
        self.button_upload_image2.clicked.connect(self.upload_image2)
        self.button_add_point.clicked.connect(self.enable_add_point)
        self.button_add_line.clicked.connect(self.enable_add_line)
        self.button_undo.clicked.connect(self.undo_last_action)
        self.button_screenshot.clicked.connect(self.take_screenshot)
        self.button_save_log.clicked.connect(self.save_log)

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

    def enable_add_point(self):
        """启用添加点模式"""
        self.adding_line = False

    def enable_add_line(self):
        """启用添加线模式"""
        self.adding_line = True

    def undo_last_action(self):
        """撤销最后一次操作"""
        if self.lines:
            self.logs.append("Undo line: {}".format(self.lines.pop()))
        elif self.points:
            self.logs.append("Undo point: {}".format(self.points.pop()))
        else:
            QMessageBox.warning(self, "Warning", "No actions to undo!")
            return
        self.display_combined_image()

    def display_combined_image(self):
        """在重叠图像上显示点和线"""
        if self.image1 is None or self.image2 is None:
            return

        combined_image = cv2.addWeighted(self.image1, 0.5, self.image2, 0.5, 0)
        for point in self.points:
            cv2.circle(combined_image, point, 5, (0, 255, 0), -1)
        for line in self.lines:
            cv2.line(combined_image, line[0], line[1], (255, 0, 0), 2)

        self.display_image(combined_image, self.label_image1)

    def take_screenshot(self):
        """截图并保存"""
        if self.image1 is None or self.image2 is None:
            QMessageBox.warning(self, "Error", "Please upload both images first!")
            return

        combined_image = cv2.addWeighted(self.image1, 0.5, self.image2, 0.5, 0)
        for point in self.points:
            cv2.circle(combined_image, point, 5, (0, 255, 0), -1)
        for line in self.lines:
            cv2.line(combined_image, line[0], line[1], (255, 0, 0), 2)

        file_path, _ = QFileDialog.getSaveFileName(self, "Save Screenshot", "", "Image Files (*.png *.jpg *.bmp)")
        if file_path:
            cv2.imwrite(file_path, combined_image)
            QMessageBox.information(self, "Success", "Screenshot saved successfully.")

    def save_log(self):
        """保存日志到文件"""
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Log", "", "Text Files (*.txt)")
        if file_path:
            with open(file_path, "w") as file:
                file.write("\n".join(self.logs))
            QMessageBox.information(self, "Success", "Log saved successfully.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageComparisonTool()
    window.show()
    sys.exit(app.exec_())
