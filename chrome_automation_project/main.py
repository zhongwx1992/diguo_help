
from math import fabs
from time import sleep
import pyautogui
from pyautogui import ImageNotFoundException
import random
#from package.attacked import get_attacked_locations,ATTACKED_LOCATIONS
from package.screen import PRIMARY_MONITOR_INFO, GAME_CENTER_LOCATION, get_ingore_region,calculate_distance,image_center_location, search_and_click_image,get_click_type_path
from package.region import primary_region_to_screen_region
from change_map import return_to_holy_place,is_in_holy_place
from city_function import get_online_reward,rebuild_main_city,get_dock_order
from pynput import keyboard
from datetime import datetime
from login_service import login_staus,return_login_exit



# 全局变量
DRAG_IGNORE_POSITION = (0,0)
# 游戏基础单元大小
#GAME_UNIT_SIZE = (140,70)
GAME_UNIT_SIZE = (124,80)

# 叛军搜索置信度
REBEL_SEARCH_CONFIDENCE = 0.9
# 叛军搜索区域 ，为了防止出现意外进行了阉割，仅保留了搜索区域，避免误触
# ( 游戏单元的宽度 // 2 + 5, 浏览器标题高度 + 游戏单元的高度 * 2 , 游戏屏幕宽度 - 游戏单元的宽度 * 1.5  )
REBEL_SEARCH_REGION = (70, 318, 1165,440)

DIRECTION_LIST = ['north','northeast','southeast','southwest','northwest','west','east','south']
DIRECTION_LIST_INDEX = random.randint(0, 7)
ATTACKED_LOCATIONS=[]

REBEL_ATTACKED_NUMBER = 0

def rebuild_and_back_to_holy_place(active=True):
    """
    Purpose: 重建城市并回到圣域
    """
    if rebuild_main_city():
        print("检测到被攻击，重建主城，并回圣域")
        return_to_holy_place(active=active)
        return True
    else:
        #print("未检测到被攻击，继续")
        return False

def get_attacked_locations( rebel_location ):
    """
    获取已经攻击过的叛军坐标列表
    """
    global ATTACKED_LOCATIONS
    # 这是获取到的，需要下次点击的位置
    x , y = rebel_location

    if len(ATTACKED_LOCATIONS) > 0:
        # 计算攻击之后位置和之前攻击位置的距离，推算出本次攻击之后，历史攻击过位置的相对坐标
        for index, i in enumerate(ATTACKED_LOCATIONS):
            b_x , b_y = i
            ATTACKED_LOCATIONS[index] = (2 * b_x - x, 2 * b_y - y)

    # 这里加入的，应该是游戏屏幕中心的坐标了，因为这是攻击之后的位置

    ATTACKED_LOCATIONS.append(GAME_CENTER_LOCATION['location'])
    #print("-------------------------")
    #print("本次找到攻击目标：", (x,y))
    print("-------------------------\n" ,"已攻击过目标：", ATTACKED_LOCATIONS, "总数量：", len(ATTACKED_LOCATIONS))
    return ATTACKED_LOCATIONS

def drag_screen(direction: str, x_distance=0, y_distance=0, duration=0.7):
    """
    拖动屏幕
    :param direction: 拖动方向，'west' 向西，'east' 向东，'north' 向北，'south' 向南，
    'northeast' 东北，'southeast' 东南，'northwest' 西北，'southwest' 西南
    :param distance: 拖动距离（像素）
    :param duration: 拖动持续时间（秒）
    :return: 拖动的像素差异 (dx, dy)
    """
    
    x_distance = 4*GAME_UNIT_SIZE[0]
    y_distance = 3*GAME_UNIT_SIZE[1]

    center_x, center_y = GAME_CENTER_LOCATION['location']
    # 移动鼠标到屏幕中心
    pyautogui.moveTo(center_x,center_y, duration=0.2)
    # 计算拖动方向
    dx, dy = 0, 0
    if direction == 'west':
        dx = x_distance
    elif direction == 'east':
        dx = -x_distance
    elif direction == 'north':
        dy = y_distance
    elif direction == 'south':
        dy = -y_distance

    elif direction == 'northeast':
        dx = -x_distance
        dy = y_distance
    elif direction == 'southeast':
        dx = -x_distance
        dy = -y_distance
    elif direction == 'northwest':
        dx = x_distance
        dy = y_distance
    elif direction == 'southwest':
        dx = x_distance
        dy = -y_distance
    

    print("游戏中心坐标：", center_x, center_y) 
    print("拖动前坐标：", pyautogui.position())
    # 执行拖动操作
    pyautogui.mouseDown(button='left')
    pyautogui.dragRel(dx, dy, duration=duration, button='left')
    pyautogui.mouseUp(button='left')
    
    #需要拿这个坐标去做判断
    after_x, after_y = pyautogui.position()

    drag_info = {
        'deta': (dx,dy),
        'after_drag': (after_x,after_y),
        # 其实就是游戏屏幕中心
        'before_drag': (center_x,center_y)  
    }
    global DRAG_IGNORE_POSITION
    DRAG_IGNORE_POSITION = (after_x,after_y)

    return drag_info



# 直接固化坐标，避免每次都计算
def is_ingore_rebel(x=0 , y=0):
    """
    判断输入的坐标是否在禁止区域
    输入的坐标必须非None
    在的话返回 True 不在返回 False
    """
    # 判断坐标是否在滑动坐标前的 禁止区域
    is_drag_ingore = False
    is_game_center_ingore = False
    is_attacked = False
    
    # 判断坐标是否在已经攻击过的区域内
    print(f"禁止攻击区域判断 - 本次攻击坐标：({x},{y})")
    print(f"禁止攻击区域判断 - 已经攻击过的坐标：{ATTACKED_LOCATIONS}")

    if len(ATTACKED_LOCATIONS) > 0:
        for i in ATTACKED_LOCATIONS:
            #判断 x y 是不是在这个忽视区域
            last_ingore = get_ingore_region(i[0],i[1])
            a = last_ingore['a']
            b = last_ingore['b']
            c = last_ingore['c']
            if int(x) < b[0] and int(x) > a[0] and int(y) < c[1] and int(y) > b[1]:
                is_attacked = True
                break


    if DRAG_IGNORE_POSITION != (0,0):
        drag_ingore = get_ingore_region(DRAG_IGNORE_POSITION[0],DRAG_IGNORE_POSITION[1])       
        a = drag_ingore['a']
        b = drag_ingore['b']
        c = drag_ingore['c']
        if int(x) < b[0] and int(x) > a[0] and int(y) < c[1] and int(y) > b[1]:
            is_drag_ingore = True

    # 判断坐标是否在游戏屏幕中心的禁止区域
    a = GAME_CENTER_LOCATION['a']
    b = GAME_CENTER_LOCATION['b']
    c = GAME_CENTER_LOCATION['c']
    # 区域限制
    if int(x) < b[0] and int(x) > a[0] and int(y) < c[1] and int(y) > b[1]:
        #print("坐标在区域内")
        is_game_center_ingore = True
    
    print(f"坐标：({x},{y}) \n 游戏中心坐标：{is_game_center_ingore} \n 滑动坐标前：{is_drag_ingore} \n 已经攻击过：{is_attacked}")
    # 两个都返回false最终才能通过
    if is_game_center_ingore or is_drag_ingore or is_attacked:
        return True
    else:
        return False


# 这个函数现在没用到了
def search_rebel(search_level):
    """
    搜索叛军并返回可直接使用的攻击坐标，因为叛军的寻找是通过等级的小圆圈数字，所以最后需要微调一下y的坐标
    :param search_level: 叛军等级
    :return: (x, y) 可直接用于攻击的坐标，未找到返回None
    """
    level_path = f'chrome_automation_project/diguo/rebel/{search_level}.png'

    rebel_x, rebel_y = image_center_location(level_path, region=primary_region_to_screen_region(REBEL_SEARCH_REGION,PRIMARY_MONITOR_INFO),confidence=REBEL_SEARCH_CONFIDENCE)
    
    if rebel_x is None or rebel_y is None:
        print(f"未找到叛军图像: {search_level}")
        return None
    if is_ingore_rebel(rebel_x,rebel_y):
        print(f"找到的叛军在中心区域内: {search_level}")
        return None

    attack_x = rebel_x
    attack_y = rebel_y - 25
    pyautogui.moveTo(attack_x, attack_y, 1)
    print(f"移动成功，找到叛军: ({attack_x}, {attack_y})")
    return attack_x, attack_y



def is_aim_rebel(search_level):
    """
    输入叛军等级，判断打开的是否是该等级叛军
    :param level: 叛军等级
    :return: True 是该等级叛军， False 不是该等级叛军
    """
    level_path = f'chrome_automation_project/diguo/rebel/info/{search_level}.png'
    location = image_center_location(image_path=level_path,confidence=0.9)        
    aim_reblel = location != (None, None)
    #print("结果: ",location)
    #pyautogui.moveTo(location[0], location[1])
    return aim_reblel


def search_best_rebel(search_level):
    """
    搜索叛军并返回所有匹配的叛军坐标列表
    :param search_level: 叛军等级
    返回距离中心点最近的叛军坐标
    :return: 返回最优攻击坐标，未找到返回 (None,None)
    """
    level_path = f'chrome_automation_project/diguo/rebel/level/{search_level}.png'
    
    try:
        # 尝试获取所有匹配位置
        all_locations = pyautogui.locateAllOnScreen(
            level_path,
            confidence=REBEL_SEARCH_CONFIDENCE,
            region=primary_region_to_screen_region(REBEL_SEARCH_REGION,PRIMARY_MONITOR_INFO)
        )
        rebel_coords = []
        # 遍历所有找到的叛军图像
        for location in all_locations:
            # 获取屏幕坐标
            screen_x, screen_y = pyautogui.center(location)
            # 转换为相对于主显示器的坐标
            primary = PRIMARY_MONITOR_INFO
            primary_x = (screen_x - primary.x) // 2
            primary_y = (screen_y - primary.y) // 2
            # 计算可直接用于攻击的坐标
            attack_x = primary_x
            attack_y = primary_y - 25

            # 检查是否位于 禁止命中区域
            is_ingore = is_ingore_rebel(attack_x,attack_y)
            
            if (attack_x, attack_y) in rebel_coords or is_ingore: 
                print(f" ({attack_x}, {attack_y}) 坐标重复。 {is_ingore} 在禁止区域内")
                continue

            sort_key = calculate_distance((attack_x,attack_y),GAME_CENTER_LOCATION['location'])
            rebel_coords.append((attack_x, attack_y , sort_key))
            # 调试使用
            # pyautogui.moveTo(attack_x, attack_y, 2)
            # print(f"移动成功，找到叛军: ({attack_x}, {attack_y})")

        if rebel_coords == []:
            print(f"未找到符合条件的 {level_path} 叛军")
            return (None,None)
        
        # 按sort_key排序，使距离中心点最近的叛军排在前面
        # print('排序前:', rebel_coords)
        rebel_coords = sorted(rebel_coords, key=lambda x: x[2])
        #(int(rebel_coords[0][0]), int(rebel_coords[0][1]))
        # print('排序后:', rebel_coords)
        return (int(rebel_coords[0][0]), int(rebel_coords[0][1])) 

    except ImageNotFoundException:
        # 完全未找到匹配项时进入此分支
        print(f"未找到: {search_level} 叛军")
        all_locations = None
        return (None,None)
        
    except Exception as e:
        # 其他异常处理（如截图失败、路径错误等）
        print(f"发生未知错误: {str(e)}")
        return (None,None)




def is_back_home():
    """
    Purpose: 检查地图是否还在圣域，如果在就继续，不在返回主城所在位置
    """
    holy_place_region = (620, 230, 120, 50)
    holy_place_path = 'chrome_automation_project/diguo/location/holy_place.png'
    is_in_holy_place = image_center_location(holy_place_path,primary_region_to_screen_region( holy_place_region,PRIMARY_MONITOR_INFO )) != (None, None)

    # 在圣域不用管，出了圣域需要回到主城
    if is_in_holy_place:
        return False
    else:
        print("回到主城")
        global DIRECTION_LIST_INDEX
        DIRECTION_LIST_INDEX = DIRECTION_LIST_INDEX + 1
        search_and_click_image(click_type='back_home', clicks=1, interval=0.2, duration=0.2)
        return True

# 攻击叛军选择将领坐标
GENERALS_SEARCH = [(520,369,310,70), (520,369 + 71 * 1,310,70), (520,369 + 71 * 2,310,70), (520,369 + 71 * 3,310,70)]

def choice_attack_genelral_new(num=1):
    """
    返回值为 True 代表将领就绪
    reload_list 补兵按钮坐标集合
    generals_list 将领坐标集合
    TODO: 多人选择逻辑
    """
    select_path = f'chrome_automation_project/diguo/generals/select.png'
    rest_available_path = f'chrome_automation_project/diguo/generals/available.png'
    unavailable_path = f'chrome_automation_project/diguo/generals/unavaliable.png'
    reload_button_path = 'chrome_automation_project/diguo/generals/reload.png'

    generals_list = [(734,400),(734,470),(734,540),(734,610)]
    ## 补兵按钮
    reload_list = [(790,425),(790,495),(790,565),(790,635)]
    '''
    1号位置四个坐标
    (520,369) (830,369)
    (520,440) (830,440)
    '''    
    # 按顺序找到第一个处于休息状态的将领
    all_rest = []

    while all_rest == []:
        # 检测将领是否就绪
        #####  打开页面之后检测是否有选中将领，不管有没有都取消选中
        is_select = image_center_location(select_path)
        if is_select != (None, None):
            #print("取消默认将领")
            pyautogui.click(x=is_select[0], y=is_select[1],duration=0.2, clicks=1, interval=0.2)
        
        for index, a in enumerate(GENERALS_SEARCH[0:num]):
            rest_location = image_center_location(rest_available_path,primary_region_to_screen_region(a,PRIMARY_MONITOR_INFO))
            if rest_location != (None, None):
                all_rest = [rest_location[0] , rest_location[1], index]
                #print("找到第： ", index + 1 ," 个将领")
                # 找到可用将领之后退出循环
                break

        if all_rest == []:
            print("无可用将领，等待回兵。。。")
            # 攻击之后选择等待将领就绪页面直接消失，这里应该是检测是否还在攻击页面，如果是，就继续，如果不是就结束这个函数
            if not is_attack_page_alive():
                return False
            sleep(3)
        
    pyautogui.click(x=all_rest[0],y=all_rest[1],duration=0.2, clicks=1, interval=0.2)
    return True

# 将领补兵坐标
GENERALS_RELOAD = [(515,405,325,75), (515,480,325,75), (515,550,325,75), (515,625,325,75)]
def reload_rebel(num):
    """
    Purpose: 补兵
    1号位置四个坐标
    (520,369) (830,369)
    (520,440) (830,440)
    """
    # 英雄页面补兵按钮坐标
    reload_list = [(793,459),(793,532),(793,603),(793,676)]

    # 四个将领的搜索区域，目前只给一个
    search_and_click_image(click_type='hero_select', clicks=2, interval=0.2, duration=0.2)
    for reload_location in reload_list[0:num]:
        pyautogui.click(x=reload_location[0], y=reload_location[1],duration=0.2, clicks=1, interval=0.2)
    # 退出补兵将领页面
    while image_center_location( image_path=get_click_type_path('oncall') ) != (None, None):
        search_and_click_image(click_type='backspace', clicks=1, interval=0.2, duration=0.2)
    return 1


def is_attack_page_alive():
    """
    查看攻打叛军页面是否正常还在，如果还在说明攻击失败，那么取消攻击
    :return: True 页面还在， False 完成攻击动作
    """
    sleep(0.5)
    level_path = f'chrome_automation_project/diguo/rebel/info/attack_page.png'
    location = image_center_location(image_path=level_path,confidence=0.8)        
    page_alive = location != (None, None)
    #print("攻击失败：", page_alive)
    return page_alive

def attack_rebel(coords,level,num):
    """
    攻击叛军，这个函数只承担攻击的功能, 给一个坐标，然后过去攻击，可能成功也可能失败
    :param coords: 叛军坐标元组 (x, y) 或 None
    :return: 这里只需要返回攻击状态就可以 
    """
    if coords is None:
        #print("未找到叛军，无法攻击")
        return 0
    
    # 点击进入叛军页面
    pyautogui.click( x=coords[0], y=coords[1] ,button='left', clicks=1, interval=0.2, duration=0.3)
    # 点击就加入攻击过位置
    get_attacked_locations(coords)

    # 错误点击区域地图适配
    region_map = 'chrome_automation_project/diguo/region_map.png'
    is_click_region_map = image_center_location(image_path=region_map,confidence=0.9) != (None, None)        
    if is_click_region_map:
        print("点击错误区域地图，取消攻击")        
        search_and_click_image(click_type='backspace', clicks=1, interval=0.2, duration=0.2)
        drag_screen(direction=DIRECTION_LIST[DIRECTION_LIST_INDEX % 8])
        return 0

    # 叛军身份判断，判断是否是该等级叛军
    if is_aim_rebel(level):
        #print("找到叛军，开始攻击")
        # 添加进攻按钮点击功能
        search_and_click_image(click_type ='reble_info_attack', clicks=1, interval=0.2, duration=0.2)
        # 选择主将
        choice_attack_genelral_new(num)

        # 确认攻击
        search_and_click_image(click_type='rel_attack', clicks=1, interval=0.2, duration=0.2)

        global REBEL_ATTACKED_NUMBER
        REBEL_ATTACKED_NUMBER = REBEL_ATTACKED_NUMBER + 1

        if is_attack_page_alive():
            print("攻击错误，取消攻击")
            search_and_click_image(click_type='reble_info_cancel', clicks=1, interval=0.2, duration=0.2)
            return 0

        return 1
    else:
        # 找错了，要取消，点击取消按钮
        print("找到的叛军不是目标叛军，取消攻击")
        search_and_click_image(click_type='reble_info_cancel', clicks=1, interval=0.2, duration=0.2)
        return 0



# 清剿叛军逻辑
def cycle_attack(send_rebel_list,num):
    """
    Purpose: 清剿叛军
    : send_rebel_list: 叛军等级列表，可以传入多个等级
    : num 代表打的次数
    """

    return_login_exit()

    rebel_list = sorted(send_rebel_list, reverse=True)
    #print("当前需要清剿的叛军等级：",rebel_list)

    for i in rebel_list:
        location = search_best_rebel(i)
        #print("找到 ", i ," 的叛军坐标：",location)
        if location != (None,None):
            rebel_location_list = ( location, i )
            break
        else:
            rebel_location_list = ((None,None),None)
    
    rebel_locaiton = rebel_location_list[0]
    rebel_level = rebel_location_list[1]

    if rebel_locaiton == (None, None):
        #print("未找到叛军，移动屏幕")
        # 点击到了资源采集
        get_resource = 'chrome_automation_project/diguo/get_resource/get_resource.png'
        is_click_get_resource = image_center_location(image_path=get_resource,confidence=0.9) != (None, None)        
        if is_click_get_resource:
            #print("点击到了资源采集，取消攻击")
            search_and_click_image(click_type='cancel_get_resource', clicks=1, interval=0.2, duration=0.2)
        # 增加异常处理 ，退出攻打叛军页面
        search_and_click_image(click_type='exit', clicks=1, interval=0.2, duration=0.2)
        drag_screen(direction=DIRECTION_LIST[DIRECTION_LIST_INDEX % 8])    
        global ATTACKED_LOCATIONS
        ATTACKED_LOCATIONS=[]
        if rebuild_and_back_to_holy_place(active=True):
            reload_rebel(num)
        sleep(1)
        # 拖动鼠标之后上一个叛军还是会被选中
        #移动后需要 判断是否还在圣域
        is_back_home()  
    else:
        attack_rebel(rebel_locaiton,rebel_level,num)
        

def main(attack_num,send_rebel_list=[26,27],num=4,is_active=False):
    """
    Purpose: test the python file
    """
    
    # get_dock_order(is_active)
    pre_order_time = datetime.now()

    # reload_rebel(num)    
    while REBEL_ATTACKED_NUMBER <= attack_num:
        #  判断是否在世界界面
        if image_center_location(get_click_type_path('to_world')) != (None, None):
            search_and_click_image(click_type='to_world',clicks=2, interval=0.2, duration=0.2)
            sleep(2)
        # 重建城池
        #rebuild_main_city()
        # TODO：重构reload函数
        # if rebuild_main_city():
        #     reload_rebel(num)
        # 回工作地点 回圣域
        if not is_in_holy_place():
            return_login_exit()
            sleep(1)
            print("不在圣域") 
            sleep(1)
            # 这里回圣域的功能，出现被重建卡住的情况
            return_to_holy_place(active=True)        
        # 攻打叛军
        cycle_attack(send_rebel_list=send_rebel_list,num=num)
        print("当前时间:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "已攻击 ",REBEL_ATTACKED_NUMBER," 个叛军")

        # sleep(10)

        time_diff = datetime.now() - pre_order_time  # 得到timedelta对象
        total_seconds = time_diff.total_seconds()
        # 设置20分钟跑一次船
        if  total_seconds >= 30 * 60:
            get_dock_order(is_active)
            pre_order_time = datetime.now()
            global DIRECTION_LIST_INDEX
            DIRECTION_LIST_INDEX = DIRECTION_LIST_INDEX + 1





if __name__ == '__main__':
    #main(500,[26,27],4)
    #get_online_reward()
    # 178
    print("程序开始运行")
    sleep(10)
    #哥德
    #main(200,[22],1)
    # 红豆生南国 24 可以三个刷
    #main(350,[28,29],2,False)
    #main(350,[24,25,26,27,28,29],3,False)
    
    # 有
    #main(350,[28,29],2,False)
    
    main(350,[28,29],3,False)


    # ship()