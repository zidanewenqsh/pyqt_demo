import sys
import math
import cv2
from PyQt5.QtGui import QPixmap, QPainter, QColor, QImage
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QTextEdit, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt5 import QtWidgets
from Ui_wanlihong13 import Ui_MainWindow
class ImageMeasurement(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # 初始化UI
        self.image1 = None
        self.image2 = None
        self.points1 = []
        self.points2 = []
        
        # 按钮点击事件连接
        self.button_load_image_1.clicked.connect(self.load_image_1)
        self.button_load_image_2.clicked.connect(self.load_image_2)
        self.button_select_points.clicked.connect(self.select_measurement_points)
        self.button_calculate_results.clicked.connect(self.calculate_results)

    def load_image_1(self):
        """加载图像1"""
        file_path, _ = QFileDialog.getOpenFileName(self, "Load Image 1", "", "Image Files (*.png *.jpg *.bmp)")
        if file_path:
            self.image1 = cv2.imread(file_path)
            self.display_image(self.image1, self.label_image_1)

    def load_image_2(self):
        """加载图像2"""
        file_path, _ = QFileDialog.getOpenFileName(self, "Load Image 2", "", "Image Files (*.png *.jpg *.bmp)")
        if file_path:
            self.image2 = cv2.imread(file_path)
            self.display_image(self.image2, self.label_image_2)

    def display_image(self, image, label):
        """将OpenCV图像显示到QLabel上"""
        if image is not None:
            q_image = self.convert_cv_to_qt(image)  # 将OpenCV图像转换为Qt图像
            pixmap = QPixmap.fromImage(q_image)
            label.setPixmap(pixmap.scaled(label.width(), label.height(), Qt.KeepAspectRatio))

    def convert_cv_to_qt(self, cv_img):
        """将OpenCV图像转换为Qt图像"""
        height, width, channel = cv_img.shape
        bytes_per_line = 3 * width
        cv_img_rgb = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        q_img = QImage(cv_img_rgb.data, width, height, bytes_per_line, QImage.Format_RGB888)
        return q_img

    def mousePressEvent(self, event):
        """处理鼠标点击事件，选择测量点"""
        if self.image1 is not None and self.image2 is not None:
            if event.x() < 350:  # 图像1区域
                point = QPoint(event.x() - 50, event.y() - 50)
                self.points1.append(point)
                self.draw_point(self.label_image_1, point)
            elif event.x() > 450:  # 图像2区域
                point = QPoint(event.x() - 450, event.y() - 50)
                self.points2.append(point)
                self.draw_point(self.label_image_2, point)

    def draw_point(self, label, point):
        """在图像上绘制点"""
        pixmap = label.pixmap()
        painter = QPainter(pixmap)
        painter.setPen(QColor(255, 0, 0))  # 红色点
        painter.setBrush(QColor(255, 0, 0))
        painter.drawEllipse(point, 5, 5)  # 绘制圆点
        painter.end()
        label.setPixmap(pixmap)

    def calculate_distance(self, p1, p2):
        """计算两点之间的距离"""
        return math.sqrt((p2.x() - p1.x()) ** 2 + (p2.y() - p1.y()) ** 2)

    def calculate_angle(self, p1, p2, p3):
        """计算三点之间的角度"""
        angle = math.degrees(math.atan2(p3.y() - p2.y(), p3.x() - p2.x()) - math.atan2(p1.y() - p2.y(), p1.x() - p2.x()))
        return angle if angle >= 0 else angle + 360

    def calculate_ratio(self, p1, p2, p3, p4):
        """计算两点之间的比例"""
        dist1 = self.calculate_distance(p1, p2)
        dist2 = self.calculate_distance(p3, p4)
        return dist1 / dist2 if dist2 != 0 else 0

    def select_measurement_points(self):
        """选择测量点并显示"""
        self.points1.clear()
        self.points2.clear()
        self.textEdit_results.clear()
        self.label_image_1.setText("Image 1: Click to select measurement points")
        self.label_image_2.setText("Image 2: Click to select measurement points")

    def calculate_results(self):
        """计算测量结果并显示"""
        if len(self.points1) < 2 or len(self.points2) < 2:
            self.textEdit_results.setPlainText("Error: Please select at least two points on each image.")
            return

        # 计算点之间的距离
        dist1 = self.calculate_distance(self.points1[0], self.points1[1])
        dist2 = self.calculate_distance(self.points2[0], self.points2[1])
        self.textEdit_results.append(f"Distance between points in Image 1: {dist1:.2f}")
        self.textEdit_results.append(f"Distance between points in Image 2: {dist2:.2f}")

        # 计算角度
        if len(self.points1) >= 3 and len(self.points2) >= 3:
            angle1 = self.calculate_angle(self.points1[0], self.points1[1], self.points1[2])
            angle2 = self.calculate_angle(self.points2[0], self.points2[1], self.points2[2])
            self.textEdit_results.append(f"Angle in Image 1: {angle1:.2f}")
            self.textEdit_results.append(f"Angle in Image 2: {angle2:.2f}")

        # 计算比例
        if len(self.points1) >= 4 and len(self.points2) >= 4:
            ratio = self.calculate_ratio(self.points1[0], self.points1[1], self.points2[0], self.points2[1])
            self.textEdit_results.append(f"Ratio of distances: {ratio:.2f}")

def main():
    app = QApplication(sys.argv)  # 创建一个应用实例
    window = ImageMeasurement()    # 创建主窗口
    window.show()                  # 显示主窗口
    sys.exit(app.exec_())          # 启动事件循环，等待用户操作

if __name__ == "__main__":
    main()  # 调用main函数，启动应用
