"""任务管理界面组件。"""

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QListWidget, QListWidgetItem,
    QCheckBox, QFrame, QMenu
)
from PyQt6.QtGui import QFont, QAction

from ..i18n import STRINGS


class TaskItem(QFrame):
    """单个任务项目"""

    def __init__(self, text: str, completed: bool = False, parent=None):
        super().__init__(parent)
        self._completed = completed
        self._text = text

        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setStyleSheet("""
            TaskItem {
                background: white;
                border: 1px solid #ECF0F1;
                border-radius: 8px;
                padding: 4px;
            }
            TaskItem:hover {
                border-color: #3498DB;
            }
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)

        self._checkbox = QCheckBox()
        self._checkbox.setChecked(completed)
        self._checkbox.setStyleSheet("""
            QCheckBox::indicator {
                width: 20px; height: 20px;
                border: 2px solid #BDC3C7;
                border-radius: 10px;
            }
            QCheckBox::indicator:checked {
                background: #2ECC71;
                border-color: #2ECC71;
            }
        """)

        self._text_label = QLabel(text)
        self._text_label.setFont(QFont("Segoe UI", 12))
        if completed:
            self._text_label.setStyleSheet("color: #95A5A6; text-decoration: line-through; border: none;")
        else:
            self._text_label.setStyleSheet("color: #2C3E50; border: none;")

        self._delete_btn = QPushButton("✕")
        self._delete_btn.setFixedSize(24, 24)
        self._delete_btn.setStyleSheet("""
            QPushButton {
                background: transparent; color: #BDC3C7;
                border: none; font-size: 14px;
            }
            QPushButton:hover { color: #E74C3C; }
        """)

        layout.addWidget(self._checkbox)
        layout.addWidget(self._text_label)
        layout.addStretch()
        layout.addWidget(self._delete_btn)

        self._checkbox.toggled.connect(self._on_toggle)

    def _on_toggle(self, checked: bool):
        self._completed = checked
        if checked:
            self._text_label.setStyleSheet("color: #95A5A6; text-decoration: line-through; border: none;")
        else:
            self._text_label.setStyleSheet("color: #2C3E50; border: none;")

    @property
    def is_completed(self) -> bool:
        return self._completed

    @property
    def task_text(self) -> str:
        return self._text


class TaskWidget(QWidget):
    """任务列表面板"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._tasks: list[TaskItem] = []
        self._lang = "zh"
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(16)
        layout.setContentsMargins(24, 24, 24, 24)
        t = STRINGS.get(self._lang, STRINGS["zh"])

        # ── 标题 ──
        self._task_title = QLabel(t.get("task_title", "📋 任务列表"))
        self._task_title.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        self._task_title.setStyleSheet("color: #2C3E50;")
        layout.addWidget(self._task_title)

        # ── 输入区域 ──
        input_layout = QHBoxLayout()
        self._input_field = QLineEdit()
        self._input_field.setPlaceholderText(t.get("task_placeholder", "输入新任务..."))
        self._input_field.setStyleSheet("""
            QLineEdit {
                padding: 10px 16px;
                border: 2px solid #E0E0E0;
                border-radius: 8px;
                font-size: 14px;
                background: white;
            }
            QLineEdit:focus {
                border-color: #3498DB;
            }
        """)

        self._add_btn = QPushButton(t.get("task_add", "＋ 添加"))
        self._add_btn.setStyleSheet("""
            QPushButton {
                background: #3498DB; color: white;
                border: none; border-radius: 8px;
                padding: 10px 20px;
                font-size: 14px; font-weight: bold;
            }
            QPushButton:hover { background: #2980B9; }
        """)

        input_layout.addWidget(self._input_field)
        input_layout.addWidget(self._add_btn)
        layout.addLayout(input_layout)

        # ── 任务列表容器 ──
        self._task_container = QVBoxLayout()
        self._task_container.setSpacing(6)
        layout.addLayout(self._task_container)

        # ── 空状态 ──
        self._empty_label = QLabel(t.get("task_empty", "还没有任务，添加一个吧 ✍️"))
        self._empty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._empty_label.setStyleSheet("color: #BDC3C7; font-size: 14px; padding: 40px;")
        layout.addWidget(self._empty_label)

        layout.addStretch()

        # ── 连接信号 ──
        self._add_btn.clicked.connect(self._add_task)
        self._input_field.returnPressed.connect(self._add_task)

    def _add_task(self):
        text = self._input_field.text().strip()
        if not text:
            return

        item = TaskItem(text)
        self._tasks.append(item)
        self._task_container.addWidget(item)
        self._input_field.clear()
        self._empty_label.hide()

        # 连接删除按钮
        item.findChildren(QPushButton)[0].clicked.connect(
            lambda: self._remove_task(item)
        )

    def _remove_task(self, item: TaskItem):
        self._tasks.remove(item)
        self._task_container.removeWidget(item)
        item.deleteLater()
        if not self._tasks:
            self._empty_label.show()

    def get_active_tasks(self) -> list[str]:
        return [t.task_text for t in self._tasks if not t.is_completed]

    def clear_completed(self):
        to_remove = [t for t in self._tasks if t.is_completed]
        for item in to_remove:
            self._remove_task(item)

    def set_language(self, lang: str):
        """切换语言"""
        self._lang = lang
        t = STRINGS.get(lang, STRINGS["zh"])
        self._task_title.setText(t.get("task_title", "📋 任务列表"))
        self._input_field.setPlaceholderText(t.get("task_placeholder", "输入新任务..."))
        self._add_btn.setText(t.get("task_add", "＋ 添加"))
        self._empty_label.setText(t.get("task_empty", "还没有任务，添加一个吧 ✍️"))
