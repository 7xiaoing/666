"""设置界面组件 — 配置番茄钟参数。"""

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QSpinBox, QComboBox, QCheckBox,
    QScrollArea, QFrame, QGroupBox
)
from PyQt6.QtGui import QFont

from ..models.settings import SettingsManager, TimerSettings, AppSettings


class SettingsSpinRow(QWidget):
    """标签+数值调整行"""

    def __init__(self, label: str, value: int, min_val: int = 1, max_val: int = 60,
                 suffix: str = " 分钟", tooltip: str = ""):
        super().__init__()
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 4, 0, 4)

        lbl = QLabel(label)
        lbl.setStyleSheet("color: #2C3E50; font-size: 14px;")

        self._spin = QSpinBox()
        self._spin.setRange(min_val, max_val)
        self._spin.setValue(value)
        self._spin.setSuffix(suffix)
        self._spin.setFixedWidth(120)
        self._spin.setStyleSheet("""
            QSpinBox {
                padding: 6px 10px;
                border: 1px solid #D5D8DC;
                border-radius: 6px;
                font-size: 13px;
            }
            QSpinBox:focus { border-color: #3498DB; }
        """)

        if tooltip:
            self.setToolTip(tooltip)

        layout.addWidget(lbl)
        layout.addStretch()
        layout.addWidget(self._spin)

    @property
    def value(self) -> int:
        return self._spin.value()


class SettingsWidget(QWidget):
    """设置面板"""

    # 设置变更信号：通知外部应用更新主题、语言等
    settings_changed = pyqtSignal(dict)

    def __init__(self, settings_manager: SettingsManager, parent=None):
        super().__init__(parent)
        self._settings_manager = settings_manager
        self._setup_ui()
        self._load_settings()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(24, 24, 24, 24)

        # ── 标题 ──
        title = QLabel("⚙️ 设置")
        title.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        title.setStyleSheet("color: #2C3E50;")
        layout.addWidget(title)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("QScrollArea { border: none; }")

        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setSpacing(16)

        # ── 计时设置 ──
        timer_group = QGroupBox("⏱️ 番茄钟时长")
        timer_group.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        timer_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                border: 1px solid #E0E0E0;
                border-radius: 12px;
                margin-top: 16px;
                padding: 20px 16px 16px 16px;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                padding: 0 8px;
                color: #2C3E50;
            }
        """)

        timer_layout = QVBoxLayout(timer_group)
        timer_layout.setSpacing(8)

        self._work_spin = SettingsSpinRow("工作时间", 25, 1, 120, " 分钟")
        self._short_break_spin = SettingsSpinRow("短休息时间", 5, 1, 30, " 分钟")
        self._long_break_spin = SettingsSpinRow("长休息时间", 15, 1, 60, " 分钟")
        self._interval_spin = SettingsSpinRow("长休息间隔", 4, 1, 10, " 个番茄")
        self._goal_spin = SettingsSpinRow("每日目标", 12, 1, 50, " 个番茄")

        timer_layout.addWidget(self._work_spin)
        timer_layout.addWidget(self._short_break_spin)
        timer_layout.addWidget(self._long_break_spin)
        timer_layout.addWidget(self._interval_spin)
        timer_layout.addWidget(self._goal_spin)

        scroll_layout.addWidget(timer_group)

        # ── 行为设置 ──
        behavior_group = QGroupBox("🎯 行为选项")
        behavior_group.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        behavior_group.setStyleSheet(timer_group.styleSheet())

        behavior_layout = QVBoxLayout(behavior_group)
        self._auto_break_cb = QCheckBox("完成后自动开始休息")
        self._auto_work_cb = QCheckBox("休息完成后自动开始工作")
        self._tray_cb = QCheckBox("最小化到系统托盘")
        self._notify_cb = QCheckBox("启用桌面通知")
        self._sound_cb = QCheckBox("启用声音提醒")

        for cb in (self._auto_break_cb, self._auto_work_cb, self._tray_cb,
                   self._notify_cb, self._sound_cb):
            cb.setStyleSheet("""
                QCheckBox {
                    color: #2C3E50; font-size: 13px; spacing: 8px;
                    padding: 4px 0;
                }
                QCheckBox::indicator {
                    width: 18px; height: 18px;
                    border: 2px solid #BDC3C7;
                    border-radius: 4px;
                }
                QCheckBox::indicator:checked {
                    background: #3498DB; border-color: #3498DB;
                }
            """)
            behavior_layout.addWidget(cb)

        scroll_layout.addWidget(behavior_group)

        # ── 外观设置 ──
        appearance_group = QGroupBox("🎨 外观")
        appearance_group.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        appearance_group.setStyleSheet(timer_group.styleSheet())

        appearance_layout = QVBoxLayout(appearance_group)

        theme_row = QHBoxLayout()
        theme_row.addWidget(QLabel("主题"))
        theme_row.addStretch()
        self._theme_combo = QComboBox()
        self._theme_combo.addItems(["浅色", "深色"])
        self._theme_combo.setStyleSheet("""
            QComboBox {
                padding: 6px 12px; border: 1px solid #D5D8DC;
                border-radius: 6px; font-size: 13px;
            }
        """)
        theme_row.addWidget(self._theme_combo)
        appearance_layout.addLayout(theme_row)

        lang_row = QHBoxLayout()
        lang_row.addWidget(QLabel("语言"))
        lang_row.addStretch()
        self._lang_combo = QComboBox()
        self._lang_combo.addItems(["中文", "English"])
        self._lang_combo.setStyleSheet(self._theme_combo.styleSheet())
        lang_row.addWidget(self._lang_combo)
        appearance_layout.addLayout(lang_row)

        scroll_layout.addWidget(appearance_group)

        # ── 操作按钮 ──
        btn_layout = QHBoxLayout()
        self._save_btn = QPushButton("💾 保存设置")
        self._reset_btn = QPushButton("↩️ 恢复默认")

        self._save_btn.setStyleSheet("""
            QPushButton {
                background: #2ECC71; color: white;
                border: none; border-radius: 8px;
                padding: 12px 24px; font-size: 14px; font-weight: bold;
            }
            QPushButton:hover { background: #27AE60; }
        """)
        self._reset_btn.setStyleSheet("""
            QPushButton {
                background: #E74C3C; color: white;
                border: none; border-radius: 8px;
                padding: 12px 24px; font-size: 14px; font-weight: bold;
            }
            QPushButton:hover { background: #C0392B; }
        """)

        btn_layout.addStretch()
        btn_layout.addWidget(self._save_btn)
        btn_layout.addWidget(self._reset_btn)
        btn_layout.addStretch()

        scroll_layout.addLayout(btn_layout)
        scroll_layout.addStretch()

        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)

        # ── 连接信号 ──
        self._save_btn.clicked.connect(self._save_settings)
        self._reset_btn.clicked.connect(self._reset_settings)
        # 切换主题/语言时立即生效（不等待保存按钮）
        self._theme_combo.currentIndexChanged.connect(self._apply_preview)
        self._lang_combo.currentIndexChanged.connect(self._apply_preview)

    def _get_current_values(self):
        """获取当前表单中的所有设置值"""
        t = TimerSettings(
            work_duration=self._work_spin.value,
            short_break=self._short_break_spin.value,
            long_break=self._long_break_spin.value,
            long_break_interval=self._interval_spin.value,
            daily_goal=self._goal_spin.value,
            auto_start_break=self._auto_break_cb.isChecked(),
            auto_start_work=self._auto_work_cb.isChecked(),
        )
        s = AppSettings(
            timer=t,
            theme="light" if self._theme_combo.currentIndex() == 0 else "dark",
            language="zh" if self._lang_combo.currentIndex() == 0 else "en",
            minimize_to_tray=self._tray_cb.isChecked(),
            notification_enabled=self._notify_cb.isChecked(),
            sound_enabled=self._sound_cb.isChecked(),
        )
        return t, s

    def _apply_preview(self):
        """主题/语言切换时立即预览效果"""
        _, s = self._get_current_values()
        self.settings_changed.emit({
            "theme": s.theme,
            "language": s.language,
        })

    def _load_settings(self):
        s = self._settings_manager.settings
        t = s.timer

        self._work_spin._spin.setValue(t.work_duration)
        self._short_break_spin._spin.setValue(t.short_break)
        self._long_break_spin._spin.setValue(t.long_break)
        self._interval_spin._spin.setValue(t.long_break_interval)
        self._goal_spin._spin.setValue(t.daily_goal)

        self._auto_break_cb.setChecked(t.auto_start_break)
        self._auto_work_cb.setChecked(t.auto_start_work)
        self._tray_cb.setChecked(s.minimize_to_tray)
        self._notify_cb.setChecked(s.notification_enabled)
        self._sound_cb.setChecked(s.sound_enabled)

        self._theme_combo.setCurrentIndex(0 if s.theme == "light" else 1)
        self._lang_combo.setCurrentIndex(0 if s.language == "zh" else 1)

    def _save_settings(self):
        t, s = self._get_current_values()
        self._settings_manager._settings = s
        self._settings_manager.save()

        # 通知 MainWindow 应用变更
        self.settings_changed.emit({
            "theme": s.theme,
            "language": s.language,
            "timer": t,
        })

        # 反馈
        self._save_btn.setText("✅ 已保存")
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(2000, lambda: self._save_btn.setText("💾 保存设置"))

    def _reset_settings(self):
        self._settings_manager.reset()
        self._load_settings()

        # 通知 MainWindow 恢复默认
        s = self._settings_manager.settings
        self.settings_changed.emit({
            "theme": s.theme,
            "language": s.language,
            "timer": s.timer,
        })

        self._save_btn.setText("↩️ 已重置")
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(2000, lambda: self._save_btn.setText("💾 保存设置"))
