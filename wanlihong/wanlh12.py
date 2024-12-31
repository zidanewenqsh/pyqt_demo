from Ui_wanlihong12 import Ui_MainWindow
import cv2
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt

class AnnotationWithArrows(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 初始化属性
        self.image = None
        self.annotations = []  # 记录箭头的起点和终点
        self.current_start_point = None  # 当前箭头的起点

        # 信号与槽
        self.button_load_image.clicked.connect(self.load_image)
        self.button_draw_arrow.clicked.connect(self.start_drawing_arrow)
        self.button_undo.clicked.connect(self.undo_last_arrow)
        self.button_save_screenshot.clicked.connect(self.save_screenshot)

    def load_image(self):
        """加载图像"""
        file_path, _ = QFileDialog.getOpenFileName(self, "Load Image", "", "Image Files (*.png *.jpg *.bmp)")
        if file_path:
            self.image = cv2.imread(file_path)
            self.show_image(self.image, self.image_label)
            QMessageBox.information(self, "Image Loaded", "Image successfully loaded.")
        else:
            QMessageBox.warning(self, "No Image Selected", "Please select an image file.")

    def start_drawing_arrow(self):
        """开始绘制箭头"""
        if self.image is None:
            QMessageBox.warning(self, "Error", "Please load an image before drawing.")
            return

        QMessageBox.information(self, "Draw Arrow", "Click to set the start and end points for the arrow.")
        self.image_label.mousePressEvent = self.draw_arrow

    def draw_arrow(self, event):
        """在图像上绘制箭头"""
        x, y = event.pos().x(), event.pos().y()
        if self.current_start_point is None:
            # 设置起点
            self.current_start_point = (x, y)
            self.log_window.append(f"Arrow start point: ({x}, {y})")
        else:
            # 设置终点并绘制箭头
            end_point = (x, y)
            self.annotations.append((self.current_start_point, end_point))
            self.log_window.append(f"Arrow end point: ({x}, {y})")
            self.current_start_point = None  # 重置起点

            # 在图像上绘制箭头
            annotated_image = self.image.copy()
            for start, end in self.annotations:
                cv2.arrowedLine(annotated_image, start, end, (0, 0, 255), 2, tipLength=0.05)

            # 更新显示
            self.show_image(annotated_image, self.image_label)

    def undo_last_arrow(self):
        """撤销最后一个箭头"""
        if self.annotations:
            self.annotations.pop()
            self.log_window.append("Last arrow undone.")
            # 更新图像
            annotated_image = self.image.copy()
            for start, end in self.annotations:
                cv2.arrowedLine(annotated_image, start, end, (0, 0, 255), 2, tipLength=0.05)
            self.show_image(annotated_image, self.image_label)
        else:
            QMessageBox.warning(self, "Error", "No arrows to undo.")

    def save_screenshot(self):
        """保存当前图像的截图"""
        if self.image is None:
            QMessageBox.warning(self, "Error", "No image to save.")
            return

        file_path, _ = QFileDialog.getSaveFileName(self, "Save Screenshot", "", "Image Files (*.png *.jpg *.bmp)")
        if file_path:
            annotated_image = self.image.copy()
            for start, end in self.annotations:
                cv2.arrowedLine(annotated_image, start, end, (0, 0, 255), 2, tipLength=0.05)
            cv2.imwrite(file_path, annotated_image)
            QMessageBox.information(self, "Screenshot Saved", f"Screenshot saved to {file_path}.")
            self.log_window.append(f"Screenshot saved to {file_path}.")

    def show_image(self, image, label):
        """在 QLabel 中显示图像"""
        if image is None:
            return
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        qimage = QImage(rgb_image.data, rgb_image.shape[1], rgb_image.shape[0], rgb_image.strides[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qimage)

        # 确保图像能按照比例缩放显示在 QLabel 中
        label.setPixmap(pixmap.scaled(label.size(), Qt.KeepAspectRatio))

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = AnnotationWithArrows()
    window.show()
    sys.exit(app.exec_())
