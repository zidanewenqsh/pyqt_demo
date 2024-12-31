import sys
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from Ui_wanlihong16 import Ui_MainWindow  # 导入编译生成的 UI 文件类


class MeasurementTool(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.image = None
        self.points = []  # 存储用户选择的特征点
        self.logs = []  # 存储测量日志

        # 绑定信号和槽
        self.button_upload_image.clicked.connect(self.upload_image)
        self.button_add_point.clicked.connect(self.enable_point_selection)
        self.button_measure_distance.clicked.connect(self.measure_distance)
        self.button_measure_angle.clicked.connect(self.measure_angle)
        self.button_measure_ratio.clicked.connect(self.measure_ratio)
        self.button_save_logs.clicked.connect(self.save_logs)

    def upload_image(self):
        """上传图像并显示在 QLabel 中"""
        file_path, _ = QFileDialog.getOpenFileName(self, "Upload Image", "", "Image Files (*.png *.jpg *.bmp)")
        if file_path:
            self.image = cv2.imread(file_path)
            self.display_image(self.image)

    def display_image(self, image):
        """显示图像在 QLabel 上"""
        if image is not None:
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            height, width, channel = image_rgb.shape
            bytes_per_line = channel * width
            q_image = QImage(image_rgb.data, width, height, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            self.label_image.setPixmap(pixmap.scaled(self.label_image.width(), self.label_image.height(), Qt.KeepAspectRatio))

    def enable_point_selection(self):
        """启用鼠标点击选择端点"""
        if self.image is None:
            QMessageBox.warning(self, "Error", "Please upload an image first.")
            return
        self.setMouseTracking(True)

    def mousePressEvent(self, event):
        """鼠标点击事件：选择特征点"""
        if event.button() == Qt.LeftButton and self.image is not None:
            x = event.x() - 50  # 偏移以适应 QLabel 的位置
            y = event.y() - 60
            if 0 <= x <= 700 and 0 <= y <= 400:  # 限制点击范围
                self.points.append((x, y))
                self.logs.append(f"Added point: ({x}, {y})")
                self.update_image_with_points()
                self.update_logs()

    def update_image_with_points(self):
        """在图像上绘制特征点"""
        if self.image is not None:
            image_with_points = self.image.copy()
            for point in self.points:
                cv2.circle(image_with_points, point, 5, (0, 0, 255), -1)
            self.display_image(image_with_points)

    def measure_distance(self):
        """测量两点之间的距离"""
        if len(self.points) < 2:
            QMessageBox.warning(self, "Error", "Please select at least 2 points.")
            return
        p1, p2 = self.points[-2], self.points[-1]
        distance = ((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2) ** 0.5
        self.logs.append(f"Distance between {p1} and {p2}: {distance:.2f}")
        self.update_logs()

    def measure_angle(self):
        """测量三点之间的角度"""
        if len(self.points) < 3:
            QMessageBox.warning(self, "Error", "Please select at least 3 points.")
            return
        p1, p2, p3 = self.points[-3], self.points[-2], self.points[-1]
        angle = self.calculate_angle(p1, p2, p3)
        self.logs.append(f"Angle between {p1}, {p2}, {p3}: {angle:.2f} degrees")
        self.update_logs()

    def measure_ratio(self):
        """测量两段距离的比例"""
        if len(self.points) < 4:
            QMessageBox.warning(self, "Error", "Please select at least 4 points.")
            return
        p1, p2, p3, p4 = self.points[-4], self.points[-3], self.points[-2], self.points[-1]
        d1 = ((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2) ** 0.5
        d2 = ((p4[0] - p3[0]) ** 2 + (p4[1] - p3[1]) ** 2) ** 0.5
        ratio = d1 / d2 if d2 != 0 else 0
        self.logs.append(f"Ratio of distances: {d1:.2f}/{d2:.2f} = {ratio:.2f}")
        self.update_logs()

    def save_logs(self):
        """保存日志到文件"""
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Logs", "", "Text Files (*.txt)")
        if file_path:
            with open(file_path, "w") as f:
                f.write("\n".join(self.logs))
            QMessageBox.information(self, "Success", "Logs saved successfully.")

    def update_logs(self):
        """更新日志显示"""
        self.textEdit_logs.setText("\n".join(self.logs))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MeasurementTool()
    window.show()
    sys.exit(app.exec_())
