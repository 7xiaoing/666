# 番茄钟 — 软件架构设计

## 1. 概述

本文档描述番茄钟（Pomodoro Timer）桌面应用的软件架构。该应用基于 PyQt6 构建，遵循番茄工作法的核心理念，提供计时、任务管理、数据统计等功能。

### 1.1 技术栈

| 层次 | 技术选型 |
|:---|:---|
| UI 框架 | PyQt6 (Qt6) |
| 编程语言 | Python 3.9+ |
| 数据持久化 | JSON 文件 |
| 构建工具 | PyInstaller |
| 样式 | Qt Style Sheets (QSS) |

---

## 2. 整体架构

系统采用 **分层架构** 设计，分为三层：

```
┌─────────────────────────────────────┐
│          UI 表现层 (src/ui/)         │
│  MainWindow │ TimerWidget │ Stats   │
│  TaskWidget │ SettingsWidget        │
├─────────────────────────────────────┤
│          业务逻辑层 (src/)           │
│  PomodoroTimer (状态机引擎)          │
├─────────────────────────────────────┤
│          数据持久层 (src/models/)    │
│  SettingsManager │ StatsManager     │
│  JSON ←──────────→ 磁盘文件         │
└─────────────────────────────────────┘
```

### 2.1 各层职责

| 层次 | 职责 | 关键类 |
|:---|:---|:---|
| UI 表现层 | 用户界面渲染、交互事件处理 | MainWindow, TimerWidget |
| 业务逻辑层 | 计时器核心逻辑、状态管理 | PomodoroTimer |
| 数据持久层 | 配置与统计数据读写 | SettingsManager, StatsManager |

---

## 3. 核心模块设计

### 3.1 计时器引擎 — 有限状态机

计时器核心基于 **有限状态机 (Finite State Machine)** 模型，具有清晰的阶段和状态枚举：

**阶段 (Phase)**:
```
IDLE ─→ WORK ─→ SHORT_BREAK
                ─→ LONG_BREAK
```

**状态 (State)**:
```
STOPPED → RUNNING → PAUSED → RUNNING → STOPPED
```

**状态转移图**:
```
                    pause()
┌────────┐    ┌──────────┐     ┌────────┐
│ RUNNING │───→│  PAUSED  │────→│ RUNNING │
└────────┘    └──────────┘     └────────┘
    │                              ↑
    │ timeout=0                   resume()
    ↓                              │
┌──────────┐                      │
│ STOPPED  │──────────────────────┘
└──────────┘     start_work()
```

### 3.2 信号机制

基于 Qt 的 Signals/Slots 观察者模式：

```
┌──────────────────┐     tick(int)     ┌──────────────┐
│                  │──────────────────→│              │
│  PomodoroTimer   │  phase_changed()  │  TimerWidget  │
│  (Subject)       │──────────────────→│  (Observer)   │
│                  │  state_changed()  │              │
│                  │──────────────────→│              │
│                  │    completed()    │              │
│                  │──────────────────→│  MainWindow   │
└──────────────────┘                   └──────────────┘
```

### 3.3 数据持久化

- **设置文件**: `~/.tomato-clock/settings.json`
- **统计文件**: `~/.tomato-clock/statistics.json`
- **格式**: UTF-8 JSON，支持中文字符
- **策略**: 每次修改即时写盘（write-through）

---

## 4. UI 组件树

```
QApplication
└── MainWindow (QMainWindow)
    ├── Sidebar (QFrame)
    │   ├── Logo + AppName
    │   └── Navigation Buttons × 4
    └── Content (QStackedWidget)
        ├── [0] TimerWidget
        │   ├── PhaseLabel
        │   ├── CircularProgressBar (自定义 QWidget)
        │   ├── TimeLabel
        │   ├── ProgressBar
        │   └── ControlButtons (开始/暂停/停止)
        ├── [1] StatisticsWidget
        │   ├── StatCard × 4
        │   └── 周趋势柱状图
        ├── [2] TaskWidget
        │   ├── 输入栏 + 添加按钮
        │   └── TaskList (TaskItem × N)
        └── [3] SettingsWidget
            ├── 计时设置组
            ├── 行为选项组
            └── 外观设置组
```

---

## 5. 设计模式应用

| 模式 | 应用位置 | 说明 |
|:---|:---|:---|
| **观察者模式** | Qt Signals/Slots | 计时器状态变化通知 UI 更新 |
| **状态模式** | PomodoroTimer | 通过 State/Phase 枚举管理行为 |
| **单例模式** | SettingsManager | 全局唯一配置管理实例 |
| **策略模式** | TimerSettings | 可插拔的计时参数配置 |
| **组合模式** | UI 组件树 | Widget 嵌套组合构建界面 |

---

## 6. 数据流

```
用户操作 → 按钮点击 → Slot 方法
    → PomodoroTimer.方法()
    → Signal 发射
    → UI Widget 更新
    → StatsManager 持久化
```

### 完整番茄流程

```
[开始] → timer.start_work()
    → 每 1s: tick(remaining) 信号 → TimerWidget 更新显示
    → 倒计时归零 → completed("work") 信号
    → MainWindow 接收:
        1. 创建 PomodoroRecord
        2. StatsManager.add_record()
        3. 桌面通知
        4. 自动开始休息（根据设置）
```

---

## 7. 扩展性设计

- **插件式计时时长**: TimerSettings 可动态配置所有时长参数
- **主题切换**: 预留浅色/深色主题接口
- **国际化**: 中英双语资源字符串，可扩展更多语言
- **数据导出**: StatsManager 可扩展 CSV/Excel 导出

---

## 8. 安全性

- 所有数据存储在本地 `~/.tomato-clock/` 目录
- 无网络请求
- 无用户隐私数据收集
