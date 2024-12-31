import sys
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from Ui_wanlihong15 import Ui_MainWindow  # 导入编译后的 UI 文件类


class ImageMeasurement(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.image = None
        self.logs = []  # 日志记录

        # 绑定按钮信号和槽
        self.button_upload_image.clicked.connect(self.upload_image)
        self.button_undo.clicked.connect(self.undo_action)
        self.button_reset.clicked.connect(self.reset_image)
        self.button_modify.clicked.connect(self.modify_feature)
        self.button_delete.clicked.connect(self.delete_feature)
        self.button_screenshot.clicked.connect(self.take_screenshot)
        self.button_generate_table.clicked.connect(self.generate_table)

    def upload_image(self):
        """上传图像并显示在 QLabel 中"""
        file_path, _ = QFileDialog.getOpenFileName(self, "Upload Image", "", "Image Files (*.png *.jpg *.bmp)")
        if file_path:
            self.image = cv2.imread(file_path)
            self.display_image(self.image)

    def display_image(self, image):
        """显示图像在 QLabel 中"""
        if image is not None:
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            height, width, channel = image_rgb.shape
            bytes_per_line = channel * width
            q_image = QImage(image_rgb.data, width, height, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            self.label_image.setPixmap(pixmap.scaled(self.label_image.width(), self.label_image.height(), Qt.KeepAspectRatio))

    def undo_action(self):
        """撤销操作"""
        QMessageBox.information(self, "Undo", "Undo action triggered!")

    def reset_image(self):
        """重置图像"""
        if self.image is not None:
            self.display_image(self.image)
            self.logs.clear()
            self.textEdit_results.clear()
            QMessageBox.information(self, "Reset", "Image reset completed.")

    def modify_feature(self):
        """修改特征"""
        QMessageBox.information(self, "Modify", "Modify feature triggered!")

    def delete_feature(self):
        """删除特征"""
        QMessageBox.information(self, "Delete", "Delete feature triggered!")

    def take_screenshot(self):
        """截图并保存"""
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Screenshot", "", "Image Files (*.png *.jpg *.bmp)")
        if file_path:
            if self.image is not None:
                cv2.imwrite(file_path, self.image)
                QMessageBox.information(self, "Screenshot", "Screenshot saved successfully.")
            else:
                QMessageBox.warning(self, "Error", "No image to save.")

    def generate_table(self):
        """生成特征值表格"""
        QMessageBox.information(self, "Generate Table", "Generate table triggered!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageMeasurement()
    window.show()
    sys.exit(app.exec_())
