"""主窗口 — 番茄钟应用主界面容器。"""

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QStackedWidget, QLabel, QFrame,
    QApplication, QSystemTrayIcon, QMenu
)
from PyQt6.QtGui import QFont, QIcon, QAction, QPixmap, QPainter, QColor

from ..timer import PomodoroTimer, TimerPhase, TimerState
from ..models.settings import SettingsManager
from ..models.statistics import StatsManager, PomodoroRecord

from .timer_widget import TimerWidget
from .statistics_widget import StatisticsWidget
from .task_widget import TaskWidget
from .settings_widget import SettingsWidget


class SidebarButton(QPushButton):
    """侧边栏导航按钮"""

    def __init__(self, text: str, icon: str = ""):
        super().__init__(f"{icon} {text}")
        self.setFixedHeight(48)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet("""
            QPushButton {
                background: transparent;
                color: #7F8C8D;
                border: none;
                border-radius: 10px;
                padding: 0 16px;
                text-align: left;
                font-size: 14px;
            }
            QPushButton:hover {
                background: #34495E;
                color: #ECF0F1;
            }
            QPushButton:checked {
                background: #2980B9;
                color: white;
                font-weight: bold;
            }
        """
        )
        self.setCheckable(True)


class MainWindow(QMainWindow):
    """番茄钟应用主窗口"""

    def __init__(self):
        super().__init__()

        # ── 核心服务 ──
        self._settings_manager = SettingsManager()
        self._stats_manager = StatsManager()
        self._timer = PomodoroTimer()
        self._apply_settings()

        self._tray_icon = None  # 初始化，避免系统托盘不可用时崩溃

        self._setup_window()
        self._setup_ui()
        self._setup_tray()
        self._connect_signals()

    def _setup_window(self):
        self.setWindowTitle("🍅 番茄钟")
        self.setMinimumSize(900, 650)
        self.resize(960, 700)
        self.setStyleSheet("""
            QMainWindow {
                background: #F5F6FA;
            }
        """)

    def _setup_ui(self):
        # ── 中央容器 ──
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # ── 侧边栏 ──
        sidebar = QFrame()
        sidebar.setFixedWidth(200)
        sidebar.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 #2C3E50, stop:1 #1A252F);
        """)

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(12, 20, 12, 20)
        sidebar_layout.setSpacing(8)

        # Logo
        logo = QLabel("🍅")
        logo.setStyleSheet("font-size: 36px;")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        app_name = QLabel("番茄钟")
        app_name.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        app_name.setStyleSheet("color: white;")
        app_name.setAlignment(Qt.AlignmentFlag.AlignCenter)

        version = QLabel("v1.0.0")
        version.setStyleSheet("color: #7F8C8D; font-size: 11px;")
        version.setAlignment(Qt.AlignmentFlag.AlignCenter)

        sidebar_layout.addWidget(logo)
        sidebar_layout.addWidget(app_name)
        sidebar_layout.addWidget(version)
        sidebar_layout.addSpacing(30)

        # 导航按钮
        self._nav_buttons = []
        nav_items = [
            ("timer", "⏱️", "计时器"),
            ("stats", "📊", "统计"),
            ("tasks", "📋", "任务"),
            ("settings", "⚙️", "设置"),
        ]

        for key, icon, label in nav_items:
            btn = SidebarButton(label, icon)
            btn.clicked.connect(lambda checked, k=key: self._switch_page(k))
            self._nav_buttons.append(btn)
            sidebar_layout.addWidget(btn)

        sidebar_layout.addStretch()

        # 底部信息
        footer = QLabel("🍅 专注每一刻")
        footer.setStyleSheet("color: #566573; font-size: 11px;")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(footer)

        # ── 内容区域 ──
        content = QFrame()
        content.setStyleSheet("background: #F5F6FA;")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)

        self._stack = QStackedWidget()

        # 各页面
        self._timer_widget = TimerWidget(self._timer)
        self._stats_widget = StatisticsWidget(self._stats_manager)
        self._task_widget = TaskWidget()
        self._settings_widget = SettingsWidget(self._settings_manager)

        self._stack.addWidget(self._timer_widget)   # index 0
        self._stack.addWidget(self._stats_widget)   # index 1
        self._stack.addWidget(self._task_widget)    # index 2
        self._stack.addWidget(self._settings_widget)  # index 3

        content_layout.addWidget(self._stack)

        # ── 组装 ──
        main_layout.addWidget(sidebar)
        main_layout.addWidget(content)

        # 默认选中第一个
        if self._nav_buttons:
            self._nav_buttons[0].setChecked(True)

    def _setup_tray(self):
        """系统托盘"""
        if QSystemTrayIcon.isSystemTrayAvailable():
            self._tray_icon = QSystemTrayIcon(self)
            # 创建简单的图标
            pixmap = QPixmap(32, 32)
            pixmap.fill(QColor("#E74C3C"))
            self._tray_icon.setIcon(QIcon(pixmap))
            self._tray_icon.setToolTip("🍅 番茄钟")

            tray_menu = QMenu()
            show_action = tray_menu.addAction("显示窗口")
            show_action.triggered.connect(self.show)

            quit_action = tray_menu.addAction("退出")
            quit_action.triggered.connect(QApplication.instance().quit)

            self._tray_icon.setContextMenu(tray_menu)
            self._tray_icon.activated.connect(self._on_tray_activated)
            self._tray_icon.show()

    def _connect_signals(self):
        self._timer.completed.connect(self._on_timer_completed)
        self._timer.tick.connect(self._update_tray_tooltip)

    def _switch_page(self, key: str):
        pages = {"timer": 0, "stats": 1, "tasks": 2, "settings": 3}
        idx = pages.get(key, 0)
        self._stack.setCurrentIndex(idx)

        for btn in self._nav_buttons:
            btn.setChecked(False)
        idx_map = {"timer": 0, "stats": 1, "tasks": 2, "settings": 3}
        self._nav_buttons[idx_map.get(key, 0)].setChecked(True)

        # 刷新统计页面
        if key == "stats":
            from ..models.statistics import DailyStats
            # 简单刷新
            self._stats_widget.deleteLater()
            self._stats_widget = StatisticsWidget(self._stats_manager)
            self._stack.removeWidget(self._stack.widget(1))
            self._stack.insertWidget(1, self._stats_widget)
            self._stack.setCurrentIndex(1)

    def _apply_settings(self):
        s = self._settings_manager.settings
        self._timer.configure(
            work_sec=s.timer.work_seconds,
            short_break_sec=s.timer.short_break_seconds,
            long_break_sec=s.timer.long_break_seconds,
            long_break_interval=s.timer.long_break_interval,
        )

    def _on_timer_completed(self, phase_name: str):
        if phase_name == "work":
            record = PomodoroRecord(
                duration=self._timer._work_sec,
                task_name=self._task_widget.get_active_tasks()[0]
                    if self._task_widget.get_active_tasks() else "专注",
            )
            self._stats_manager.add_record(record)
            self._timer_widget.update_count(
                self._stats_manager.get_today_stats().completed_pomodoros
            )
            self._show_notification("🍅 番茄完成！", "太棒了！该休息一下了 ✨")

        elif phase_name == "break":
            self._show_notification("☕ 休息结束", "准备开始新的番茄吧！")

        # 自动开始
        s = self._settings_manager.settings
        if phase_name == "work" and s.timer.auto_start_break:
            self._timer.start_break()
        elif phase_name == "break" and s.timer.auto_start_work:
            self._timer.start_work()

    def _show_notification(self, title: str, message: str):
        """显示桌面通知"""
        if not self._settings_manager.settings.notification_enabled:
            return

        if self._tray_icon and QSystemTrayIcon.supportsMessages():
            self._tray_icon.showMessage(title, message, QSystemTrayIcon.MessageIcon.Information, 5000)

    def _update_tray_tooltip(self, remaining: int):
        if self._tray_icon is None:
            return
        if self._timer.state == TimerState.RUNNING:
            m = remaining // 60
            s = remaining % 60
            self._tray_icon.setToolTip(f"🍅 {m:02d}:{s:02d}")

    def _on_tray_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.DoubleClick:
            self.show()

    def closeEvent(self, event):
        if self._settings_manager.settings.minimize_to_tray:
            event.ignore()
            self.hide()
            self._show_notification("番茄钟", "已最小化到托盘，双击恢复")
        else:
            event.accept()
