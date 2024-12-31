import sys
import json
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QTableWidgetItem, QMessageBox, QApplication
from Ui_wanlihong2 import Ui_MainWindow  # 假设 UI 文件生成的 Python 类为 ui_mainwindow.py
from datetime import datetime

class CaseManager(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # 数据存储
        self.cases = []  # 用于存储案件数据

        # 信号与槽
        self.button_new_case.clicked.connect(self.new_case)
        self.button_import_cases.clicked.connect(self.import_cases)
        self.button_delete_cases.clicked.connect(self.delete_cases)
        self.button_save_cases.clicked.connect(self.save_cases)

        # 初始化表格
        self.case_table.setColumnCount(4)
        self.case_table.setHorizontalHeaderLabels(["Case ID", "Case Name", "Status", "Created At"])

    def new_case(self):
        case_name, ok = QFileDialog.getSaveFileName(self, "Enter Case Name")
        if not ok or not case_name:
            return
        new_case = {
            "case_id": str(len(self.cases) + 1).zfill(3),
            "case_name": case_name,
            "status": "Ongoing",
            "created_at": QTableWidgetItem(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        }
        self.cases.append(new_case)
        self.refresh_table()

    def import_cases(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Import Cases", "", "JSON Files (*.json)")
        if not file_path:
            return
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                self.cases = json.load(file)
            self.refresh_table()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to import cases: {e}")

    def delete_cases(self):
        selected_rows = set([index.row() for index in self.case_table.selectedIndexes()])
        if not selected_rows:
            QMessageBox.warning(self, "Warning", "No cases selected for deletion.")
            return
        for row in sorted(selected_rows, reverse=True):
            del self.cases[row]
        self.refresh_table()

    def save_cases(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Cases", "", "JSON Files (*.json)")
        if not file_path:
            return
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                json.dump(self.cases, file, ensure_ascii=False, indent=4)
            QMessageBox.information(self, "Success", "Cases saved successfully.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save cases: {e}")

    def refresh_table(self):
        self.case_table.setRowCount(len(self.cases))
        for row, case in enumerate(self.cases):
            self.case_table.setItem(row, 0, QTableWidgetItem(case["case_id"]))
            self.case_table.setItem(row, 1, QTableWidgetItem(case["case_name"]))
            self.case_table.setItem(row, 2, QTableWidgetItem(case["status"]))
            self.case_table.setItem(row, 3, QTableWidgetItem(case["created_at"]))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CaseManager()
    window.show()
    sys.exit(app.exec_())
