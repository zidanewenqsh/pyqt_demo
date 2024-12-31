import sys
import cv2
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from Ui_wanlihong27 import Ui_MainWindow  # 导入编译后的 UI 文件类


class ReportGenerationTool(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 初始化变量
        self.image1_path = None
        self.image2_path = None
        self.logs = []  # 记录鉴定过程的日志

        # 绑定按钮信号和槽
        self.button_upload_image1.clicked.connect(self.upload_image1)
        self.button_upload_image2.clicked.connect(self.upload_image2)
        self.button_save_report.clicked.connect(self.save_report)

    def upload_image1(self):
        """上传检材图像"""
        file_path, _ = QFileDialog.getOpenFileName(self, "Upload Image 1", "", "Image Files (*.png *.jpg *.bmp)")
        if file_path:
            self.image1_path = file_path
            image = cv2.imread(file_path)
            self.display_image(image, self.label_image1)
            self.logs.append(f"Image 1 uploaded: {file_path}")

    def upload_image2(self):
        """上传样本图像"""
        file_path, _ = QFileDialog.getOpenFileName(self, "Upload Image 2", "", "Image Files (*.png *.jpg *.bmp)")
        if file_path:
            self.image2_path = file_path
            image = cv2.imread(file_path)
            self.display_image(image, self.label_image2)
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
        """生成并保存鉴定文书报告"""
        # 获取用户输入的委托事项
        commission = self.textedit_commission.toPlainText()

        # 构建报告内容
        report_content = [
            "鉴定文书报告",
            "=" * 30,
            f"委托事项:\n{commission}",
            "",
            f"检材路径: {self.image1_path or '未提供'}",
            f"样本路径: {self.image2_path or '未提供'}",
            "",
            "鉴定过程记录:",
            "\n".join(self.logs),
            "",
            "比对方法: 使用 Dlib 的欧氏距离方法",
            "比对过程: 请参阅过程日志。",
            "结论: 请根据比对结果填写结论。",
        ]

        # 保存报告到文件
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Report", "", "Text Files (*.txt)")
        if file_path:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write("\n".join(report_content))
            QMessageBox.information(self, "Success", "Report saved successfully!")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ReportGenerationTool()
    window.show()
    sys.exit(app.exec_())
