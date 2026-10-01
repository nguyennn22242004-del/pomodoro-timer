import sys
import os
import json
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                             QLabel, QPushButton, QSpinBox, QMessageBox)
from PyQt6.QtCore import QTimer, Qt

DATA_FILE = os.path.expanduser("~/.pomodoro_data.json")

class PomodoroTimer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("Pomodoro Timer - Ubuntu")
        self.setFixedSize(350, 400)
        
        # Thời gian mặc định (giây)
        self.work_time = 25 * 60
        self.break_time = 5 * 60
        self.time_left = self.work_time
        self.is_work_mode = True
        self.is_running = False
        self.completed_sessions = self.load_data()

        # Layout chính
        layout = QVBoxLayout()

        # Chế độ làm việc / nghỉ ngơi
        self.status_label = QLabel("LÀM VIỆC", self)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("font-size: 20px; font-weight: bold; color: #2C3E50;")
        layout.addWidget(self.status_label)

        # Đếm ngược thời gian
        self.timer_label = QLabel(self.format_time(self.time_left), self)
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.timer_label.setStyleSheet("font-size: 48px; font-weight: bold; color: #E74C3C;")
        layout.addWidget(self.timer_label)

        # Số phiên hoàn thành
        self.stats_label = QLabel(f"Số phiên hoàn thành: {self.completed_sessions}", self)
        self.stats_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.stats_label)

        # Các nút điều khiển
        btn_layout = QHBoxLayout()
        self.start_btn = QPushButton("Bắt đầu", self)
        self.start_btn.clicked.connect(self.start_timer)
        btn_layout.addWidget(self.start_btn)

        self.pause_btn = QPushButton("Tạm dừng", self)
        self.pause_btn.clicked.connect(self.pause_timer)
        btn_layout.addWidget(self.pause_btn)

        self.reset_btn = QPushButton("Đặt lại", self)
        self.reset_btn.clicked.connect(self.reset_timer)
        btn_layout.addWidget(self.reset_btn)

        layout.addLayout(btn_layout)

        # Timer của Qt
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)

        self.setLayout(layout)

    def format_time(self, seconds):
        mins = seconds // 60
        secs = seconds % 60
        return f"{mins:02d}:{secs:02d}"

    def start_timer(self):
        if not self.is_running:
            self.timer.start(1000)
            self.is_running = True

    def pause_timer(self):
        if self.is_running:
            self.timer.stop()
            self.is_running = False

    def reset_timer(self):
        self.timer.stop()
        self.is_running = False
        self.is_work_mode = True
        self.time_left = self.work_time
        self.status_label.setText("LÀM VIỆC")
        self.timer_label.setText(self.format_time(self.time_left))

    def update_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_label.setText(self.format_time(self.time_left))
        else:
            self.timer.stop()
            self.is_running = False
            if self.is_work_mode:
                self.completed_sessions += 1
                self.save_data()
                self.stats_label.setText(f"Số phiên hoàn thành: {self.completed_sessions}")
                QMessageBox.information(self, "Hết giờ!", "Hoàn thành phiên làm việc! Hãy nghỉ ngơi chút nhé.")
                self.is_work_mode = False
                self.status_label.setText("NGHỈ NGƠI")
                self.time_left = self.break_time
            else:
                QMessageBox.information(self, "Hết giờ nghỉ!", "Hết giờ nghỉ ngơi! Bắt đầu phiên làm việc mới thôi.")
                self.is_work_mode = True
                self.status_label.setText("LÀM VIỆC")
                self.time_left = self.work_time
            
            self.timer_label.setText(self.format_time(self.time_left))

    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r") as f:
                    data = json.load(f)
                    return data.get("completed_sessions", 0)
            except Exception:
                return 0
        return 0

    def save_data(self):
        with open(DATA_FILE, "w") as f:
            json.dump({"completed_sessions": self.completed_sessions}, f)

def main():
    app = QApplication(sys.argv)
    timer_app = PomodoroTimer()
    timer_app.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()