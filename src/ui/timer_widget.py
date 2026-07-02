"""番茄钟主计时器界面组件。"""

from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QProgressBar, QFrame
)
from PyQt6.QtGui import QFont, QPainter, QColor, QBrush, QPen, QConicalGradient

from ..timer import PomodoroTimer, TimerPhase, TimerState


class CircularProgressBar(QWidget):
    """圆形进度条控件"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self._progress = 0.0
        self._phase_color = QColor("#E74C3C")
        self.setMinimumSize(280, 280)

    def set_progress(self, value: float):
        self._progress = max(0.0, min(1.0, value))
        self.update()

    def set_phase_color(self, color: QColor):
        self._phase_color = color
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect()
        side = min(rect.width(), rect.height())
        painter.translate(rect.center())
        painter.scale(side / 280.0, side / 280.0)

        # 背景圆环
        pen = QPen(QColor("#E0E0E0"), 8)
        painter.setPen(pen)
        painter.drawArc(-125, -125, 250, 250, 0, 360 * 16)

        # 进度圆环
        if self._progress > 0:
            gradient = QConicalGradient(0, 0, -90)
            gradient.setColorAt(0.0, self._phase_color)
            gradient.setColorAt(1.0, self._phase_color.lighter(130))
            pen = QPen(QBrush(gradient), 8)
            pen.setCapStyle(Qt.PenCapStyle.RoundCap)
            painter.setPen(pen)
            span = int(self._progress * 360 * 16)
            painter.drawArc(-125, -125, 250, 250, 90 * 16, -span)

        painter.end()


class TimerWidget(QWidget):
    """计时器主界面部件"""

    PHASE_COLORS = {
        TimerPhase.WORK: QColor("#E74C3C"),        # 红色 — 紧张工作
        TimerPhase.SHORT_BREAK: QColor("#2ECC71"),  # 绿色 — 放松休息
        TimerPhase.LONG_BREAK: QColor("#3498DB"),   # 蓝色 — 长休息
        TimerPhase.IDLE: QColor("#95A5A6"),          # 灰色 — 空闲
    }

    PHASE_LABELS = {
        TimerPhase.WORK: "🍅 工作中",
        TimerPhase.SHORT_BREAK: "☕ 短休息",
        TimerPhase.LONG_BREAK: "🌴 长休息",
        TimerPhase.IDLE: "⏳ 准备就绪",
    }

    def __init__(self, timer: PomodoroTimer, parent=None):
        super().__init__(parent)
        self._timer = timer
        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)

        # ── 阶段标签 ──
        self._phase_label = QLabel(self.PHASE_LABELS[TimerPhase.IDLE])
        self._phase_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont("Segoe UI", 18)
        self._phase_label.setFont(font)
        self._phase_label.setStyleSheet("color: #7F8C8D;")

        # ── 圆形进度 + 时间显示 ──
        self._circular_progress = CircularProgressBar()
        container = QHBoxLayout()
        container.addStretch()
        container.addWidget(self._circular_progress)
        container.addStretch()

        self._time_label = QLabel("25:00")
        self._time_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont("Segoe UI", 56, QFont.Weight.Light)
        self._time_label.setFont(font)
        self._time_label.setStyleSheet("color: #2C3E50;")
        # 将时间标签叠加在圆形进度条上
        self._time_label.setParent(self._circular_progress)
        self._time_label.setGeometry(0, 90, 280, 100)
        self._time_label.raise_()

        # 进度条
        self._progress_bar = QProgressBar()
        self._progress_bar.setRange(0, 100)
        self._progress_bar.setValue(0)
        self._progress_bar.setFixedHeight(4)
        self._progress_bar.setTextVisible(False)
        self._progress_bar.setStyleSheet("""
            QProgressBar {
                background: #ECF0F1;
                border: none;
                border-radius: 2px;
            }
            QProgressBar::chunk {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #E74C3C, stop:1 #C0392B);
                border-radius: 2px;
            }
        """)

        # ── 番茄计数 ──
        self._count_label = QLabel("今日番茄: 0")
        self._count_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._count_label.setStyleSheet("color: #95A5A6; font-size: 13px;")

        # ── 控制按钮 ──
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(16)

        self._start_btn = QPushButton("▶ 开始")
        self._pause_btn = QPushButton("⏸ 暂停")
        self._stop_btn = QPushButton("⏹ 停止")

        for btn in (self._start_btn, self._pause_btn, self._stop_btn):
            btn.setFixedSize(120, 42)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)

        self._start_btn.setStyleSheet("""
            QPushButton {
                background: #E74C3C; color: white; border: none;
                border-radius: 21px; font-size: 15px; font-weight: bold;
            }
            QPushButton:hover { background: #C0392B; }
        """)
        self._pause_btn.setStyleSheet("""
            QPushButton {
                background: #F39C12; color: white; border: none;
                border-radius: 21px; font-size: 15px; font-weight: bold;
            }
            QPushButton:hover { background: #D68910; }
        """)
        self._stop_btn.setStyleSheet("""
            QPushButton {
                background: #95A5A6; color: white; border: none;
                border-radius: 21px; font-size: 15px; font-weight: bold;
            }
            QPushButton:hover { background: #7F8C8D; }
        """)

        btn_layout.addStretch()
        btn_layout.addWidget(self._start_btn)
        btn_layout.addWidget(self._pause_btn)
        btn_layout.addWidget(self._stop_btn)
        btn_layout.addStretch()

        # ── 组装 ──
        layout.addStretch()
        layout.addWidget(self._phase_label)
        layout.addSpacing(10)
        layout.addLayout(container)
        layout.addWidget(self._progress_bar)
        layout.addWidget(self._count_label)
        layout.addSpacing(10)
        layout.addLayout(btn_layout)
        layout.addStretch()

        # 按钮状态
        self._pause_btn.setEnabled(False)
        self._stop_btn.setEnabled(False)

    def _connect_signals(self):
        self._start_btn.clicked.connect(self._on_start)
        self._pause_btn.clicked.connect(self._on_pause_resume)
        self._stop_btn.clicked.connect(self._on_stop)

        self._timer.tick.connect(self._on_tick)
        self._timer.phase_changed.connect(self._on_phase_changed)
        self._timer.state_changed.connect(self._on_state_changed)

    def _format_time(self, seconds: int) -> str:
        m = seconds // 60
        s = seconds % 60
        return f"{m:02d}:{s:02d}"

    def _on_start(self):
        if self._timer.state == TimerState.STOPPED:
            self._timer.start_work()

    def _on_pause_resume(self):
        self._timer.toggle_pause()

    def _on_stop(self):
        self._timer.stop()

    def _on_tick(self, remaining: int):
        self._time_label.setText(self._format_time(remaining))
        self._circular_progress.set_progress(self._timer.progress)
        self._progress_bar.setValue(int(self._timer.progress * 100))

    def _on_phase_changed(self, phase: TimerPhase):
        color = self.PHASE_COLORS.get(phase, QColor("#95A5A6"))
        self._circular_progress.set_phase_color(color)
        self._phase_label.setText(self.PHASE_LABELS.get(phase, ""))
        self._phase_label.setStyleSheet(f"color: {color.name()};")

        if phase == TimerPhase.IDLE:
            self._time_label.setText("25:00")
            self._circular_progress.set_progress(0)
            self._progress_bar.setValue(0)

    def _on_state_changed(self, state: TimerState):
        if state == TimerState.RUNNING:
            self._start_btn.setEnabled(False)
            self._pause_btn.setEnabled(True)
            self._pause_btn.setText("⏸ 暂停")
            self._stop_btn.setEnabled(True)
        elif state == TimerState.PAUSED:
            self._pause_btn.setText("▶ 继续")
        elif state == TimerState.STOPPED:
            self._start_btn.setEnabled(True)
            self._pause_btn.setEnabled(False)
            self._stop_btn.setEnabled(False)
            self._pause_btn.setText("⏸ 暂停")

    def update_count(self, count: int):
        self._count_label.setText(f"🍅 今日番茄: {count}")
