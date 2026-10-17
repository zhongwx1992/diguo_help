# 帝国网页版自动化辅助工具 🎮

基于 Python + PyAutoGUI + OpenCV + PaddleOCR 的网页游戏自动化脚本，通过图像识别和 OCR 实现自动刷叛军、船坞运输、在线奖励、荣誉领取、才艺学习等功能。

## 功能特性

| 功能 | 说明 |
|------|------|
| ⚔️ 自动刷叛军 | 按指定等级在屏幕范围内搜索攻击，找不到自动拖动地图换方向 |
| 🎯 连续取消检测 | 连续取消攻击 20 次自动告警 |
| ⛵ 船坞运输 | 定时执行船坞订单，自动寻找船坞并填满所有坑位 |
| 🎁 在线奖励 | 自动领取在线奖励，支持双倍领取弹窗 |
| 📚 荣誉领取 | 自动进入图书馆购买荣誉书籍，支持广告免费刷新 |
| 🎨 才艺学习 | 支持同时学习多个才艺（琴室/棋室/书房/画廊），自动领取学习结果 |
| 🏰 城池重建 | 检测城池被攻击时自动重建主城 |
| 🔐 登录状态监控 | 挂机循环每轮检测登录状态，登出自动退出 |
| 🕐 日常任务调度 | 启动先执行一次，之后按 `ship_interval`（默认 20min）定时触发 |
| 👥 多角色配置 | `ROLE_CONFIG` 配置驱动，切换角色改一行即可 |
| 🔍 OCR 文字识别 | PaddleOCR 屏幕文字识别，支持标定任意区域坐标 |

## 技术栈

| 依赖 | 用途 |
|------|------|
| **Python 3.11** | 运行环境 |
| [PyAutoGUI](https://pyautogui.readthedocs.io/) | 屏幕截图、图像定位、鼠标键盘自动化 |
| [OpenCV](https://pypi.org/project/opencv-python/) | 图像匹配（`confidence` 参数需要） |
| [PaddleOCR](https://github.com/PaddlePaddle/PaddleOCR) | 屏幕文字识别（中文/数字） |
| [PaddlePaddle](https://www.paddlepaddle.org.cn/) | PaddleOCR 推理引擎 |
| [screeninfo](https://pypi.org/project/screeninfo/) | 获取显示器信息 |

## 项目结构

```
diguo_help/
├── chrome_automation_project/
│   ├── main.py                 # ⭐ 主入口，ROLE_CONFIG 多角色配置驱动
│   ├── login_service.py        # 登录状态检测（token 过期 / 登出自动 sys.exit）
│   ├── change_map.py           # 地图切换辅助
│   ├── city_function.py        # 城池功能（在线奖励、荣誉、才艺、跑船、重建）
│   ├── package/
│   │   ├── __init__.py
│   │   ├── screen.py           # 图像识别底层工具（含聚类去重）
│   │   ├── ocr_util.py         # PaddleOCR 屏幕文字识别工具
│   │   ├── region.py           # 区域坐标转换
│   │   ├── generals.py         # 将领管理
│   │   ├── attacked.py         # 攻击记录
│   │   └── change_map/         # 地图切换模板
│   └── diguo/                  # 🖼️ 图像模板库
│       ├── rebel/              # 叛军（level/info/攻击按钮）
│       ├── generals/           # 将领状态
│       ├── city/               # 船坞、重建、在线奖励
│       ├── reward/
│       │   ├── online/         # 在线奖励模板
│       │   ├── library/        # 图书馆荣誉模板
│       │   └── palace/         # 宫殿才艺坊模板
│       ├── login/              # 登录页面
│       ├── location/           # 地图位置标识
│       └── ...
├── diguo/                      # Python 虚拟环境（git 已忽略）
├── .gitignore                  # 虚拟环境等大文件忽略规则
└── README.md
```

## 安装与配置

### 1. 环境准备

```bash
cd diguo_help
python3 -m venv diguo
source diguo/bin/activate

# 核心依赖
pip install pyautogui opencv-python numpy screeninfo Pillow

# OCR 依赖（首次运行会自动下载模型 ~20MB）
pip install paddlepaddle paddleocr
```

### 2. 游戏配置

1. Chrome 浏览器打开帝国网页版并登录
2. **浏览器窗口最大化**，游戏界面完整显示在主屏幕
3. 确认屏幕分辨率与图像模板匹配（默认适配 1440×900 等）
4. macOS 需授权：**系统设置 → 隐私与安全性 → 辅助功能** → 勾选终端/Python

## 使用方法

### 主脚本：多角色配置驱动

编辑 `chrome_automation_project/main.py` 底部：

```python
# ========== 选择角色 ==========
active_role = 'role'    # ← 改这里切换

# ========== 角色配置表 ==========

```

运行：

```bash
cd diguo_help
source diguo/bin/activate
python chrome_automation_project/main.py
```

### 角色配置参数说明

| 分组 | 参数 | 默认值 | 说明 |
|------|------|--------|------|
| rebel | `attack_num` | - | 打叛军目标总数，**≤0 表示不打叛军**直接挂机 |
| rebel | `send_rebel_list` | - | 叛军等级列表，如 `[28, 29]` |
| rebel | `num` | - | 将领数量 |
| ship | `is_active` | `True` | 是否跑船（False 跳过跑船但其他日常正常） |
| ship | `ship_interval` | `1200` | **日常任务最小执行间隔秒数**（默认 20min） |
| study | `study_active` | `False` | 是否才艺学习 |
| study | `study_type` | `['琴室']` | 才艺类型，支持多类型：`['琴室','棋室','书房','画廊']` |

### OCR 工具（独立测试）

```bash
# 交互式选区域 + OCR 识别
python chrome_automation_project/package/ocr_util.py

# 代码调用
from package.ocr_util import ocr_region, find_text, extract_number, get_today_rebel_count

# 识别固定区域
results = ocr_region(x=623, y=612, w=105, h=18)
# → [{'text': '今日已剿灭叛军:300/300', 'confidence': 0.99}, ...]

# 提取数字
num = extract_number('365.89万')  # → 365.89

# 游戏专用：今日叛军数量
done, total = get_today_rebel_count()  # → (300, 300)
```

## 核心工作流程

```
main(attack_num=300, ship_interval=1200, ...) 启动
│
├─ 重置全局状态 + 打印配置
│
├─ 🔴 首次启动 → 先执行一次日常任务（跑船/奖励/荣誉/才艺）
│
├─ attack_num ≤ 0?
│   └─ 跳过打叛军 → 直接进挂机循环（见下方阶段二）
│
╞═══════════ 阶段一：打叛军 + 定时日常 ═══════════
│  while 已攻击数 < attack_num:
│    ├─ 登录检测（登出自动退出）
│    ├─ 切世界界面 → 回圣域
│    ├─ cycle_attack() 清剿叛军
│    │   └─ 连续取消 20 次 → 告警
│    │
│    └─ 距上次日常 ≥ ship_interval?
│        └─ 执行日常任务（跑船/奖励/荣誉/才艺）
│
╞═══════════ 阶段二：叛军打满 → 挂机日常任务 ═══════════
│  while True:                            ← continuous_ship_with_reward
│    ├─ 登录检测（登出自动退出）
│    ├─ 重建城市
│    ├─ 执行日常任务
│    └─ sleep(ship_interval)
│
└─ Ctrl+C → 打印"已手动停止"
```

### 日常任务统一入口

`_run_daily_tasks(is_active, study_active, study_type)` 负责：

```
├─ get_dock_order()       ← if is_active
├─ get_online_reward()    ← 始终尝试
├─ get_free_honors()      ← 始终尝试
└─ get_study_art()        ← if study_active
```

每个任务独立 `try/except`，任一失败不影响其他。

## 图像模板

脚本依赖 `chrome_automation_project/diguo/` 下的 PNG 模板。游戏界面更新后需重新截取替换。

常用模板路径（在 `package/screen.py` 的 `get_click_type_path()` 中定义）：

| click_type | 用途 | 所在目录 |
|------------|------|---------|
| `reble_info_attack` | 叛军详情页「进攻」按钮 | rebel/info/ |
| `rel_attack` | 确认攻击按钮 | diguo/ 根 |
| `holy_place` | 圣域标识 | location/ |
| `online_reward` | 在线奖励弹窗 | reward/online/ |
| `double_reward` | 双倍领取按钮 | reward/online/ |
| `rebuild_city` | 重建城池按钮 | city/ |
| `dock` | 船坞入口 | city/ |
| `library` | 图书馆入口 | reward/library/ |
| `art` | 才艺坊入口 | reward/palace/ |
| `study` | 才艺学习房间按钮 | reward/palace/ |
| `exit_study` | 退出单个才艺学习界面 | reward/palace/ |

## OCR 性能

| 阶段 | 耗时 |
|------|------|
| 首次调用（模型加载） | ~20s，仅首次 |
| 后续每次 OCR | **~0.4s**（截图 0.2s + 推理 0.2s） |
| 调用次数 | 无限制，纯本地推理不走网络 |

## 注意事项

1. **全屏运行**：Chrome 浏览器必须最大化，游戏界面不能有遮挡
2. **主显示器**：游戏必须显示在主显示器，多显示器自动做坐标转换
3. **运行期间**：脚本运行时不要操作鼠标键盘
4. **图像精度**：默认 `confidence=0.8`，如找不到图像可降到 0.7
5. **虚拟环境**：不要在 headless 环境运行（需要 GUI）
6. **虚拟环境不上 git**：已配置 `.gitignore` 忽略 `/diguo/`，避免 push 大文件

## 停止脚本

- 终端按 `Ctrl + C` 强制终止
- 挂机循环检测到账号登出自动退出（`sys.exit(0)`）

## License

仅供学习交流使用，请勿用于游戏作弊或违反服务条款的场景。
