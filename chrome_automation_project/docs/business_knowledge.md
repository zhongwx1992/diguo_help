# 帝国助手业务知识沉淀

> 本文档记录日常任务相关的业务规则、实现特点和已知限制，便于后续迭代时快速了解上下文。
> 代码位置默认指 `chrome_automation_project/` 目录。

## 1. 日常任务总体机制

### 1.1 统一入口
- 入口函数：`main.py` 中的 `_run_daily_tasks()`。
- 执行顺序固定为：
  1. 跑船 `get_dock_order`
  2. 领在线奖励 `get_online_reward`
  3. 领荣誉 `get_free_honors`
  4. 学习才艺 `get_study_art`
  5. 领体力 `get_strength`
  6. 扫荡战役 `get_every_battle`
- 每个任务独立 `try/except`，任一失败不影响其他任务。
- 顺序上「领体力」在「扫荡战役」之前，因此体力领取成功会刷新扫荡冷却，同一轮即可扫荡。

### 1.2 执行节奏
- `_run_daily_tasks()` 本身不控制间隔，由外层循环控制。
- 配置项 `ship_interval` 控制日常任务最小执行间隔，`role_config.py` 中默认 `23 * 60`（约 23 分钟）。
- 三种触发场景：
  - 挂机阶段：跑完一轮 `sleep(ship_interval)`。
  - 叛军阶段：距上次执行 `>= ship_interval` 才触发。
  - 纯日常循环（`is_attack_rebel=False`）：首次用 `last_run_time` 对齐节奏，之后每轮 `sleep(interval)`。

### 1.3 程序启动与退出
- 启动后先执行一次日常任务，再进入循环。
- 退出条件：
  - 检测到「返回登录」界面：`login_service.return_login_exit()` 中 `sys.exit(0)`。
  - 手动退出：`Ctrl+C`，由两处 `KeyboardInterrupt` 捕获。
- 每次退出前会调用 `print_status("程序退出前任务状态")` 打印任务时间状态。

## 2. 任务时间管理 `task_timer.py`

### 2.1 设计
- **纯内存**字典 `{task_name: datetime}`，进程重启后清空。
- 因此首次运行天然不受冷却限制（记录为空），但时间窗仍然生效。
- 副作用：中途重启会丢失冷却记录，同一天可能重复执行已冷却任务。

### 2.2 任务常量
| 常量 | 值 | 含义 |
|---|---|---|
| `TASK_SHIP` | `ship` | 跑船 |
| `TASK_HONORS` | `honors` | 领荣誉 |
| `TASK_STRENGTH` | `strength` | 领体力 |
| `TASK_STUDY` | `study_art` | 学习才艺 |
| `TASK_BATTLE` | `battle` | 扫荡战役 |
| `TASK_ONLINE` | `online_reward` | 在线奖励 |
| `TASK_REBEL_START` | `rebel_start` | 叛军开始 |
| `TASK_REBEL_FULL` | `rebel_full` | 叛军打满 |

### 2.3 核心接口
- `can_run(task, cooldown_seconds=None, time_windows=None) -> bool`
  - 先判断时间窗，再判断冷却。
  - `time_windows` 左闭右开，例如 `[(11,15),(18,22)]` 表示 `11:00 <= hour < 15:00`，故 `15:00`、`22:00` 整点不执行。
- `mark_success(task)`：记录成功时间，并打印任务状态。
- `reset(task)`：清除记录，使下一次不受冷却限制。
- `get_last_success(task)`：读取上次成功时间。
- `print_status(prefix)` / `format_status()`：打印/格式化全部任务时间状态。

## 3. 各任务特点

### 3.1 跑船 `get_dock_order`
- 冷却：无（交给外层 `ship_interval` 控制）。
- 记录：仅在流程正常结束时 `mark_success(TASK_SHIP)`。
- 特点：需要先在城市中找到船坞，找不到会拖动重试；图纸用完或资源不足会提前结束。
- 说明：跑船即使未完成订单也会记录时间，当前视为符合预期。

### 3.2 在线奖励 `get_online_reward`
- 冷却：无。
- 记录：成功领取后 `mark_success(TASK_ONLINE)`。
- 特点：没有在线奖励时返回 `False`，不记录。

### 3.3 领荣誉 `get_free_honors`
- 冷却：1 小时（`cooldown_seconds=3600`）。
- 记录：成功领取后 `mark_success(TASK_HONORS)`。
- 可选消费：`buy_bamboo_slip`（8000 荣誉买断简）、`buy_red_book_debris`（13000 荣誉买红书碎片）。
- 特点：进入城市 → 图书馆 → 书店 → 购买/免费领取；支持广告免费刷新。

### 3.4 学习才艺 `get_study_art`
- 冷却：1 小时 5 分钟（`65 * 60` 秒）。
- 记录：**只有实际学习到至少一个才艺**才 `mark_success(TASK_STUDY)`；如果所有房间都在学习中或没有可用按钮，则不记录冷却，返回 `False`。
- 房间：琴室、棋室、书房、画廊，支持传入单个或多个。
- 流程：进城 → 宫殿 → 才艺坊 → 领取已完成结果 → 逐个房间「快速选择」→ 确认学习 → 退出。

### 3.5 领体力 `get_strength`
- 冷却：2 小时。
- 时间窗：`11:00-15:00`、`18:00-22:00`（左闭右开）。
- 业务规则：每个时间段只有一次免费领取机会。
- 记录：仅当找到体力入口且存在「免费领取」按钮时才 `mark_success(TASK_STRENGTH)`，并 `reset(TASK_BATTLE)` 刷新扫荡冷却。
- 未找到入口或没有免费按钮时：退出福利界面，返回 `0`，不占用冷却。

### 3.6 扫荡战役 `get_every_battle`
- 冷却：2 小时。
- 联动：领体力成功后立即清除其冷却，可马上扫荡。
- 记录：只有当本次确实完成扫荡（未直接弹出购买体力界面）时才 `mark_success(TASK_BATTLE)`；一开始就没体力则不记录，返回 `0`。
- 特点：会循环扫荡直到体力不足（最多 4 次），然后退出体力购买界面。

### 3.7 叛军
- 记录：`TASK_REBEL_START`（当天开始）与 `TASK_REBEL_FULL`（当天打满），均按日期每天只记一次。
- 打满判定：连续取消攻击叛军 10 次（`REBEL_ATTACKED_CANCAL_NUMBER >= 10`）即判定打满，进入挂机阶段。
- 跨天：检测到日期变化后重置连续取消计数，重新进入打叛军阶段。
- 注意：纯内存记录，重启后当天会重新记录「叛军开始」。

## 4. 已知限制

1. 时间记录为纯内存，重启清零；这是当前有意选择的行为。
2. 「成功」以流程完成/关键界面检测为准，不做服务端结果校验。
3. 体力与扫荡的联动只能保证「体力领取成功后放行扫荡」，若扫荡自身无体力则不会记录冷却。
4. 部分 OCR/图像识别依赖屏幕状态，识别失败可能被判定为「未找到入口」而跳过，不记录冷却。

## 5. 主要配置项

| 配置 | 位置 | 说明 |
|---|---|---|
| `ship_interval` | `role_config.py` | 日常任务执行间隔（秒），默认 `23 * 60` |
| `study_active` / `study_type` | `role_config.py` | 是否学习才艺及房间列表 |
| `buy_bamboo_slip` / `buy_red_book_debris` | `role_config.py` | 荣誉消费开关 |
| `is_active` | `role_config.py` | 是否执行跑船 |

## 6. 变更记录

- 新增 `task_timer.py`，统一记录日常任务时间（纯内存）并支持冷却/时间窗判断。
- 各任务接入冷却：荣誉 1h、体力 2h（+时间窗）、扫荡 2h、才艺 65min；跑船/在线奖励仅记录。
- 体力领取成功会刷新扫荡冷却。
- 修复「假成功」：才艺未实际学习、扫荡无体力、体力无可领取入口时不再记录冷却。
- 新增任务状态打印与退出前状态汇总。
- 新增叛军开始/打满时间记录。
