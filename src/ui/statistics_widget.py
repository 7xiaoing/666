"""统计看板界面组件 — 展示番茄钟使用数据。"""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QFrame, QGridLayout, QSizePolicy
)
from PyQt6.QtGui import QFont

from ..models.statistics import StatsManager
from ..i18n import STRINGS


class StatCard(QFrame):
    """统计卡片组件"""

    def __init__(self, title: str, value: str, subtitle: str = "", color: str = "#3498DB"):
        super().__init__()
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setStyleSheet(f"""
            StatCard {{
                background: white;
                border: 1px solid #E8E8E8;
                border-radius: 12px;
                border-top: 3px solid {color};
            }}
        """)
        self.setMinimumHeight(120)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(4)

        title_label = QLabel(title)
        title_label.setStyleSheet(f"color: {color}; font-size: 12px; font-weight: bold; border: none;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        value_label = QLabel(value)
        value_label.setStyleSheet("color: #2C3E50; font-size: 32px; font-weight: bold; border: none;")
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        sub_label = QLabel(subtitle)
        sub_label.setStyleSheet("color: #95A5A6; font-size: 11px; border: none;")
        sub_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(title_label)
        layout.addWidget(value_label)
        layout.addWidget(sub_label)


class DayBar(QFrame):
    """单日柱状图条"""

    def __init__(self, day_label: str, count: int, max_count: int, color: str = "#E74C3C"):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(4)

        # 数值
        count_label = QLabel(str(count))
        count_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        count_label.setStyleSheet("color: #2C3E50; font-size: 11px; font-weight: bold; border: none;")

        # 柱状条
        bar = QFrame()
        bar.setFixedWidth(28)
        height = max(4, int(count / max(max_count, 1) * 120))
        bar.setFixedHeight(height)
        bar.setStyleSheet(f"""
            background: qlineargradient(x1:0, y1:1, x2:0, y2:0,
                stop:0 {color}, stop:1 {color}AA);
            border: none;
            border-radius: 4px;
        """)

        # 日期标签
        day = QLabel(day_label)
        day.setAlignment(Qt.AlignmentFlag.AlignCenter)
        day.setStyleSheet("color: #95A5A6; font-size: 10px; border: none;")

        layout.addStretch()
        layout.addWidget(count_label)
        layout.addWidget(bar, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(day)


class StatisticsWidget(QWidget):
    """统计看板"""

    def __init__(self, stats_manager: StatsManager, parent=None):
        super().__init__(parent)
        self._stats_manager = stats_manager
        self._lang = "zh"
        self._setup_ui()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(24, 24, 24, 24)
        t = STRINGS.get(self._lang, STRINGS["zh"])

        # ── 标题 ──
        title = QLabel(t.get("stats_title", "📊 数据统计"))
        title.setFont(QFont("Segoe UI", 20, QFont.Weight.Bold))
        title.setStyleSheet("color: #2C3E50;")
        layout.addWidget(title)

        # ── 概览卡片 ──
        today = self._stats_manager.get_today_stats()
        weekly = self._stats_manager.get_weekly_stats()
        weekly_total = sum(w.completed_pomodoros for w in weekly)
        stats = self._stats_manager.stats
        unit = t.get("stats_count_unit", "个番茄")
        best = t.get("stats_best", "最高: {}").format(stats.best_streak)

        grid = QGridLayout()
        grid.setSpacing(12)

        self._today_card = StatCard(t.get("stats_today", "今日完成"), str(today.completed_pomodoros), unit, "#E74C3C")
        self._weekly_card = StatCard(t.get("stats_weekly", "本周完成"), str(weekly_total), unit, "#3498DB")
        self._total_card = StatCard(t.get("stats_total", "累计完成"), str(stats.total_pomodoros), unit, "#2ECC71")
        self._streak_card = StatCard(t.get("stats_streak", "连续天数"), str(stats.current_streak), best, "#F39C12")

        grid.addWidget(self._today_card, 0, 0)
        grid.addWidget(self._weekly_card, 0, 1)
        grid.addWidget(self._total_card, 1, 0)
        grid.addWidget(self._streak_card, 1, 1)

        layout.addLayout(grid)

        # ── 本周趋势 ──
        trend_title = QLabel(t.get("stats_weekly_trend", "📈 本周趋势"))
        trend_title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        trend_title.setStyleSheet("color: #2C3E50;")
        layout.addWidget(trend_title)

        chart_frame = QFrame()
        chart_frame.setStyleSheet("""
            background: white; border: 1px solid #E8E8E8;
            border-radius: 12px;
        """)
        chart_frame.setMinimumHeight(200)

        chart_layout = QVBoxLayout(chart_frame)
        chart_layout.setContentsMargins(20, 20, 20, 20)

        bars_layout = QHBoxLayout()
        bars_layout.setSpacing(8)
        bars_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        weekdays = t.get("weekdays", ["一", "二", "三", "四", "五", "六", "日"])
        max_count = max((w.completed_pomodoros for w in weekly), default=1)

        self._bars = []
        for i, day_stats in enumerate(weekly):
            bar = DayBar(weekdays[i], day_stats.completed_pomodoros, max_count)
            self._bars.append(bar)
            bars_layout.addWidget(bar)

        chart_layout.addLayout(bars_layout)
        layout.addWidget(chart_frame)

        # 弹性空间
        layout.addStretch()

    def set_language(self, lang: str):
        """切换语言 — 简单重建界面"""
        self._lang = lang
        # 刷新统计时自动使用新语言
        self.refresh()

    def refresh(self):
        """刷新统计数据"""
