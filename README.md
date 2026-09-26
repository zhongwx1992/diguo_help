# 帝国网页版自动化辅助工具 🎮

基于 Python + PyAutoGUI 的网页游戏自动化脚本，通过图像识别实现自动刷叛军、自动补兵、船坞运输、城池重建等功能。

## 功能特性

| 功能 | 说明 |
|------|------|
| 🔍 自动搜索叛军 | 按指定等级在屏幕范围内搜索，优先攻击距离中心最近的目标 |
| ⚔️ 自动攻击 | 点击叛军 → 选择就绪将领 → 确认攻击，全流程自动完成 |
| 🗺️ 自动拖动地图 | 找不到叛军时自动向 8 个方向拖动屏幕继续搜索 |
| 🏠 圣域检测 | 自动判断是否在圣域地图，偏离时自动回归 |
| 🔄 自动补兵 | 将领兵力不足时自动补兵等待就绪 |
| ⛵ 船坞运输 | 定时（默认 30 分钟）执行船坞订单操作 |
| 🏰 城池重建 | 检测城池被攻击时自动重建主城 |
| 🔐 登录状态监控 | Token 过期自动退出，等待重新登录 |
| 🚫 防重复攻击 | 记录已攻击坐标，禁止重复点击同一叛军 |

## 技术栈

- **Python 3.11**
- [PyAutoGUI](https://pyautogui.readthedocs.io/) — 屏幕截图、图像定位、鼠标键盘自动化
- [OpenCV](https://pypi.org/project/opencv-python/) — 图像匹配（`confidence` 参数需要）
- [Selenium](https://www.selenium.dev/) — Chrome 浏览器自动化控制（可选）
- [screeninfo](https://pypi.org/project/screeninfo/) — 获取显示器信息
- [pynput](https://pypi.org/project/pynput/) — 键盘监听

## 项目结构

```
diguo_help/
├── chrome_automation_project/
│   ├── main.py                 # ⭐ 主入口，自动刷叛军核心循环
│   ├── login_service.py        # 登录状态检测
│   ├── change_map.py           # 地图切换（圣域/主城）
│   ├── city_function.py        # 城池功能（重建、船坞、在线奖励）
│   ├── attack_city.py          # 攻城功能
│   ├── play_game.py            # 小游戏辅助
│   ├── diguo_help.py           # Selenium 版辅助脚本
│   ├── package/
│   │   ├── screen.py           # 核心工具（图像识别、点击、屏幕计算）
│   │   ├── region.py           # 区域坐标转换
│   │   ├── generals.py         # 将领管理
│   │   └── attacked.py         # 攻击记录
│   └── diguo/                  # 🖼️ 图像模板库（用于图像匹配）
│       ├── rebel/              # 叛军相关截图
│       ├── generals/           # 将领状态截图
│       ├── city/               # 城池相关截图
│       ├── login/              # 登录页面截图
│       ├── location/           # 地图位置标识
│       ├── attack_city/        # 攻城目标城市截图
│       ├── get_resource/       # 资源采集截图
│       └── game/               # 小游戏截图
├── chromedriver-mac-arm64/     # ChromeDriver（macOS Apple Silicon）
└── diguo/                      # Python 虚拟环境
```

## 安装与配置

### 1. 环境准备

```bash
# 克隆项目后，进入目录
cd diguo_help

# 创建虚拟环境（或使用已有的 diguo/）
python3 -m venv diguo
source diguo/bin/activate

# 安装依赖
pip install pyautogui opencv-python selenium screeninfo pynput Pillow
```

### 2. ChromeDriver（仅 Selenium 脚本需要）

本项目已包含 `chromedriver-mac-arm64/chromedriver`，适用于 **macOS Apple Silicon**。

其他平台请从 [ChromeDriver 官网](https://chromedriver.chromium.org/) 下载对应版本，放在项目根目录即可。

### 3. 游戏配置

1. 在 Chrome 浏览器中打开帝国网页版并登录账号
2. **浏览器窗口需最大化**，游戏界面需完整显示在主屏幕上
3. 确认屏幕分辨率与图像模板匹配（默认适配 1440×900 等常见分辨率）

## 使用方法

### 主脚本：自动刷叛军

编辑 `chrome_automation_project/main.py` 末尾的参数：

```python
# 参数说明：
# main(攻击总次数, [叛军等级列表], 将领数量, 是否活跃模式)

# 示例 1：攻击 350 次，刷 28/29 级叛军，用 3 个将领
main(350, [28, 29], 3, False)

# 示例 2：攻击 200 次，刷 22 级叛军（歌德），单将领
main(200, [22], 1, False)
```

运行脚本：

```bash
cd diguo_help
source diguo/bin/activate
python chrome_automation_project/main.py
```

### Selenium 脚本（备选）

```bash
python chrome_automation_project/diguo_help.py
```

## 核心工作流程

```
┌─────────────────────────────────────────────┐
│  main() 主循环                                │
│                                               │
│  1. 检测登录状态 → Token 过期则退出            │
│  2. 检测是否在世界地图 → 不在则切到世界         │
│  3. 检测是否在圣域 → 不在则回圣域              │
│  4. cycle_attack() 清剿叛军                    │
│     ├─ search_best_rebel() 搜索叛军            │
│     │   └─ 按距离中心排序，返回最优坐标         │
│     ├─ attack_rebel() 执行攻击                 │
│     │   ├─ 点击叛军                            │
│     │   ├─ 选择可用将领                        │
│     │   └─ 确认攻击                            │
│     └─ 未找到则 drag_screen() 换方向           │
│  5. 每 30 分钟执行一次船坞运输                  │
│  6. 循环直到完成指定攻击次数                    │
└─────────────────────────────────────────────┘
```

## 图像模板说明

脚本依赖 `chrome_automation_project/diguo/` 目录下的 PNG 截图进行图像匹配。如果游戏界面有更新，需要重新截取对应截图替换。

常用模板路径（在 `package/screen.py` 的 `get_click_type_path()` 中定义）：

| click_type | 用途 |
|------------|------|
| `reble_info_attack` | 叛军详情页的「进攻」按钮 |
| `rel_attack` | 确认攻击按钮 |
| `backspace` | 返回键 |
| `holy_place` | 圣域标识（用于位置检测） |
| `online_reward` | 在线奖励弹窗 |
| `rebuild_city` | 重建城池按钮 |
| `dock` / `dock_yellow_order` | 船坞相关 |

## ⚠️ 注意事项

1. **全屏运行**：Chrome 浏览器必须最大化，游戏界面不能有遮挡
2. **主显示器**：游戏必须显示在**主显示器**上，多显示器环境下坐标会自动转换
3. **图像精度**：`confidence=0.9` 匹配度较高，如找不到图像可适当降低（0.7~0.8）
4. **运行期间**：脚本运行时**不要操作鼠标和键盘**，否则会干扰自动点击
5. **虚拟环境**：脚本依赖 pyautogui 等 GUI 库，不要在 headless 环境下运行
6. **Mac 权限**：macOS 需要在「系统设置 → 隐私与安全性 → 辅助功能」中授权终端 Python

## 停止脚本

- 直接在终端按 `Ctrl + C` 强制终止
- 或点击游戏界面的暂停/停止按钮（需自行适配）

## License

仅供学习交流使用，请勿用于游戏作弊或违反服务条款的场景。
