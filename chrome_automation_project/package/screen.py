from turtle import position
from screeninfo import get_monitors
from pyautogui import locateOnScreen, center, ImageNotFoundException, moveTo, click
from time import sleep

# 游戏基础单元大小
#GAME_UNIT_SIZE = (140,70)
GAME_UNIT_SIZE = (124,80)

def get_primary_monitor():
    """获取主显示器信息"""
    monitors = get_monitors()
    for m in monitors:
        if m.is_primary:
            return m
    return monitors[0]  # 如果没有主显示器标记，返回第一个
# 直接固化信息，避免每次都计算
PRIMARY_MONITOR_INFO = get_primary_monitor()


def get_screen_center():
    """获取主显示器中心坐标"""
    #primary = primary_monitor
    center_x = PRIMARY_MONITOR_INFO.width // 2
    center_y = PRIMARY_MONITOR_INFO.height // 2
    return center_x, center_y

# 直接固化坐标，避免每次都计算
SCREEN_CENTER_INFO = get_screen_center()


# 构建禁止区域计算函数
def get_ingore_region(x, y):
    """
    Purpose: 构建禁止区域计算函数
    :x  输入需要计算的坐标
    :y  输入需要计算的坐标
    :return: 禁止区域计算结果，  
    """
    map_size_x = GAME_UNIT_SIZE[0]
    map_size_y = GAME_UNIT_SIZE[1]

    point_a = (x - map_size_x // 2 , y - map_size_y // 2)
    point_b = (x + map_size_x // 2 , y - map_size_y // 2)
    point_c = (x + map_size_x // 2 , y + map_size_y // 2)
    point_d = (x - map_size_x // 2 , y + map_size_y // 2)

    return_value = {
        'location': (x,y),
        'a': point_a,
        'b': point_b,
        'c': point_c,
        'd': point_d
    }
    #print(f"构建禁止区域计算结果： {return_value} ")
    return return_value

def get_game_center_location():
    """
    叛军搜索需要排除的区域四点坐标，从左上角开始顺时针 (左上) b(右上) c(右下) d(左下) 四个点

    游戏中心位于游戏屏幕，(6, 4.5) 单元位置 整个游戏屏幕一共由 11 * 9 个单位组成 
    每个游戏单位占用的像素大小应该是 ( 1352 // 11, (878 - 158) // 9 ) 单位像素
    主屏浏览器占用的屏幕像素高度： 158 （测量得到）
    """
    game_center_x = SCREEN_CENTER_INFO[0]
    ## 这里游戏中心的y刚好和屏幕中心的y 差一个游戏单位的位置
    #game_center_y = SCREEN_CENTER_INFO[1] + GAME_UNIT_SIZE[1] // 2
    # base + 4 单元像素
    game_center_y = 158 + 4 * GAME_UNIT_SIZE[1]
    return_value = get_ingore_region(game_center_x, game_center_y)
    # print(f"获取基础坐标信息： {return_value} ")
    return return_value

# 直接固化游戏屏幕中心坐标，避免每次都计算
GAME_CENTER_LOCATION = get_game_center_location()


def calculate_distance(point1, point2):
    """
    计算两点之间的欧几里得距离
    :param point1: 第一个点的坐标 (x1, y1)
    :param point2: 第二个点的坐标 (x2, y2)
    :return: 两点之间的距离
    """
    x1, y1 = point1
    x2, y2 = point2
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    
def get_click_type_path(click_type: str) -> str | None:
    """
    根据点击类型获取对应的图片路径
    Args:
        click_type: 操作类型字符串
    Returns:
        对应的图片路径字符串， 如果类型不存在则返回None
    """
    path_mapping = {
        '300_attacked': 'chrome_automation_project/diguo/rebel/info/300_attacked.png',
        'reble_info_attack': 'chrome_automation_project/diguo/rebel/info/attack.png',
        'rel_attack': 'chrome_automation_project/diguo/rel_attack.png',
        'back_home': 'chrome_automation_project/diguo/rebel/home.png',
        'reble_info_cancel': 'chrome_automation_project/diguo/rebel/info/cancel.png',
        'backspace': 'chrome_automation_project/diguo/backspace.png',
        'cancel_get_resource': 'chrome_automation_project/diguo/get_resource/cancel.png',
        # 背包操作
        'backpack': 'chrome_automation_project/package/change_map/backpack.png',
        'backpack_attack': 'chrome_automation_project/package/change_map/backpack_attack.png',
        'random_move': 'chrome_automation_project/package/change_map/random_move.png',
        'random_move_use': 'chrome_automation_project/package/change_map/random_move_use.png',
         
        'to_world': 'chrome_automation_project/package/change_map/to_world.png',
        'to_city': 'chrome_automation_project/package/change_map/to_city.png',
        'holy_place': 'chrome_automation_project/diguo/location/holy_place.png',

        'online_reward': 'chrome_automation_project/diguo/city/online_reward.png',
        'get_online_reward': 'chrome_automation_project/diguo/city/get_online_reward.png',
        'online_reward_exit': 'chrome_automation_project/diguo/city/online_reward_exit.png',
        'rebuild_city': 'chrome_automation_project/diguo/city/rebuild_city.png',
        'rebuild_city_confirm': 'chrome_automation_project/diguo/city/rebuild_city_confirm.png',
        'rebuild_city_cancel': 'chrome_automation_project/diguo/city/rebuild_city_cancel.png',
        
        # 船坞操作
        'dock': 'chrome_automation_project/diguo/city/dock.png',
        'dock_in': 'chrome_automation_project/diguo/city/dock_in.png',
        'dock_yellow_order': 'chrome_automation_project/diguo/city/dock_yellow_order.png',
        'dock_yellow_confirm': 'chrome_automation_project/diguo/city/dock_yellow_confirm.png',

        'dock_get_order': 'chrome_automation_project/diguo/city/dock_get_order.png',
        'dock_yellow_order_shoes': 'chrome_automation_project/diguo/city/dock_yellow_order_shoes.png',
        'dock_get_order_confirm': 'chrome_automation_project/diguo/city/dock_get_order_confirm.png',
        'rebuild_main_city': 'chrome_automation_project/diguo/city/rebuild_main_city.png',
        'rebuild_main_city_confirm': 'chrome_automation_project/diguo/city/rebuild_main_city_confirm.png',

        'in_dock': 'chrome_automation_project/diguo/city/in_dock.png',
        'quit_dock': 'chrome_automation_project/diguo/city/quit_dock.png',

        'dock_source': 'chrome_automation_project/diguo/city/dock_source.png',

        # 登录操作
        'token_expired': 'chrome_automation_project/diguo/login/token_expired.png',
        'return_to_login': 'chrome_automation_project/diguo/login/return_to_login.png',
        'other_login': 'chrome_automation_project/diguo/login/other_login.png',
        'refresh_web': 'chrome_automation_project/diguo/login/refresh_web.png',
        'start_game_button': 'chrome_automation_project/diguo/login/start_game_button.png',
        'close_notice': 'chrome_automation_project/diguo/login/close_notice.png',
        'server_list': 'chrome_automation_project/diguo/login/server_list.png',
        'h705': 'chrome_automation_project/diguo/login/h705.png',

        ## game help
        'dishu_start_game': 'chrome_automation_project/diguo/game/attack_dishu/star_game.png',
        'dishu_game_over': 'chrome_automation_project/diguo/game/attack_dishu/game_over.png',
        'dishu_1': 'chrome_automation_project/diguo/game/attack_dishu/dishu_1.png',
        'dishu_2': 'chrome_automation_project/diguo/game/attack_dishu/dishu_2.png',
        'dishu_3': 'chrome_automation_project/diguo/game/attack_dishu/3-1.png',
        'dishu_eyes': 'chrome_automation_project/diguo/game/attack_dishu/eyes.png',

        'attack_my_city': 'chrome_automation_project/diguo/city/attack_my_city.png',
        'exit': 'chrome_automation_project/diguo/rebel/info/exit.png',

        'select': 'chrome_automation_project/diguo/generals/select.png',
        'available': 'chrome_automation_project/diguo/generals/available.png',
        'unavailable': 'chrome_automation_project/diguo/generals/unavaliable.png',
        'reload': 'chrome_automation_project/diguo/generals/reload.png',
        'oncall': 'chrome_automation_project/diguo/generals/oncall.png',

        'hero_select': 'chrome_automation_project/diguo/rebel/hero_select.png',
    }
    

    if click_type not in path_mapping:
        print(f"参数错误，没有该操作类型: {click_type}")
        return None
    return path_mapping[click_type]


def image_center_location(image_path:str,region=None,confidence=0.8):
    """
    定位图像中心坐标（基于主显示器坐标系）
    :param image_path: 图像路径
    :return: (x, y) 主显示器坐标系下的中心坐标
    :region: (x, y, width, height) 主显示器区域, 注意输入的是主显示器区域，而不是屏幕区域，所以这里需要转换一下
    """
    primary = PRIMARY_MONITOR_INFO
    try:
        location = locateOnScreen(image_path, confidence=confidence,region=region)
        if not location:
            #print(f"Image not found: {image_path}")
            return None, None
    except ImageNotFoundException:
        #print(f"Image not found: {image_path}")
        return None, None
    # 获取屏幕坐标
    screen_x, screen_y = center(location)
    # 转换为相对于主显示器的坐标
    primary_x = (screen_x - primary.x) // 2
    primary_y = (screen_y - primary.y) // 2
    return primary_x, primary_y


def search_and_click_image(click_type, clicks=1, interval=0.2, duration=0.2,confidence=0.8,region=None ):
    """
    Purpose: 实现选中图片中心位置进行点击等功能
    :param click_type: 动作类型  
    :param clicks: 点击次数
    :param interval: 点击间隔
    :param duration: 点击持续时间
    """
    image_path = get_click_type_path(click_type)
    if image_path is None:
        return 0
        
    x, y = image_center_location(image_path=image_path,confidence=confidence,region=region)
    if x is None or y is None:
        #print(f"未找到图像: {image_path}")
        return 0
    #moveTo(x, y, 0.1)
    click(x, y, button='left', clicks=clicks, interval=interval, duration=duration)
    return 1


# def image_exist(image_name,confidence=0.8,region=None):
#     """
#     Purpose: 实现判断图片是否存在的功能
#     :param image_name: 图像名称 需要先存在get_click_type_path(image_name)函数中
#     :param confidence: 匹配度
#     :param region: 区域
#     """
#     x, y = image_center_location(image_path=get_click_type_path(image_name),confidence=confidence,region=region)
#     if x is None or y is None:
#         return (False, (x ,y) )
#     return (True, (x ,y) )


def click_image_when_exist(image_a,image_b,clicks=1, interval=0.2, duration=0.2,confidence=0.8,region=None):
    """
    Purpose: 实现存在图片A点击图片B的功能，当图片A出现时，才点击
    """
    position_a = image_center_location(image_path=get_click_type_path(image_a),confidence=confidence,region=region)
    position_b = image_center_location(image_path=get_click_type_path(image_b),confidence=confidence,region=region)

    if position_a[0] is not None and position_a[1] is not None:
        moveTo(position_b[0], position_b[1], 0.1)
        click(position_b[0], position_b[1], button='left', clicks=clicks, interval=interval, duration=duration)
        return True
    else:
        print("未找到图像: ", image_a)
        return False



if __name__ == "__main__":
    # 测试代码
    #print("主显示器信息:", PRIMARY_MONITOR_INFO)    
    #print("主显示器中心坐标:", SCREEN_CENTER_INFO)
    # print("游戏中心坐标:", GAME_CENTER_LOCATION)
    # print("完成")
    # print( image_center_location( get_click_type_path('300_attacked'),confidence=0.7 ))
    # search_and_click_image(click_type='300_attacked',clicks=1, interval=0.2, duration=0.2,confidence=0.7)


    click_image_when_exist(image_a='dock',image_b='dock')

    