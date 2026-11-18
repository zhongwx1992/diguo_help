"""日常任务时间记录（纯内存）。

所有任务的“上次成功时间”集中存放在一个字典里，方便统一查看和管理。
注意：纯内存实现，进程重启后会清空。
"""

from datetime import datetime

TASK_SHIP = 'ship'          # 跑船
TASK_HONORS = 'honors'      # 领荣誉
TASK_STRENGTH = 'strength'  # 领体力
TASK_STUDY = 'study_art'    # 学习才艺
TASK_BATTLE = 'battle'      # 扫荡战役
TASK_ONLINE = 'online_reward'  # 领取在线奖励
TASK_REBEL_START = 'rebel_start'  # 叛军开始
TASK_REBEL_FULL = 'rebel_full'    # 叛军打满

# 任务名 → 中文名，用于打印状态
_TASK_LABELS = {
    TASK_SHIP: '跑船',
    TASK_HONORS: '领荣誉',
    TASK_STRENGTH: '领体力',
    TASK_STUDY: '学习才艺',
    TASK_BATTLE: '扫荡战役',
    TASK_ONLINE: '在线奖励',
    TASK_REBEL_START: '叛军开始',
    TASK_REBEL_FULL: '叛军打满',
}

# {task_name: datetime} 上一次成功执行的时间
_TASK_TIMES = {}


def _display_width(text):
    """估算字符串在终端中的显示宽度（中文等宽字符按 2 列计）。"""
    return sum(2 if ord(ch) > 127 else 1 for ch in text)


def _human_delta(seconds):
    """把秒数转成易读的“距今多久”。"""
    seconds = int(seconds)
    if seconds < 60:
        return "刚刚"
    if seconds < 3600:
        return f"{seconds // 60}分钟前"
    if seconds < 86400:
        return f"{seconds // 3600}小时{seconds % 3600 // 60}分钟前"
    return f"{seconds // 86400}天前"


def format_status():
    """返回当前所有任务时间的可读状态（多行对齐）。"""
    if not _TASK_TIMES:
        return "  暂无记录"
    now = datetime.now()
    label_width = max(_display_width(label) for label in _TASK_LABELS.values()) + 4
    lines = []
    for task, label in _TASK_LABELS.items():
        ts = _TASK_TIMES.get(task)
        if ts is None:
            value = "未记录"
        else:
            value = f"{ts.strftime('%m-%d %H:%M:%S')}（{_human_delta((now - ts).total_seconds())}）"
        padding = " " * (label_width - _display_width(label))
        lines.append(f"  {label}{padding}{value}")
    return "\n".join(lines)


def print_status(prefix="任务状态"):
    """打印当前任务时间状态。"""
    print(f"【{prefix}】")
    print(format_status())


def get_last_success(task):
    """返回任务上次成功执行的时间（datetime），没有记录返回 None。"""
    return _TASK_TIMES.get(task)


def mark_success(task, when=None):
    """记录任务本次成功执行的时间。"""
    _TASK_TIMES[task] = when or datetime.now()
    print_status("任务时间更新")


def reset(task):
    """清除任务的时间记录，使其下一次不受冷却限制。"""
    if task in _TASK_TIMES:
        _TASK_TIMES.pop(task)
        print_status("任务时间更新")


def can_run(task, cooldown_seconds=None, time_windows=None):
    """
    判断任务当前是否可以执行。

    :param task: 任务名（使用本模块的 TASK_* 常量）
    :param cooldown_seconds: 距上次成功至少间隔的秒数；None 表示不限制
    :param time_windows: 允许执行的时间段列表，如 [(11, 15), (18, 22)]，
                         区间为左闭右开（11:00 <= hour < 15:00）；None 表示不限制
    :return: True 可执行 / False 不可执行
    """
    now = datetime.now()

    if time_windows is not None and not any(start <= now.hour < end for start, end in time_windows):
        print(f"【{task}】当前 {now.strftime('%H:%M')} 不在允许执行的时间段 {time_windows}，跳过")
        return False

    if cooldown_seconds is not None:
        last = get_last_success(task)
        if last is not None:
            elapsed = (now - last).total_seconds()
            if elapsed < cooldown_seconds:
                remaining = int(cooldown_seconds - elapsed)
                print(f"【{task}】距上次成功仅 {int(elapsed)}s，还需等待 {remaining}s，跳过")
                return False

    return True
