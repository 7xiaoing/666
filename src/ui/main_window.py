"""主窗口 — 番茄钟应用主界面容器。"""

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QStackedWidget, QLabel, QFrame,
    QApplication, QSystemTrayIcon, QMenu
)
from PyQt6.QtGui import QFont, QIcon, QAction, QPixmap, QPainter, QColor, QPalette

from ..timer import PomodoroTimer, TimerPhase, TimerState
from ..models.settings import SettingsManager
from ..models.statistics import StatsManager, PomodoroRecord
from ..i18n import STRINGS

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

        # 应用初始语言设置
        s = self._settings_manager.settings
        self._apply_language(s.language)

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
        self._sidebar_logo = QLabel("🍅")
        self._sidebar_logo.setStyleSheet("font-size: 36px;")
        self._sidebar_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._sidebar_title = QLabel("番茄钟")
        self._sidebar_title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        self._sidebar_title.setStyleSheet("color: white;")
        self._sidebar_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._sidebar_version = QLabel("v1.0.0")
        self._sidebar_version.setStyleSheet("color: #7F8C8D; font-size: 11px;")
        self._sidebar_version.setAlignment(Qt.AlignmentFlag.AlignCenter)

        sidebar_layout.addWidget(self._sidebar_logo)
        sidebar_layout.addWidget(self._sidebar_title)
        sidebar_layout.addWidget(self._sidebar_version)
        sidebar_layout.addSpacing(30)

        # 导航按钮
        self._nav_buttons = []
        self._nav_keys = ["timer", "stats", "tasks", "settings"]
        self._nav_icons = ["⏱️", "📊", "📋", "⚙️"]
        nav_labels = ["计时器", "统计", "任务", "设置"]

        for key, icon, label in zip(self._nav_keys, self._nav_icons, nav_labels):
            btn = SidebarButton(label, icon)
            btn.clicked.connect(lambda checked, k=key: self._switch_page(k))
            self._nav_buttons.append(btn)
            sidebar_layout.addWidget(btn)

        sidebar_layout.addStretch()

        # 底部信息
        self._sidebar_footer = QLabel("🍅 专注每一刻")
        self._sidebar_footer.setStyleSheet("color: #566573; font-size: 11px;")
        self._sidebar_footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        sidebar_layout.addWidget(self._sidebar_footer)

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
        self._settings_widget.settings_changed.connect(self._on_settings_changed)

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

    def _on_settings_changed(self, changes: dict):
        """收到设置变更通知，应用主题/语言等"""
        if "theme" in changes:
            self._apply_theme(changes["theme"])
        if "language" in changes:
            self._apply_language(changes["language"])
        if "timer" in changes:
            t = changes["timer"]
            self._timer.configure(
                work_sec=t.work_seconds,
                short_break_sec=t.short_break_seconds,
                long_break_sec=t.long_break_seconds,
                long_break_interval=t.long_break_interval,
            )

    def _apply_theme(self, theme: str):
        """应用浅色/深色主题"""
        app = QApplication.instance()
        if theme == "dark":
            # 深色主题
            palette = QPalette()
            palette.setColor(QPalette.ColorRole.Window, QColor("#1E1E2E"))
            palette.setColor(QPalette.ColorRole.WindowText, QColor("#CDD6F4"))
            palette.setColor(QPalette.ColorRole.Base, QColor("#181825"))
            palette.setColor(QPalette.ColorRole.AlternateBase, QColor("#313244"))
            palette.setColor(QPalette.ColorRole.Button, QColor("#313244"))
            palette.setColor(QPalette.ColorRole.ButtonText, QColor("#CDD6F4"))
            palette.setColor(QPalette.ColorRole.Text, QColor("#CDD6F4"))
            palette.setColor(QPalette.ColorRole.BrightText, QColor("#F38BA8"))
            palette.setColor(QPalette.ColorRole.Highlight, QColor("#89B4FA"))
            palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#1E1E2E"))
            palette.setColor(QPalette.ColorRole.Link, QColor("#89B4FA"))
            app.setPalette(palette)

            self.setStyleSheet("""
                QMainWindow { background: #1E1E2E; }
                QLabel { color: #CDD6F4; }
            """)
        else:
            # 浅色主题（默认）
            palette = QPalette()
            palette.setColor(QPalette.ColorRole.Window, QColor("#F5F6FA"))
            palette.setColor(QPalette.ColorRole.WindowText, QColor("#2C3E50"))
            palette.setColor(QPalette.ColorRole.Base, QColor("#FFFFFF"))
            palette.setColor(QPalette.ColorRole.Button, QColor("#ECF0F1"))
            palette.setColor(QPalette.ColorRole.ButtonText, QColor("#2C3E50"))
            palette.setColor(QPalette.ColorRole.Text, QColor("#2C3E50"))
            palette.setColor(QPalette.ColorRole.Highlight, QColor("#3498DB"))
            palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#FFFFFF"))
            app.setPalette(palette)

            self.setStyleSheet("""
                QMainWindow { background: #F5F6FA; }
            """)

        # 更新窗口标题
        lang = self._settings_manager.settings.language
        t = STRINGS.get(lang, STRINGS["zh"])
        self.setWindowTitle(t.get("window_title", "🍅 番茄钟"))

    def _apply_language(self, lang: str):
        """切换界面语言"""
        t = STRINGS.get(lang, STRINGS["zh"])

        # 侧边栏
        self._sidebar_title.setText(t.get("app_name", "番茄钟"))
        self._sidebar_version.setText(t.get("version", "v1.0.0"))
        for i, key in enumerate(self._nav_keys):
            label = {
                "timer": t.get("nav_timer", "Timer"),
                "stats": t.get("nav_stats", "Stats"),
                "tasks": t.get("nav_tasks", "Tasks"),
                "settings": t.get("nav_settings", "Settings"),
            }[key]
            self._nav_buttons[i].setText(f"{self._nav_icons[i]} {label}")
        self._sidebar_footer.setText(f"🍅 {t.get('footer', 'Focus Every Moment')}")

        # 窗口标题
        self.setWindowTitle(t.get("window_title", "🍅 Tomato Clock"))

        # 子组件语言切换
        self._timer_widget.set_language(lang)
        self._task_widget.set_language(lang)
        # 统计看板通过重建刷新

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
