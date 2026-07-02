# 🍅 番茄钟 — Pomodoro Timer

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![PyQt6](https://img.shields.io/badge/PyQt6-6.5+-orange.svg)](https://www.riverbankcomputing.com/software/pyqt/)

> 一款基于 **PyQt6** 构建的桌面番茄工作法计时器。美观、轻量、功能完整。

---

## ✨ 功能特性

| 功能 | 说明 |
|:---|:---|
| ⏱️ **番茄计时器** | 25 分钟工作 / 5 分钟短休息 / 15 分钟长休息，圆形进度动画 |
| 📊 **数据统计** | 每日/每周完成统计、连续天数追踪、累计番茄数 |
| 📋 **任务管理** | 添加/删除任务、标记完成、专注任务关联 |
| ⚙️ **自定义设置** | 可调节各阶段时长、自动开始、主题色、通知开关 |
| 🔔 **桌面通知** | 番茄完成时系统托盘通知提醒 |
| 🪟 **系统托盘** | 最小化到托盘后台运行，双击恢复 |
| 🌐 **双语支持** | 中文 / English 界面切换 |

---

## 🚀 快速开始

```bash
# 1. 克隆仓库
git clone https://github.com/7xiaoing/666.git
cd 666

# 2. 安装依赖
pip install -r requirements.txt

# 3. 运行
python main.py
```

### 打包

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "番茄钟" main.py
```

---

## 📁 项目结构

```
tomato-clock/
├── main.py                  # 程序入口
├── requirements.txt         # 依赖
├── LICENSE                  # MIT 许可证
├── README.md                # 说明文档
├── .gitignore
├── src/                     # 源代码
│   ├── timer.py             # 核心计时器（状态机）
│   ├── models/
│   │   ├── settings.py      # 配置管理
│   │   └── statistics.py    # 数据统计
│   └── ui/
│       ├── main_window.py   # 主窗口
│       ├── timer_widget.py  # 计时器 UI（圆形进度条）
│       ├── statistics_widget.py  # 统计看板
│       ├── task_widget.py   # 任务管理
│       └── settings_widget.py    # 设置页面
├── assets/
│   ├── icons/
│   └── images/
├── docs/
│   ├── architecture.md      # 架构设计文档
│   └── paper/               # 论文资料
└── tests/
```

---

## 🧠 架构设计

详见 [docs/architecture.md](docs/architecture.md)

核心设计：
- **计时器引擎**: 有限状态机（运行→暂停→停止→空闲）
- **信号通信**: PyQt6 Signals/Slots 观察者模式
- **数据层**: JSON 文件持久化
- **UI 层**: QStackedWidget 页面导航

---

## 📖 理论依据

本项目基于以下经典时间管理理论设计：

1. **番茄工作法** — Francesco Cirillo (1992)
2. **心流理论** — Mihaly Csikszentmihalyi
3. **GTD 方法** — David Allen
4. **四象限法则** — Stephen Covey

---

## 📄 开源许可

MIT License — 详见 [LICENSE](LICENSE)

<p align="center">🍅 <strong>专注每一刻</strong> 🍅</p>
