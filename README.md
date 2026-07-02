# 🍅 番茄钟 — Pomodoro Timer

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![PyQt6](https://img.shields.io/badge/PyQt6-6.5+-orange.svg)](https://www.riverbankcomputing.com/software/pyqt/)

> 一款基于 **PyQt6** 构建的桌面番茄工作法计时器。美观、轻量、功能完整。

番茄钟（Pomodoro Timer）是一款遵循弗朗西斯科·西里洛（Francesco Cirillo）番茄工作法原理的桌面应用，帮助用户以 25 分钟专注 + 5 分钟休息的节奏高效工作。

---

## ✨ 功能特性

- ⏱️ **番茄计时器** — 25 分钟工作 / 5 分钟短休息 / 15 分钟长休息
- 📊 **数据统计** — 每日/每周番茄完成数、连续天数、累计数据
- 📋 **任务管理** — 添加任务、标记完成、管理待办
- ⚙️ **自定义设置** — 可调节时长、自动开始、主题色等
- 🔔 **桌面通知** — 番茄完成时系统通知提醒
- 🪟 **系统托盘** — 最小化到托盘，后台运行
- 🌐 **双语支持** — 中文 / English 界面切换

---

## 📸 截图

| 主界面 | 统计看板 | 设置页面 |
|:---:|:---:|:---:|
| `assets/images/timer.png` | `assets/images/stats.png` | `assets/images/settings.png` |

---

## 🚀 快速开始

### 环境要求

- Python 3.9+
- Windows / macOS / Linux

### 安装

```bash
# 1. 克隆仓库
git clone https://github.com/7xiaoing/666.git
cd 666

# 2. 安装依赖
pip install -r requirements.txt

# 3. 运行
python main.py
```

### 打包为单文件

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "番茄钟" main.py
```

---

## 📁 项目结构

```
tomato-clock/
├── main.py                  # 程序入口
├── requirements.txt         # Python 依赖
├── LICENSE                  # MIT 开源许可证
├── README.md                # 项目说明
├── .gitignore               # Git 忽略规则
├── src/                     # 源代码
│   ├── __init__.py
│   ├── timer.py             # 核心计时器（状态机）
│   ├── models/
│   │   ├── settings.py      # 配置管理
│   │   └── statistics.py    # 数据统计
│   └── ui/
│       ├── main_window.py   # 主窗口容器
│       ├── timer_widget.py  # 计时器界面（含圆形进度条）
│       ├── statistics_widget.py  # 统计看板
│       ├── task_widget.py   # 任务管理
│       └── settings_widget.py    # 设置页面
├── assets/                  # 资源文件
│   ├── icons/
│   └── images/
├── docs/                    # 文档
│   ├── architecture.md      # 架构设计
│   └── paper/               # 论文资料
└── tests/                   # 测试
```

---

## 🧠 技术架构

详见 [docs/architecture.md](docs/architecture.md)

- **UI 框架**: PyQt6（Qt6 的 Python 绑定）
- **计时器核心**: 基于状态机模型（QTimer 驱动）
- **数据持久化**: JSON 配置文件
- **设计模式**: 观察者模式（Qt Signals/Slots）

---

## 📖 参考文献与理论依据

本项目的设计基于以下理论基础：

1. **番茄工作法** — Francesco Cirillo, *The Pomodoro Technique*
2. **心流理论** — Mihaly Csikszentmihalyi, *Flow: The Psychology of Optimal Experience*
3. **GTD 方法** — David Allen, *Getting Things Done*
4. **时间管理矩阵** — Stephen Covey, *The 7 Habits of Highly Effective People*

详细参考文献列表参见 [docs/paper/references.md](docs/paper/references.md)

---

## 🤝 贡献指南

欢迎贡献代码、提交 Issue 或改善文档！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

---

## 📄 开源许可

本项目基于 **MIT License** 开源 — 详见 [LICENSE](LICENSE) 文件。

---

## 👤 作者

- **7xiaoing** - 初始开发

---

## 🙏 致谢

- [Francesco Cirillo](https://francescocirillo.com/) — 番茄工作法创始人
- [Qt](https://www.qt.io/) — 跨平台 GUI 框架
- [Riverbank Computing](https://www.riverbankcomputing.com/) — PyQt6

<p align="center">🍅 <strong>专注每一刻</strong> 🍅</p>
