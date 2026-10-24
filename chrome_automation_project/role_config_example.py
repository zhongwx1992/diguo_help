# -*- coding: utf-8 -*-
"""
角色配置模板（示例文件，供参考 / 可直接复制使用）

使用方式：
    1. 复制本文件为 role_config.py
       cp role_config_example.py role_config.py
    2. 在 role_config.py 中填写你自己的真实配置（角色名、参数等）
    3. 把 ACTIVE_ROLE 改成你要运行的角色名，然后直接运行 main.py

说明：
    - role_config.py 已被 .gitignore 忽略，不会提交到 github，
      用于存放你个人的真实配置，避免信息泄漏。
    - 本示例文件 role_config_example.py 会提交到仓库，方便他人了解配置格式。

配置结构：
    每个角色是一个字典，按功能拆成多个分组（group）：
        rebel   叛军配置
        ship    跑船配置
        study   才艺学习配置
        honors  荣誉购买配置
    运行时会把所有分组展平（flatten）成 main() 的关键字参数。
"""

ROLE_CONFIG = {
    # 示例角色 1：刷叛军 + 才艺 + 开船
    '刷叛军弓兵才艺开船': {
        'rebel': {
            "is_attack_rebel": True,      # 是否开启打叛军
            "send_rebel_list": [28, 29],  # 要打的叛军等级列表
            "num": 2,                     # 参战将领数量
        },
        'ship': {
            "is_active": True,            # 是否开启跑船
            "ship_interval": 23 * 60,     # 日常任务执行间隔（秒）
        },
        'study': {
            "study_active": True,         # 是否开启才艺学习
            "study_type": ['书房'],        # 才艺类型：琴室 / 棋室 / 书房 / 画廊
        },
        'honors': {
            "buy_bamboo_slip": False,     # 是否花费荣誉购买断简
            "buy_red_book_debris": False, # 是否花费荣誉购买红书碎片
        },
    },
    # 示例角色 2：刷叛军 + 才艺 + 不开船
    '刷叛军骑兵才艺不开船': {
        'rebel': {
            "is_attack_rebel": True,
            "send_rebel_list": [28, 29],
            "num": 4,
        },
        'ship': {
            "is_active": True,
            "ship_interval": 23 * 60,
        },
        'study': {
            "study_active": True,
            "study_type": ['棋室'],
        },
        'honors': {
            "buy_bamboo_slip": False,
            "buy_red_book_debris": False,
        },
    },
    # 示例角色 3：不刷叛军 + 才艺 + 开船
    '不刷叛军骑兵才艺开船': {
        'rebel': {
            "is_attack_rebel": True,      # 是否开启打叛军
            "send_rebel_list": [29],
            "num": 1,
        },
        'ship': {
            "is_active": True,
            "ship_interval": 23 * 60,
        },
        'study': {
            "study_active": True,
            "study_type": ['棋室'],
        },
        'honors': {
            "buy_bamboo_slip": False,
            "buy_red_book_debris": False,
        },
    },
    # 加新角色：直接复制上面任意一个模板，改角色名和参数即可
}

# ========== 当前要运行的角色（改成你要跑的角色名） ==========
ACTIVE_ROLE = '刷叛军弓兵才艺开船'