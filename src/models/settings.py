"""应用配置模型 — 管理番茄钟的持久化设置。"""

import json
import os
from dataclasses import dataclass, asdict
from typing import Optional

CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".tomato-clock")
CONFIG_FILE = os.path.join(CONFIG_DIR, "settings.json")


@dataclass
class TimerSettings:
    """番茄钟计时设置"""
    work_duration: int = 25       # 工作时间（分钟）
    short_break: int = 5          # 短休息时间（分钟）
    long_break: int = 15          # 长休息时间（分钟）
    long_break_interval: int = 4  # 每几个番茄后长休息
    daily_goal: int = 12          # 每日目标番茄数
    auto_start_break: bool = False
    auto_start_work: bool = False

    @property
    def work_seconds(self) -> int:
        return self.work_duration * 60

    @property
    def short_break_seconds(self) -> int:
        return self.short_break * 60

    @property
    def long_break_seconds(self) -> int:
        return self.long_break * 60


@dataclass
class AppSettings:
    """全局应用设置"""
    timer: TimerSettings = None
    theme: str = "light"          # light / dark
    language: str = "zh"          # zh / en
    minimize_to_tray: bool = True
    notification_enabled: bool = True
    sound_enabled: bool = True

    def __post_init__(self):
        if self.timer is None:
            self.timer = TimerSettings()


class SettingsManager:
    """设置管理器 — 负责读写 JSON 配置文件"""

    def __init__(self):
        self._settings: Optional[AppSettings] = None

    @property
    def settings(self) -> AppSettings:
        if self._settings is None:
            self._settings = self._load()
        return self._settings

    def _load(self) -> AppSettings:
        """从磁盘加载设置"""
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                timer_data = data.get("timer", {})
                timer = TimerSettings(**timer_data)
                return AppSettings(timer=timer, **{k: v for k, v in data.items() if k != "timer"})
            except (json.JSONDecodeError, TypeError):
                pass
        return AppSettings()

    def save(self) -> None:
        """保存设置到磁盘"""
        os.makedirs(CONFIG_DIR, exist_ok=True)
        data = asdict(self._settings)
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def reset(self) -> None:
        """恢复出厂设置"""
        self._settings = AppSettings()
        self.save()
