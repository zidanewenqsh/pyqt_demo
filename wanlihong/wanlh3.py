import sys
import json
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QTableWidgetItem, QMessageBox, QApplication
from Ui_wanlihong3 import Ui_MainWindow  # 假设 UI 文件生成的 Python 类为 ui_mainwindow.py
from datetime import datetime


class CaseDossierManager(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        # 数据存储
        self.dossiers = {}

        # 信号与槽
        self.case_list.currentRowChanged.connect(self.update_case_view)
        self.button_add_material.clicked.connect(self.add_material)
        self.button_delete_material.clicked.connect(self.delete_material)
        self.button_view_material.clicked.connect(self.view_material)

    def update_case_view(self, index):
        # 更新右侧表格和日志
        pass

    def add_material(self):
        # 添加素材
        pass

    def delete_material(self):
        # 删除选中素材
        pass

    def view_material(self):
        # 查看选中素材
        pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CaseDossierManager()
    window.show()
    sys.exit(app.exec_())