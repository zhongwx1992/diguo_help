# 帝国网页版自动化辅助工具 🎮

基于 Python + PyAutoGUI + OpenCV + PaddleOCR 的网页游戏自动化脚本，通过图像识别和 OCR 实现自动刷叛军、船坞运输、在线奖励、荣誉领取、才艺学习、领体力、扫荡战役等功能。

> ⚠️ **隐私说明**：真实角色配置保存在 `role_config.py`（已被 `.gitignore` 忽略，不会提交到 GitHub）。仓库只提供 `role_config_example.py` 示例模板，请勿在 README 或提交的代码中写入个人真实配置。

## 功能特性

| 功能 | 说明 |
|------|------|
| ⚔️ 自动刷叛军 | 按指定等级在屏幕范围内搜索攻击，找不到自动拖动地图换方向 |
| 🎯 连续取消检测 | 连续取消攻击 10 次判定叛军已打满，自动进入挂机阶段 |
| ⛵ 船坞运输 | 定时执行船坞订单，自动寻找船坞并填满所有坑位 |
| 🎁 在线奖励 | 自动领取在线奖励，支持双倍领取弹窗 |
| 📚 荣誉领取 | 自动进入图书馆领取荣誉书籍，支持广告免费刷新；可配置购买断简/红书碎片 |
| 🎨 才艺学习 | 支持同时学习多个才艺（琴室/棋室/书房/画廊），自动领取学习结果 |
| 💪 领体力 | 自动领取日常福利体力 |
| ⚔️ 扫荡战役 | 自动扫荡战役 |
| 🏰 城池重建 | 检测城池被攻击时自动重建主城 |
| 🔐 登录状态监控 | 挂机循环每轮检测登录状态，登出自动退出 |
| 🕐 日常任务调度 | 启动先执行一次，之后按 `ship_interval` 定时触发 |
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

## 目录结构

```
diguo_help/
├── chrome_automation_project/
│   ├── main.py                 # ⭐ 主入口，加载角色配置并驱动主流程
│   ├── role_config.py          # 🔒 私有角色配置（.gitignore 忽略，不提交）
│   ├── role_config_example.py  # 📄 角色配置示例模板（提交，供参考/复制）
│   ├── login_service.py        # 登录状态检测（token 过期 / 登出自动退出）
│   ├── change_map.py           # 地图切换辅助
│   ├── city_function.py        # 城池功能（奖励/荣誉/才艺/跑船/体力/扫荡/重建）
│   ├── package/
│   │   ├── __init__.py
│   │   ├── screen.py           # 图像识别底层工具（含聚类去重）
│   │   ├── ocr_util.py         # PaddleOCR 屏幕文字识别工具
│   │   ├── region.py           # 区域坐标转换
│   │   ├── generals.py         # 将领管理
│   │   └── attacked.py         # 攻击记录
│   └── diguo/                  # 🖼️ 图像模板库（rebel/city/reward/generals/login 等）
├── diguo/                      # Python 虚拟环境（git 已忽略）
├── .gitignore                  # 忽略虚拟环境、私有配置等
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

### 2. 游戏环境

1. Chrome 浏览器打开帝国网页版并登录
2. **浏览器窗口最大化**，游戏界面完整显示在主屏幕
3. 确认屏幕分辨率与图像模板匹配
4. macOS 需授权：**系统设置 → 隐私与安全性 → 辅助功能** → 勾选终端/Python

### 3. 角色配置（隐私重点）

角色配置保存于独立文件 `role_config.py`，**该文件已被 `.gitignore` 忽略，不会提交到 GitHub**：

```bash
# 复制示例模板生成本地私有配置
cd chrome_automation_project
cp role_config_example.py role_config.py

# 编辑 role_config.py，填入你自己的角色名、叛军等级等参数
```

`main.py` 启动时会优先加载 `role_config.py`，若不存在则回退加载 `role_config_example.py`。

## 使用方法

### 1. 编辑角色配置

打开 `role_config.py`，按需修改各角色的参数，并设置当前要运行的角色：

```python
ROLE_CONFIG = {
    '示例角色名': {
        'rebel': {
            "is_attack_rebel": True,    # 是否开启打叛军
            "send_rebel_list": [28, 29],# 要打的叛军等级列表
            "num": 2,                   # 参战将领数量
        },
        'ship': {
            "is_active": True,          # 是否开启跑船
            "ship_interval": 23 * 60,   # 日常任务最小执行间隔（秒）
        },
        'study': {
            "study_active": True,       # 是否开启才艺学习
            "study_type": ['书房'],      # 才艺类型：琴室/棋室/书房/画廊 支持同时学习多个类型
        },
        'honors': {
            "buy_bamboo_slip": True,    # 是否花费荣誉购买断简
            "buy_red_book_debris": False,# 是否花费荣誉购买红书碎片
        },
    },
    # ... 可继续添加更多角色
}

# 当前要运行的角色
ACTIVE_ROLE = '示例角色名'
```

### 2. 运行

```bash
cd diguo_help
source diguo/bin/activate
python chrome_automation_project/main.py
```

## 角色配置参数说明

每组配置会被展平（flatten）成 `main()` 的关键字参数：

| 分组 | 参数 | 类型 | 说明 |
|------|------|------|------|
| rebel | `is_attack_rebel` | bool | 是否开启打叛军。`False` 时跳过打叛军直接进入日常挂机 |
| rebel | `send_rebel_list` | list | 叛军等级列表，如 `[28, 29]` |
| rebel | `num` | int | 参战将领数量 |
| ship | `is_active` | bool | 是否开启跑船 |
| ship | `ship_interval` | int | 日常任务最小执行间隔秒数（默认 1200 = 20min） |
| study | `study_active` | bool | 是否开启才艺学习 |
| study | `study_type` | list | 才艺类型，支持多类型：`['琴室','棋室','书房','画廊']` |
| honors | `buy_bamboo_slip` | bool | 是否花费荣誉购买断简 |
| honors | `buy_red_book_debris` | bool | 是否花费荣誉购买红书碎片 |

## 核心工作流程

```
main(**cfg)   # cfg 由 role_config 展平而来
│
├─ 重置全局状态（攻击数、连续取消数、攻击坐标、拖动位置、方向索引）
│
├─ 🔴 首次启动 → 先执行一次日常任务
│
├─ is_attack_rebel == False
│   └─ 跳过打叛军 → 直接进入日常任务挂机循环（见阶段二）
│
╞═══════════ 阶段一：打叛军 + 定时日常 ═══════════
│  while 连续取消攻击次数 < 10:
│    ├─ 登录检测（登出自动退出）
│    ├─ 切世界界面 → 回圣域
│    ├─ cycle_attack() 清剿叛军
│    │   ├─ 攻击成功 → 连续取消计数清零
│    │   └─ 取消攻击 → 连续取消计数 +1（≥10 判定叛军已打满）
│    │
│    └─ 距上次日常 ≥ ship_interval → 执行日常任务
│
╞═══════════ 阶段二：叛军打满 → 日常任务挂机 ═══════════
│  while True:                          ← continuous_ship_with_reward
│    ├─ 登录检测（登出自动退出）
│    ├─ 重建城市
│    ├─ 执行日常任务
│    └─ sleep(ship_interval)
│
└─ Ctrl+C → 打印"已手动停止"
```

### 日常任务统一入口

`_run_daily_tasks(is_active, study_active, study_type, buy_bamboo_slip, buy_red_book_debris)` 负责：

```
├─ get_dock_order()              ← if is_active（跑船）
├─ get_online_reward()           ← 始终尝试（在线奖励）
├─ get_free_honors()             ← 始终尝试（领荣誉，含购买断简/红书碎片开关）
├─ get_study_art()               ← if study_active（才艺学习）
├─ get_strength()                ← 始终尝试（领体力）
└─ get_every_battle()            ← 始终尝试（扫荡战役）
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

## OCR 工具（独立测试）

```bash
# 交互式选区域 + OCR 识别
python chrome_automation_project/package/ocr_util.py

# 代码调用
from package.ocr_util import ocr_region, find_text, extract_number

# 识别固定区域
results = ocr_region(x=623, y=612, w=105, h=18)

# 提取数字
num = extract_number('365.89万')  # → 365.89
```

## 注意事项

1. **全屏运行**：Chrome 浏览器必须最大化，游戏界面不能有遮挡
2. **主显示器**：游戏必须显示在主显示器，多显示器自动做坐标转换
3. **运行期间**：脚本运行时不要操作鼠标键盘
4. **图像精度**：默认 `confidence=0.8`，如找不到图像可降到 0.7
5. **虚拟环境**：不要在 headless 环境运行（需要 GUI）
6. **上传前检查**：`.gitignore` 已忽略 `/diguo/`（虚拟环境）和 `/chrome_automation_project/role_config.py`（私有配置），提交前请确认没有误提交真实配置

## 停止脚本

- 终端按 `Ctrl + C` 强制终止
- 挂机循环检测到账号登出自动退出

## License

仅供学习交流使用，请勿用于游戏作弊或违反服务条款的场景。