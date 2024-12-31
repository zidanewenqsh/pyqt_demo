import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from Ui_wanlihong26 import Ui_MainWindow  # 导入编译后的 UI 文件类


class FaceComparisonTool(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 初始化变量
        self.image1 = None
        self.image2 = None
        self.logs = []  # 检验过程日志

        # 绑定按钮信号和槽
        self.button_upload_image1.clicked.connect(self.upload_image1)
        self.button_upload_image2.clicked.connect(self.upload_image2)
        self.button_save_report.clicked.connect(self.save_report)

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

    def save_report(self):
        """保存检验报告"""
        notes = self.textedit_inspection_notes.toPlainText()  # 获取用户说明
        self.logs.append(f"Inspection Notes:\n{notes}")  # 添加说明到日志

        # 保存报告为文本文件
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Report", "", "Text Files (*.txt)")
        if file_path:
            with open(file_path, 'w') as file:
                file.write("\n".join(self.logs))  # 将日志写入文件
            QMessageBox.information(self, "Success", "Report saved successfully!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FaceComparisonTool()
    window.show()
    sys.exit(app.exec_())
