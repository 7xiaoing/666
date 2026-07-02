"""国际化/本地化字符串表 — 支持中文和英文。"""

STRINGS = {
    "zh": {
        # 应用名称
        "app_name": "番茄钟",
        "version": "v1.0.0",

        # 侧边栏导航
        "nav_timer": "计时器",
        "nav_stats": "统计",
        "nav_tasks": "任务",
        "nav_settings": "设置",
        "footer": "专注每一刻",

        # 计时器
        "phase_work": "🍅 工作中",
        "phase_short_break": "☕ 短休息",
        "phase_long_break": "🌴 长休息",
        "phase_idle": "⏳ 准备就绪",
        "today_count": "今日番茄: {}",
        "btn_start": "▶ 开始",
        "btn_pause": "⏸ 暂停",
        "btn_resume": "▶ 继续",
        "btn_stop": "⏹ 停止",

        # 统计
        "stats_title": "📊 数据统计",
        "stats_today": "今日完成",
        "stats_weekly": "本周完成",
        "stats_total": "累计完成",
        "stats_streak": "连续天数",
        "stats_count_unit": "个番茄",
        "stats_best": "最高: {}",
        "stats_weekly_trend": "📈 本周趋势",
        "weekdays": ["一", "二", "三", "四", "五", "六", "日"],

        # 任务
        "task_title": "📋 任务列表",
        "task_placeholder": "输入新任务...",
        "task_add": "＋ 添加",
        "task_empty": "还没有任务，添加一个吧 ✍️",

        # 设置
        "settings_title": "⚙️ 设置",
        "settings_timer": "⏱️ 番茄钟时长",
        "settings_work": "工作时间",
        "settings_short_break": "短休息时间",
        "settings_long_break": "长休息时间",
        "settings_interval": "长休息间隔",
        "settings_goal": "每日目标",
        "settings_behavior": "🎯 行为选项",
        "settings_auto_break": "完成后自动开始休息",
        "settings_auto_work": "休息完成后自动开始工作",
        "settings_tray": "最小化到系统托盘",
        "settings_notify": "启用桌面通知",
        "settings_sound": "启用声音提醒",
        "settings_appearance": "🎨 外观",
        "settings_theme": "主题",
        "settings_language": "语言",
        "theme_light": "浅色",
        "theme_dark": "深色",
        "lang_zh": "中文",
        "lang_en": "English",
        "btn_save": "💾 保存设置",
        "btn_reset": "↩️ 恢复默认",
        "btn_saved": "✅ 已保存",
        "btn_reset_done": "↩️ 已重置",
        "unit_minutes": " 分钟",
        "unit_tomatoes": " 个番茄",

        # 通知
        "notif_completed": "🍅 番茄完成！",
        "notif_completed_msg": "太棒了！该休息一下了 ✨",
        "notif_break_done": "☕ 休息结束",
        "notif_break_msg": "准备开始新的番茄吧！",
        "notif_minimized": "已最小化到托盘，双击恢复",

        # 窗口
        "window_title": "🍅 番茄钟",
    },
    "en": {
        # App
        "app_name": "Tomato Clock",
        "version": "v1.0.0",

        # Sidebar
        "nav_timer": "Timer",
        "nav_stats": "Stats",
        "nav_tasks": "Tasks",
        "nav_settings": "Settings",
        "footer": "Focus Every Moment",

        # Timer
        "phase_work": "🍅 FOCUS",
        "phase_short_break": "☕ Short Break",
        "phase_long_break": "🌴 Long Break",
        "phase_idle": "⏳ Ready",
        "today_count": "Today: {} pomodoros",
        "btn_start": "▶ Start",
        "btn_pause": "⏸ Pause",
        "btn_resume": "▶ Resume",
        "btn_stop": "⏹ Stop",

        # Stats
        "stats_title": "📊 Statistics",
        "stats_today": "Today",
        "stats_weekly": "This Week",
        "stats_total": "Total",
        "stats_streak": "Day Streak",
        "stats_count_unit": "pomodoros",
        "stats_best": "Best: {}",
        "stats_weekly_trend": "📈 Weekly Trend",
        "weekdays": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],

        # Tasks
        "task_title": "📋 Tasks",
        "task_placeholder": "Add a new task...",
        "task_add": "＋ Add",
        "task_empty": "No tasks yet. Add one! ✍️",

        # Settings
        "settings_title": "⚙️ Settings",
        "settings_timer": "⏱️ Timer Duration",
        "settings_work": "Work Duration",
        "settings_short_break": "Short Break",
        "settings_long_break": "Long Break",
        "settings_interval": "Long Break Interval",
        "settings_goal": "Daily Goal",
        "settings_behavior": "🎯 Behavior",
        "settings_auto_break": "Auto-start break after work",
        "settings_auto_work": "Auto-start work after break",
        "settings_tray": "Minimize to system tray",
        "settings_notify": "Enable desktop notifications",
        "settings_sound": "Enable sound alerts",
        "settings_appearance": "🎨 Appearance",
        "settings_theme": "Theme",
        "settings_language": "Language",
        "theme_light": "Light",
        "theme_dark": "Dark",
        "lang_zh": "中文",
        "lang_en": "English",
        "btn_save": "💾 Save",
        "btn_reset": "↩️ Reset",
        "btn_saved": "✅ Saved",
        "btn_reset_done": "↩️ Reset Done",
        "unit_minutes": " min",
        "unit_tomatoes": " pomodoros",

        # Notifications
        "notif_completed": "🍅 Pomodoro Done!",
        "notif_completed_msg": "Great! Time for a break ✨",
        "notif_break_done": "☕ Break Over",
        "notif_break_msg": "Ready for another round!",
        "notif_minimized": "Minimized to tray. Double-click to restore.",

        # Window
        "window_title": "🍅 Tomato Clock",
    },
}
