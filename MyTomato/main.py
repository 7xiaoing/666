import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QMessageBox
from PySide6.QtCore import QTimer, Qt

class TomatoClock(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("我的番茄钟")
        self.setFixedSize(300, 250) # 宽高
        
        # 核心数据
        self.total_seconds = 25 * 60  # 25分钟
        self.remaining_seconds = self.total_seconds
        self.is_running = False

        # 创建显示标签和按钮
        self.label = QLabel("25:00", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 48px; font-weight: bold; color: #e74c3c;")
        
        self.start_btn = QPushButton("开始专注", self)
        self.start_btn.clicked.connect(self.toggle_timer)

        # 布局
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.start_btn)
        
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # 定时器（心脏）
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)
        # 定时器1秒触发一次
        self.timer.setInterval(1000)

    # 启动/暂停计时器
    def toggle_timer(self):
        if not self.is_running:
            # 开始计时
            self.timer.start()
            self.is_running = True
            self.start_btn.setText("暂停")
        else:
            # 暂停计时
            self.timer.stop()
            self.is_running = False
            self.start_btn.setText("继续专注")

    # 每秒刷新时间
    def update_timer(self):
        self.remaining_seconds -= 1
        # 分钟、秒计算
        minute = self.remaining_seconds // 60
        second = self.remaining_seconds % 60
        self.label.setText(f"{minute:02d}:{second:02d}")

        # 倒计时结束
        if self.remaining_seconds <= 0:
            self.timer.stop()
            self.is_running = False
            self.start_btn.setText("重新开始")
            # 弹窗提醒
            QMessageBox.information(self, "完成", "本次番茄专注结束！可以休息啦")
            # 重置时间
            self.remaining_seconds = self.total_seconds
            self.label.setText("25:00")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TomatoClock()
    window.show()
    sys.exit(app.exec())