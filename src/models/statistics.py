"""统计数据模型 — 追踪番茄钟使用数据。"""

import json
import os
from dataclasses import dataclass, asdict, field
from datetime import datetime, date
from typing import Optional

STATS_DIR = os.path.join(os.path.expanduser("~"), ".tomato-clock")
STATS_FILE = os.path.join(STATS_DIR, "statistics.json")


@dataclass
class PomodoroRecord:
    """单个番茄记录"""
    id: str = ""
    task_name: str = ""
    duration: int = 1500          # 实际持续时间（秒）
    completed: bool = True
    timestamp: str = ""           # ISO 格式时间戳
    tags: list = field(default_factory=list)

    def __post_init__(self):
        if not self.id:
            from uuid import uuid4
            self.id = str(uuid4())[:8]
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()

    @property
    def date(self) -> date:
        return datetime.fromisoformat(self.timestamp).date()

    @property
    def date_str(self) -> str:
        return self.date.isoformat()


@dataclass
class DailyStats:
    """每日统计"""
    date: str = ""                # YYYY-MM-DD
    completed_pomodoros: int = 0
    interrupted_pomodoros: int = 0
    total_focus_seconds: int = 0
    tasks_completed: int = 0

    @property
    def total_focus_minutes(self) -> float:
        return round(self.total_focus_seconds / 60, 1)


@dataclass
class Statistics:
    """完整统计数据"""
    records: list = field(default_factory=list)
    total_pomodoros: int = 0
    current_streak: int = 0
    best_streak: int = 0
    last_updated: str = ""


class StatsManager:
    """统计管理器"""

    def __init__(self):
        self._stats: Optional[Statistics] = None

    @property
    def stats(self) -> Statistics:
        if self._stats is None:
            self._stats = self._load()
        return self._stats

    def _load(self) -> Statistics:
        if os.path.exists(STATS_FILE):
            try:
                with open(STATS_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                records = [PomodoroRecord(**r) for r in data.get("records", [])]
                return Statistics(records=records, **{k: v for k, v in data.items() if k != "records"})
            except (json.JSONDecodeError, TypeError):
                pass
        return Statistics()

    def save(self) -> None:
        os.makedirs(STATS_DIR, exist_ok=True)
        data = asdict(self.stats)
        data["records"] = [asdict(r) for r in self.stats.records]
        with open(STATS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def add_record(self, record: PomodoroRecord) -> None:
        """添加一条番茄记录"""
        self.stats.records.append(record)
        self.stats.total_pomodoros += 1
        self.stats.last_updated = datetime.now().isoformat()
        self._update_streaks()
        self.save()

    def _update_streaks(self) -> None:
        """更新连续天数统计"""
        dates = sorted(set(r.date_str for r in self.stats.records if r.completed), reverse=True)
        if not dates:
            return

        from datetime import timedelta
        current = datetime.strptime(dates[0], "%Y-%m-%d").date()
        streak = 0

        for d in dates:
            d_date = datetime.strptime(d, "%Y-%m-%d").date()
            if d_date == current:
                streak += 1
                current -= timedelta(days=1)
            elif d_date < current:
                break

        self.stats.current_streak = streak
        self.stats.best_streak = max(self.stats.best_streak, streak)

    def get_today_stats(self) -> DailyStats:
        """获取今日统计"""
        today = date.today().isoformat()
        today_records = [r for r in self.stats.records if r.date_str == today]
        completed = [r for r in today_records if r.completed]
        return DailyStats(
            date=today,
            completed_pomodoros=len(completed),
            interrupted_pomodoros=len(today_records) - len(completed),
            total_focus_seconds=sum(r.duration for r in completed),
        )

    def get_weekly_stats(self) -> list[DailyStats]:
        """获取本周每日统计"""
        from datetime import timedelta
        today = date.today()
        week = []
        for i in range(6, -1, -1):
            d = (today - timedelta(days=i)).isoformat()
            records = [r for r in self.stats.records if r.date_str == d]
            completed = [r for r in records if r.completed]
            week.append(DailyStats(
                date=d,
                completed_pomodoros=len(completed),
                interrupted_pomodoros=len(records) - len(completed),
                total_focus_seconds=sum(r.duration for r in completed),
            ))
        return week
