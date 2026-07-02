#!/usr/bin/env python3
"""
🍅 番茄钟 — Pomodoro Timer

基于 PyQt6 构建的桌面番茄工作法计时器。
支持任务管理、数据统计、自定义设置、系统托盘。

依赖:
    pip install PyQt6 pyqtgraph plyer win10toast

运行:
    python main.py
"""

import sys
import os

# 确保 src 在路径中
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QFont, QPalette, QColor
from src.ui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("番茄钟")
    app.setApplicationVersion("1.0.0")
    app.setOrganizationName("7xiaoing")

    # ── 全局样式 ──
    app.setStyle("Fusion")
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor("#F5F6FA"))
    palette.setColor(QPalette.ColorRole.WindowText, QColor("#2C3E50"))
    app.setPalette(palette)

    # ── 全局字体 ──
    font = QFont("Segoe UI", 10)
    app.setFont(font)

    # ── 全局样式表 ──
    app.setStyleSheet("""
        QToolTip {
            background: #2C3E50;
            color: white;
            border: none;
            padding: 6px 10px;
            border-radius: 4px;
            font-size: 12px;
        }
        QScrollBar:vertical {
            width: 8px;
            background: transparent;
        }
        QScrollBar::handle:vertical {
            background: #BDC3C7;
            border-radius: 4px;
            min-height: 30px;
        }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 0;
        }
    """)

    # ── 启动主窗口 ──
    window = MainWindow()
    window.show()

    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
