"""番茄钟核心计时器逻辑 — 基于状态机模型实现。"""

from enum import Enum, auto
from typing import Callable, Optional
from PyQt6.QtCore import QTimer, QObject, pyqtSignal


class TimerPhase(Enum):
    """计时器阶段"""
    WORK = auto()         # 工作时间
    SHORT_BREAK = auto()  # 短休息
    LONG_BREAK = auto()   # 长休息
    IDLE = auto()         # 空闲/停止


class TimerState(Enum):
    """计时器状态"""
    RUNNING = auto()
    PAUSED = auto()
    STOPPED = auto()


class PomodoroTimer(QObject):
    """番茄钟计时器核心类

    基于状态机设计：
      IDLE → RUNNING → PAUSED → RUNNING → ... → STOPPED → IDLE

    信号:
      tick(int): 每秒触发，传出剩余秒数
      phase_changed(TimerPhase): 阶段切换时触发
      state_changed(TimerState): 状态切换时触发
      completed(str): 一个番茄完成时触发
    """

    tick = pyqtSignal(int)
    phase_changed = pyqtSignal(TimerPhase)
    state_changed = pyqtSignal(TimerState)
    completed = pyqtSignal(str)  # 阶段名称

    def __init__(self, work_sec: int = 1500, short_break_sec: int = 300,
                 long_break_sec: int = 900, long_break_interval: int = 4):
        super().__init__()
        self._work_sec = work_sec
        self._short_break_sec = short_break_sec
        self._long_break_sec = long_break_sec
        self._long_break_interval = long_break_interval

        self._phase: TimerPhase = TimerPhase.IDLE
        self._state: TimerState = TimerState.STOPPED
        self._remaining: int = 0
        self._total: int = 0
        self._completed_count: int = 0

        self._qtimer = QTimer(self)
        self._qtimer.timeout.connect(self._on_tick)
        self._qtimer.setInterval(1000)

    # ── 属性 ──────────────────────────────────────────

    @property
    def phase(self) -> TimerPhase:
        return self._phase

    @property
    def state(self) -> TimerState:
        return self._state

    @property
    def remaining(self) -> int:
        return self._remaining

    @property
    def total(self) -> int:
        return self._total

    @property
    def elapsed(self) -> int:
        return self._total - self._remaining

    @property
    def progress(self) -> float:
        """返回 0.0 ~ 1.0 的进度"""
        if self._total == 0:
            return 0.0
        return 1.0 - (self._remaining / self._total)

    @property
    def completed_count(self) -> int:
        return self._completed_count

    # ── 配置 ──────────────────────────────────────────

    def configure(self, work_sec: int, short_break_sec: int,
                  long_break_sec: int, long_break_interval: int) -> None:
        self._work_sec = work_sec
        self._short_break_sec = short_break_sec
        self._long_break_sec = long_break_sec
        self._long_break_interval = long_break_interval

    # ── 控制方法 ──────────────────────────────────────

    def start_work(self) -> None:
        """开始一个工作番茄"""
        self._phase = TimerPhase.WORK
        self._total = self._work_sec
        self._remaining = self._total
        self._state = TimerState.RUNNING
        self._qtimer.start()
        self.phase_changed.emit(self._phase)
        self.state_changed.emit(self._state)
        self.tick.emit(self._remaining)

    def start_break(self) -> None:
        """开始休息"""
        self._completed_count += 1
        if self._completed_count % self._long_break_interval == 0:
            self._phase = TimerPhase.LONG_BREAK
            self._total = self._long_break_sec
        else:
            self._phase = TimerPhase.SHORT_BREAK
            self._total = self._short_break_sec
        self._remaining = self._total
        self._state = TimerState.RUNNING
        self._qtimer.start()
        self.phase_changed.emit(self._phase)
        self.state_changed.emit(self._state)
        self.tick.emit(self._remaining)

    def pause(self) -> None:
        """暂停计时"""
        if self._state == TimerState.RUNNING:
            self._state = TimerState.PAUSED
            self._qtimer.stop()
            self.state_changed.emit(self._state)

    def resume(self) -> None:
        """恢复计时"""
        if self._state == TimerState.PAUSED:
            self._state = TimerState.RUNNING
            self._qtimer.start()
            self.state_changed.emit(self._state)

    def stop(self) -> None:
        """停止计时"""
        self._qtimer.stop()
        self._state = TimerState.STOPPED
        self._phase = TimerPhase.IDLE
        self._remaining = 0
        self.state_changed.emit(self._state)
        self.phase_changed.emit(self._phase)

    def toggle_pause(self) -> None:
        """切换暂停/继续"""
        if self._state == TimerState.RUNNING:
            self.pause()
        elif self._state == TimerState.PAUSED:
            self.resume()

    def reset(self) -> None:
        """重置为初始状态"""
        self.stop()
        self._completed_count = 0

    # ── 内部 ──────────────────────────────────────────

    def _on_tick(self) -> None:
        """每秒回调"""
        self._remaining -= 1
        self.tick.emit(self._remaining)

        if self._remaining <= 0:
            self._qtimer.stop()
            self._state = TimerState.STOPPED
            self.state_changed.emit(self._state)

            if self._phase == TimerPhase.WORK:
                phase_name = "work"
                self.completed.emit(phase_name)
            elif self._phase in (TimerPhase.SHORT_BREAK, TimerPhase.LONG_BREAK):
                phase_name = "break"
                self.completed.emit(phase_name)
