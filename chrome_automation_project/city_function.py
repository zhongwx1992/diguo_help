
import sys
from time import sleep
import pyautogui
from package.screen import search_and_click_image,image_center_location,get_click_type_path,GAME_CENTER_LOCATION,image_center_location_all
from pyautogui import moveTo, click
from login_service import return_login_exit
from task_timer import TASK_SHIP, TASK_HONORS, TASK_STRENGTH, TASK_STUDY, TASK_BATTLE, TASK_ONLINE, can_run, mark_success, reset
from package.ocr_util import get_character_info




def get_online_reward(is_free_ads=False):
    """
    Purpose: 实现获取在线奖励的功能 ,
    点击在线奖励->获取奖励->确认奖励->退出奖励
    """
    ## 判断主城状态 
    return_login_exit()        
    search_and_click_image(click_type='to_city',clicks=2, interval=0.2, duration=0.2)
    sleep(2)
    online_reward_position = image_center_location(get_click_type_path('online_reward'))
    if online_reward_position[0] is None or online_reward_position[1] is None:
        print("无在线奖励")
        search_and_click_image(click_type='to_world',clicks=2, interval=0.2, duration=0.2)
        return False
    moveTo(online_reward_position[0], online_reward_position[1], 0.1)
    click(online_reward_position[0], online_reward_position[1], button='left', clicks=2, interval=0.2, duration=0.2)
    sleep(1)

    # 判断是否成功进入在线奖励主界面
    online_reward_main_page_position = image_center_location(get_click_type_path('online_reward_main_page'))
    if online_reward_main_page_position[0] is None or online_reward_main_page_position[1] is None:
        print("点击失败，无在线奖励主页面")
        search_and_click_image(click_type='to_world',clicks=2, interval=0.2, duration=0.2)
        return False

    last_diamond_position = (775, 730)
    get_online_reward_position = image_center_location(get_click_type_path('get_online_reward'))
    # 没有免广告，且点击到的是最后一个带钻石的奖励按钮
    if is_free_ads is False and get_online_reward_position[1] == last_diamond_position[1]:
        print("预留最后一个带钻石的双倍奖励。")
        # search_and_click_image(click_type='get_online_reward',clicks=2, interval=0.2, duration=0.2)
    else:
        search_and_click_image(click_type='get_online_reward',clicks=2, interval=0.2, duration=0.2)
        ### 这里点击之后可能跳出双倍领取提示，需要判断
        sleep(2)
        double_reward_position = image_center_location(get_click_type_path('double_reward'))
        if double_reward_position[0] is not None and double_reward_position[1] is not None:
            moveTo(double_reward_position[0], double_reward_position[1], 0.1)
            click(double_reward_position[0], double_reward_position[1], button='left', clicks=2, interval=0.2, duration=0.2)
            print("双倍领取成功")
            sleep(1)

        # 需要点空地址，确认领取 
        pyautogui.click(x=GAME_CENTER_LOCATION['location'][0]+200, y=GAME_CENTER_LOCATION['location'][1] ,clicks=2)
        sleep(0.5)         

    ## 需要增加一个判断，判断在线奖励是否退出 
    exit_online_reward_position = image_center_location(get_click_type_path('exit_online_reward'))
    while exit_online_reward_position[0] is not None and exit_online_reward_position[1] is not None:
        search_and_click_image(click_type='exit_online_reward',clicks=2, interval=0.2, duration=0.2)
        exit_online_reward_position = image_center_location(get_click_type_path('exit_online_reward'))
        sleep(0.5)

    search_and_click_image(click_type='to_world',clicks=2, interval=0.2, duration=0.2)
    sleep(1)
    mark_success(TASK_ONLINE)
    return True



def rebuild_city():
    """
    Purpose: 重建城市
    """
    search_and_click_image(click_type='rebuild_city',clicks=1, interval=0.2, duration=0.2)
    search_and_click_image(click_type='rebuild_city_confirm',clicks=1, interval=0.2, duration=0.2)
    return True

def attack_status_check():
    """
    Purpose: 检查被攻击状态
    """
    attack_status_position = image_center_location(get_click_type_path('attack_my_city'))
    if attack_status_position[0] is not None and attack_status_position[1] is not None:
        print("被攻击")
        return True
    else:
        print("未被攻击")
        return False

def fix_click_library_red_book_location(click_type):
    """
    Purpose: 修复图书馆红书碎片和断简坐标距离
    """
    location = image_center_location( get_click_type_path(click_type),confidence=0.8) 
    if location == (None, None):
        print(f"未识别到{click_type}")
        return None
    else:
        print(f"识别到{click_type}坐标为 ({location[0]}, {location[1] + 60})")    
        pyautogui.moveTo(location[0], location[1] + 60)
        pyautogui.click(clicks=2)
        sleep(1)

        ### 在这里增加断简数量不足判断


        pyautogui.click(x=GAME_CENTER_LOCATION['location'][0] + 300, y=GAME_CENTER_LOCATION['location'][1],clicks=2)
        sleep(0.2)
        return (location[0], location[1] + 60)


def get_free_honors(buy_bamboo_slip=False, buy_red_book_debris=False):
    """
    Purpose: 获取免费荣誉

    :param red_book_bamboo_slip: 是否花费 8000 荣誉购买断简
    :param red_book_debris: 是否花费 13000 荣誉购买红书碎片
    """

    if not can_run(TASK_HONORS, cooldown_seconds=3600):
        return False

    ## 判断主城状态 
    return_login_exit()        
    search_and_click_image(click_type='to_city',clicks=2, interval=0.2, duration=0.2)
    sleep(1)
    rebuild_city()
    center_x, center_y = GAME_CENTER_LOCATION['location']
    # 移动鼠标到屏幕中心
    pyautogui.moveTo(center_x,center_y, duration=0.2)
    pyautogui.mouseDown(button='left')
    pyautogui.dragRel(300, 150, duration=0.5, button='left')
    pyautogui.mouseUp(button='left')
    sleep(1)

    library_location = image_center_location( get_click_type_path('library'),confidence=0.8)
    if library_location == (None, None):
        print("未找到图书馆")
        ## 增加退出城市的功能
        search_and_click_image(click_type='to_world',clicks=2, interval=0.2, duration=0.2)
        return False
    search_and_click_image(click_type='library',clicks=2, interval=0.2, duration=0.2)
    sleep(1)
    search_and_click_image(click_type='book_shop',clicks=1, interval=0.2, duration=0.2)
    sleep(1)
    search_and_click_image(click_type='buy_book',clicks=1, interval=0.2, duration=0.2)
    sleep(1)
    search_and_click_image(click_type='free_get',clicks=1, interval=0.2, duration=0.2)
    sleep(1)
    if image_center_location( get_click_type_path('red_book_bamboo_slip'), confidence=0.8) != (None, None) and buy_bamboo_slip:
        fix_click_library_red_book_location('red_book_bamboo_slip')
        ### 需要增加断简不足情况处理逻辑
    if image_center_location( get_click_type_path('red_book_debris'),confidence=0.8) != (None, None) and buy_red_book_debris:
        fix_click_library_red_book_location('red_book_debris')

    # 增加广告免费刷新逻辑
    if image_center_location( get_click_type_path('free_ad_refresh'),confidence=0.8) != (None, None):
        search_and_click_image(click_type='free_ad_refresh',clicks=2, interval=0.2, duration=0.2)
        sleep(1)
        search_and_click_image(click_type='free_get',clicks=2, interval=0.2, duration=0.2)
        sleep(1)
        if image_center_location( get_click_type_path('red_book_bamboo_slip'),confidence=0.8) != (None, None) and buy_bamboo_slip:   
            fix_click_library_red_book_location('red_book_bamboo_slip')
        if image_center_location( get_click_type_path('red_book_debris'),confidence=0.8) != (None, None) and buy_red_book_debris:
            fix_click_library_red_book_location('red_book_debris')

    back_space_location = image_center_location( get_click_type_path('back_space'),confidence=0.8)
    while back_space_location != (None, None):
        search_and_click_image(click_type='back_space',clicks=1, interval=0.2, duration=0.2)
        back_space_location = image_center_location( get_click_type_path('back_space'),confidence=0.8)
        sleep(1)
    search_and_click_image(click_type='to_world',clicks=2, interval=0.2, duration=0.2)
    mark_success(TASK_HONORS)
    return True

def get_study_art(is_active=True, art_type=['琴室']):
    """
    才艺学习 - 支持一次学习多个才艺类型

    :param is_active: 是否启用该函数，False 时直接跳过不执行
    :param art_type: str 或 list[str]，可选值：琴室 棋室 书房 画廊
                     例：'琴室' 或 ['琴室', '棋室'] 或 ['琴室','棋室','书房','画廊']
    :return: True=成功 False=失败/未启用
    """
    

    print(f"【才艺学习】is_active={is_active}, art_type={art_type}")    

    if not is_active:
        print("【才艺学习】is_active=False，跳过")
        return False

    ART_TYPE_LIST = ['琴室', '棋室', '书房', '画廊']

    # 兼容单字符串输入，统一转 list
    if isinstance(art_type, str):
        art_types = [art_type]
    else:
        art_types = list(art_type)

    # 校验所有输入类型是否合法
    invalid = [t for t in art_types if t not in ART_TYPE_LIST]
    if invalid:
        print(f"无效的才艺类型: {invalid}，可选值: {ART_TYPE_LIST}")
        return False

    if not can_run(TASK_STUDY, cooldown_seconds=65 * 60):
        return False

    return_login_exit()
    sleep(1)
    search_and_click_image(click_type='to_city',clicks=2, interval=0.2, duration=0.2)
    sleep(1)
    rebuild_city()
    sleep(1)
    search_and_click_image(click_type='palace',clicks=2, interval=0.2, duration=0.2)
    sleep(2)
    # 进入才艺坊
    search_and_click_image(click_type='art',clicks=1, interval=0.2, duration=0.2)
    sleep(1)

    # 确定已经进入才艺访
    art_main_page_position = image_center_location(get_click_type_path('art_main_page'))
    if art_main_page_position[0] is None or art_main_page_position[1] is None:
        print("未进入才艺坊")
        search_and_click_image(click_type='art_back_space',clicks=2, interval=0.2, duration=0.2)
        sleep(1)
        search_and_click_image(click_type='to_world',clicks=2, interval=0.2, duration=0.2)
        sleep(1)
        return False

    center_x, center_y = GAME_CENTER_LOCATION['location']
    # 移动鼠标到屏幕中心
    pyautogui.moveTo(center_x,center_y, duration=0.2)
    pyautogui.mouseDown(button='left')
    pyautogui.dragRel(0, -150, duration=0.5, button='left')
    pyautogui.mouseUp(button='left')
    sleep(1)

    ## 先点击领取， 可能会有多个领取按钮，需要判断是否有多个领取按钮
    get_art_result_position = image_center_location(get_click_type_path('get_art_result'))
    while get_art_result_position[0] is not None and get_art_result_position[1] is not None:
        moveTo(get_art_result_position[0], get_art_result_position[1], 0.1)
        click(get_art_result_position[0], get_art_result_position[1], button='left', clicks=2, interval=0.2, duration=0.2)
        sleep(1)
        #search_and_click_image(click_type='get_art_result',clicks=1, interval=0.2, duration=0.2)
        print("领取成功")
        # 需要点空地址，确认领取 
        pyautogui.click(x=GAME_CENTER_LOCATION['location'][0], y=GAME_CENTER_LOCATION['location'][1] ,clicks=2)
        sleep(1)
        pyautogui.click(x=GAME_CENTER_LOCATION['location'][0], y=GAME_CENTER_LOCATION['location'][1] ,clicks=2)
        get_art_result_position = image_center_location(get_click_type_path('get_art_result'))

    ### 才艺学习按钮硬编码参考坐标（x 相同，按 y 从上到下）
    STUDY_BUTTON_POSITIONS = {
        '琴室': (768, 313),
        '棋室': (768, 469),
        '书房': (768, 624),
        '画廊': (768, 780),
    }
    Y_TOLERANCE = 80  # y 轴容差像素，用于判断某个房间的按钮是否可见

    # 获取屏幕上当前可见的所有 study 按钮（去重后）
    learned_count = 0
    visible_locations = image_center_location_all(get_click_type_path('study'))
    if visible_locations == (None, None):
        print(f"没有可以学习的才艺按钮，跳过学习")
        visible_locations = []
    else:
        print(f"屏幕上检测到 {len(visible_locations)} 个可见 study 按钮: {visible_locations}")
        # 逐个学习用户指定的才艺
        for art in art_types:
            ref_x, ref_y = STUDY_BUTTON_POSITIONS[art]

            # 匹配：在可见按钮中找 y 坐标落在该房间参考范围内的
            matched_pos = None
            for (vx, vy) in visible_locations:
                if abs(vy - ref_y) <= Y_TOLERANCE:
                    matched_pos = (vx, vy)
                    break

            if matched_pos is None:
                print(f"⚠️ {art} 按钮未找到（可能正在学习中），跳过")
                continue

            print(f"开始学习 {art}，坐标 {matched_pos}")
            moveTo(matched_pos[0], matched_pos[1], 0.1)
            click(matched_pos[0], matched_pos[1], button='left', clicks=2, interval=0.2, duration=0.2)
            sleep(1)
            # 选择快速选择
            search_and_click_image(click_type='choice_beauty', clicks=1, interval=0.2, duration=0.2)
            sleep(1)
            # 确认学习
            search_and_click_image(click_type='last_study', clicks=2, interval=0.2, duration=0.2)
            sleep(1)
            # 退出学习界面（只点 1 次，避免把才艺坊也退了）
            search_and_click_image(click_type='exit_study', clicks=1, interval=0.2, duration=0.2)
            sleep(1)
            learned_count += 1
            print(f"✓ 已完成学习: {art}")
        
    search_and_click_image(click_type='art_back_space', clicks=2, interval=0.2, duration=0.2)
    sleep(1)
    search_and_click_image(click_type='art_back_space', clicks=2, interval=0.2, duration=0.2)
    sleep(1)
    search_and_click_image(click_type='to_world', clicks=2, interval=0.2, duration=0.2)
    sleep(1)
    if learned_count > 0:
        mark_success(TASK_STUDY)
        return True
    print("【才艺学习】本次没有实际学习任何才艺，不记录冷却")
    return False

def get_dock_order(is_active=False,materials='橙'):
    """
    Purpose: 跑船，根据材料类型选择不同的材料
    Args:
        is_active (bool, optional): 是否激活开船功能。 Defaults to False.
        materials (str, optional): 材料类型，橙色或红色。 Defaults to '橙' '紫' '蓝' '红'.
    """

    if not is_active:
        return 0
    return_login_exit()
    search_and_click_image(click_type='to_city',clicks=2, interval=0.2, duration=0.2)
    sleep(1)
    rebuild_city()
    find_dock = False
    max_dock_retry = 3  # 🔴 限制最多拖动寻找 3 次
    dock_retry = 0
    while not find_dock and dock_retry < max_dock_retry:
        dock_location = image_center_location( get_click_type_path('dock'),confidence=0.8)

        if dock_location != (None, None):
            print("找到船坞")
            search_and_click_image(click_type='dock',clicks=2, interval=0.2, duration=0.2)
            sleep(1)            
            if image_center_location( get_click_type_path('dock_source'),confidence=0.8) != (None, None):
                ## 领取资源，空点即可
                pyautogui.click(x=GAME_CENTER_LOCATION['location'][0], y=GAME_CENTER_LOCATION['location'][1] ,clicks=2)
                sleep(1)                    
            find_dock = True
        else:
            print(f"未找到船坞，第 {dock_retry + 1}/{max_dock_retry} 次拖动查找")

            in_city =  image_center_location( get_click_type_path('to_world'),confidence=0.8)
            if in_city == (None, None):
                print("不在主城内，退出开船函数")
                return 0

            center_x, center_y = GAME_CENTER_LOCATION['location']
            # 移动鼠标到屏幕中心
            pyautogui.moveTo(center_x,center_y, duration=0.2)
            pyautogui.mouseDown(button='left')
            pyautogui.dragRel(-300, 150, duration=0.5, button='left')
            pyautogui.mouseUp(button='left')
            sleep(1)
            dock_retry += 1

    if not find_dock:
        print(f"已拖动寻找 {max_dock_retry} 次仍未找到船坞，退出")
        search_and_click_image(click_type='to_world',clicks=2, interval=0.2, duration=0.2)
        center_x, center_y = GAME_CENTER_LOCATION['location']
        pyautogui.moveTo(center_x,center_y, duration=0.2)
        return 0

    search_and_click_image(click_type='dock',clicks=2, interval=0.2, duration=0.2)
    sleep(1)
    # 进入船坞
    search_and_click_image(click_type='dock_in',clicks=1, interval=0.2, duration=0.2)
    sleep(1)
    ### 增加购买操作
    # 购买按钮坐标，键为颜色
    buy_positions = {
        '蓝': (550, 293),
        '紫': (632, 292),
        '橙': (716, 293),
        '红': (798, 293),
    }
    click(buy_positions[materials])
    sleep(0.5)

    search_and_click_image(click_type='一键放置',clicks=2, interval=0.2, duration=0.2)
    ### 需要考虑图纸和资源不足时情况

    quit_dock_location = image_center_location( get_click_type_path('quit_dock'),confidence=0.8)
    while quit_dock_location != (None, None):    
        pyautogui.click(quit_dock_location[0], quit_dock_location[1], duration=0.2)
        quit_dock_location = image_center_location( get_click_type_path('quit_dock'),confidence=0.8)
        sleep(0.5)
    search_and_click_image(click_type='to_world',clicks=2, interval=0.2, duration=0.2)
    center_x, center_y = GAME_CENTER_LOCATION['location']
    pyautogui.moveTo(center_x,center_y, duration=0.2)

    mark_success(TASK_SHIP)
    return 1 

def rebuild_main_city():
    """
    Purpose: 检测是否被攻击 被攻击后重建主城
    """
    rebuild_main_citylocation = image_center_location( get_click_type_path('rebuild_main_city'),confidence=0.8)
    
    if rebuild_main_citylocation!= (None, None):
        print("重建主城")
        search_and_click_image(click_type='rebuild_main_city_confirm',clicks=2, interval=0.2, duration=0.2)
        return True
    else:
        #print("未被攻击")
        return False    


def get_every_battle():
    """
    Purpose:扫荡战役
    """
    if not can_run(TASK_BATTLE, cooldown_seconds=2 * 3600):
        return 0
    ## 判断主城状态 
    return_login_exit()        
    sleep(1)
    search_and_click_image(click_type='enter_battle',clicks=2, interval=0.2, duration=0.2)
    search_and_click_image(click_type='battle_position',clicks=2, interval=0.2, duration=0.2)
    search_and_click_image(click_type='clear_all_battle',clicks=2, interval=0.2, duration=0.2)
    search_and_click_image(click_type='real_battle_1',clicks=2, interval=0.2, duration=0.2)
    sleep(1)
    search_and_click_image(click_type='real_battle_2',clicks=2, interval=0.2, duration=0.2)
    ### 这里进去有两个可能，一个是成功扫荡，一个是没体力了，扫荡不了
    buy_energy_location = image_center_location( get_click_type_path('buy_energy'),confidence=0.8)
    swept = buy_energy_location == (None, None)  # 未弹出购买体力界面说明本次扫荡成功
    battle_retry = 0  # 🔴 轮次限制，最多循环 4 次
    while buy_energy_location == (None, None) and battle_retry < 4:
        print("还有体力啦 ，继续干")
        search_and_click_image(click_type='back_to_real_battle_2',clicks=1, interval=0.2, duration=0.2) 
        sleep(1)
        search_and_click_image(click_type='real_battle_2',clicks=2, interval=0.2, duration=0.2)
        sleep(1)
        buy_energy_location = image_center_location( get_click_type_path('buy_energy'),confidence=0.8)
        battle_retry += 1
        swept = True
        search_and_click_image(click_type='exit_real_battle',clicks=2, interval=0.2, duration=0.2)


    print("进入购买体力界面 - 没体力啦")
    ## 退出体力购买界面
    search_and_click_image(click_type='exit_real_battle',clicks=2, interval=0.2, duration=0.2)
    sleep(1)
    ## 退出可能存在的返回按钮
    search_and_click_image(click_type='back_to_real_battle_2',clicks=1, interval=0.2, duration=0.2) 
    sleep(1)
    ## 退出扫荡选择上阵英雄界面

    battle_hero_page_location = image_center_location( get_click_type_path('battle_hero_page'),confidence=0.8)
    while battle_hero_page_location != (None, None):
        search_and_click_image(click_type='exit_real_battle',clicks=1, interval=0.2, duration=0.2)
        battle_hero_page_location = image_center_location( get_click_type_path('battle_hero_page'),confidence=0.8)
        sleep(1)
    else:
        print("未扫荡到英雄")
    search_and_click_image(click_type='exit_real_battle',clicks=1, interval=0.2, duration=0.2)
    sleep(1)
    ## 退出战役界面
    search_and_click_image(click_type='battle_back_space',clicks=1, interval=0.2, duration=0.2)
    sleep(1)
    if swept:
        mark_success(TASK_BATTLE)
        return 1
    print("【扫荡战役】本次没有体力，未执行扫荡，不记录冷却")
    return 0
    # 成功之后就是退出

def get_strength():
    """
    Purpose: 获取日常福利 体力
    'benefit'
    'back_space_benefit'
    'strength'
    """
    if not can_run(TASK_STRENGTH, cooldown_seconds=2 * 3600, time_windows=[(11, 15), (18, 22)]):
        return 0
    return_login_exit()
    search_and_click_image(click_type='to_city',clicks=2, interval=0.2, duration=0.2)
    sleep(1)
    rebuild_city()

    search_and_click_image(click_type='benefit',clicks=2, interval=0.2, duration=0.2)
    sleep(1)

    lip_times = 0
    strength_location = image_center_location( get_click_type_path('strength'),confidence=0.8)
    while strength_location == (None, None) and lip_times < 3:
        print("未找到体力")
        lip_times += 1
        ## 需要向右滑动屏幕，找到体力
        center_x, center_y = GAME_CENTER_LOCATION['location']
        # 移动鼠标到屏幕中心
        pyautogui.moveTo(center_x,center_y - 200, duration=0.2)
        pyautogui.mouseDown(button='left')
        pyautogui.dragRel(-150, 0, duration=0.5, button='left')
        pyautogui.mouseUp(button='left')
        strength_location = image_center_location( get_click_type_path('strength'),confidence=0.8)        

    def _exit_benefit():
        """退出福利界面回到世界"""
        loc = image_center_location(get_click_type_path('back_space_benefit'), confidence=0.8)
        while loc != (None, None):
            search_and_click_image(click_type='back_space_benefit', clicks=1, interval=0.2, duration=0.2)
            sleep(1)
            loc = image_center_location(get_click_type_path('back_space_benefit'), confidence=0.8)
        search_and_click_image(click_type='to_world', clicks=2, interval=0.2, duration=0.2)

    # 未找到体力入口：退出福利界面，不记录冷却
    if strength_location == (None, None):
        print("【领体力】未找到体力入口，跳过本次领取")
        _exit_benefit()
        return 0

    search_and_click_image(click_type='strength',clicks=2, interval=0.2, duration=0.2)
    sleep(1)

    # 没有免费领取按钮，说明当前时间段已领取过
    if image_center_location(get_click_type_path('get_free_strength'), confidence=0.8) == (None, None):
        print("【领体力】当前没有可免费领取的体力，跳过本次领取")
        _exit_benefit()
        return 0

    search_and_click_image(click_type='get_free_strength',clicks=2, interval=0.2, duration=0.2)
    sleep(1)
    pyautogui.click(x=GAME_CENTER_LOCATION['location'][0], y=GAME_CENTER_LOCATION['location'][1] ,clicks=2)
    sleep(1)
    _exit_benefit()

    mark_success(TASK_STRENGTH)
    # 领取体力成功后，扫荡战役立即可用，刷新其冷却
    reset(TASK_BATTLE)
    return 1



def get_login_character_info():
    """
    Purpose: 获取登录角色信息 
    return: 角色名称 role_name
    """
    ### 搜索领主信息页面， 如果找到 直接识别，没找到就持续点击头像，直到找到领主信息页面
    role_info_location = image_center_location( get_click_type_path('领主信息页面'),confidence=0.8)
    retry = 0
    max_retry = 20  # 🔴 限制最多点击头像 20 次，避免死循环
    while role_info_location == (None, None) and retry < max_retry:
        retry += 1
        print(f"未找到领主信息页面，重试 {retry}/{max_retry}")
        role_info_postion = (34, 196)
        pyautogui.moveTo(role_info_postion[0], role_info_postion[1], duration=0.2)
        pyautogui.click(x=role_info_postion[0], y=role_info_postion[1],clicks=2)
        sleep(0.5)
        role_info_location = image_center_location( get_click_type_path('领主信息页面'),confidence=0.8)

    if role_info_location == (None, None):
        print(f"重试 {max_retry} 次仍未找到领主信息页面，退出程序")
        sys.exit(0)

    sleep(1)

    login_character_info = get_character_info()
    # print(login_character_info)
    main_back_space_location = image_center_location( get_click_type_path('main_back_space'),confidence=0.8)
    while main_back_space_location != (None, None):
        pyautogui.moveTo(main_back_space_location[0], main_back_space_location[1], duration=0.2)
        pyautogui.click(x=main_back_space_location[0], y=main_back_space_location[1],clicks=2)
        main_back_space_location = image_center_location( get_click_type_path('main_back_space'),confidence=0.8)
        sleep(0.5)

    role_name = login_character_info['role_name']
    print(f"当前登录角色: {role_name}")
    return role_name





# ----------------------------
# 以下是未完成功能函数
# ----------------------------

def market_seach_and_click_goods(goods):
    """
    Purpose: 搜索并点击商品
    """
    goods_location = image_center_location( get_click_type_path(goods),confidence=0.8)
    if goods_location != (None, None):
        print( f"{goods} 已找到")
        ## y 坐标增加偏移量
        goods_location = (goods_location[0], goods_location[1] + 30)
        # pyautogui.click(x=goods_location[0], y=goods_location[1],clicks=2)

        # 以 goods_location 为中心，Y 轴偏移 15，X 轴偏移 40，构建二次确认区域
        left_top = (goods_location[0] - 40, goods_location[1] - 15)
        right_bottom = (goods_location[0] + 40, goods_location[1] + 15)
        # 两个对角点 → 标准 (x, y, 宽, 高) 区域
        double_check_region = (
            left_top[0],
            left_top[1],
            right_bottom[0] - left_top[0],
            right_bottom[1] - left_top[1],
        )

        pyautogui.moveTo(left_top[0], left_top[1], duration=0.2) 
        sleep(2)
        pyautogui.moveTo(right_bottom[0], right_bottom[1], duration=0.2)
        ### 需要增加一个二次确认的逻辑，确认是支付对应的商品，否则会点击错误的商品，支付更高的代价
        ### 根据偏移的坐标，构建一个搜索区域，在这个区域内找到对应的支付商品，来进行二次验证

        sleep(2)  
        ### 测试使用

        confirm_exchange_page_location = image_center_location( get_click_type_path('confirm_exchange_page'),confidence=0.8)
        if confirm_exchange_page_location != (None, None):
            print("确认兑换界面已找到。")
            #search_and_click_image(click_type='confirm_purchase',clicks=2, interval=0.2, duration=0.2,confidence=0.8)
            pyautogui.click(x=GAME_CENTER_LOCATION['location'][0], y=GAME_CENTER_LOCATION['location'][1] ,clicks=1)
        else:
            print("确认兑换界面未找到。")
        
        return 1
    else:
        print( f"{goods} 未找到")    
        return 0


def get_market():
    """
    Purpose: 获取市场
    'market'
    """
    return_login_exit()
    search_and_click_image(click_type='to_city',clicks=2, interval=0.2, duration=0.2)
    sleep(1)
    rebuild_city()

    center_x, center_y = GAME_CENTER_LOCATION['location']
    # 移动鼠标到屏幕中心
    pyautogui.moveTo(center_x,center_y, duration=0.2)
    pyautogui.mouseDown(button='left')
    pyautogui.dragRel(-150, 150, duration=0.5, button='left')
    pyautogui.mouseUp(button='left')
    sleep(0.5)
    search_and_click_image(click_type='market',clicks=2, interval=0.2, duration=0.2,confidence=0.8)
    sleep(0.5)

    search_and_click_image(click_type='business_man',clicks=1, interval=0.2, duration=0.2,confidence=0.8)

    close_time_location = image_center_location( get_click_type_path('close_time'),confidence=0.8)
    if close_time_location != (None, None):
        print("流浪商人已离开！")

    else:
        print("流浪商人未离开！")
        ### 先找第一圈
        goods_list = [
                        'pay_stone_1400'
                        ,'pay_stone_20000','pay_stone_32000','pay_stone_3500','pay_stone_48000'
                        ,'pay_diamond_44'
                        ,'pay_food_8000','pay_food_16000','pay_food_35000'
                        #,'pay_food_800000'
                    ]
        for goods in goods_list:
            market_seach_and_click_goods(goods)

        ### 找完之后看有没有免费刷新

        refresh_market_location = image_center_location( get_click_type_path('refresh_free'),confidence=0.8)

        if refresh_market_location != (None, None):
            print("有免费刷新")
            
            pyautogui.moveTo(refresh_market_location[0],refresh_market_location[1], duration=0.2)
            pyautogui.click(x=refresh_market_location[0], y=refresh_market_location[1] ,clicks=1)
            ### 免费刷新完，然后再找一次商品
            sleep(1)
            for goods in goods_list:
                market_seach_and_click_goods(goods)
                
        else:
            print("没有免费刷新, 看是否有付费刷新") 
            for i in range(2):
                print(f"第{i+1}次看是否有付费刷新")
                diamond_15_refresh_location = image_center_location( get_click_type_path('refresh_diamond_15'),confidence=0.8)
                if diamond_15_refresh_location != (None, None):
                    print("有付费刷新按钮！")
                    pyautogui.moveTo(diamond_15_refresh_location[0],diamond_15_refresh_location[1], duration=0.2)
                    pyautogui.click(x=diamond_15_refresh_location[0], y=diamond_15_refresh_location[1] ,clicks=1)
                    sleep(0.5)
                    ### 付费刷新完，然后再找一次商品 
                    confirm_pay_15_diamond_page_location = image_center_location( get_click_type_path('confirm_pay_15_diamond_page'),confidence=0.8)
                    if confirm_pay_15_diamond_page_location != (None, None):
                        confirm_pay_15_diamond_location = image_center_location( get_click_type_path('confirm_pay_15_diamond'),confidence=0.8)
                        pyautogui.moveTo(confirm_pay_15_diamond_location[0],confirm_pay_15_diamond_location[1], duration=0.2)
                        pyautogui.click(x=confirm_pay_15_diamond_location[0], y=confirm_pay_15_diamond_location[1] ,clicks=1)
                        sleep(0.5)
                        for goods in goods_list:
                            market_seach_and_click_goods(goods)
                    else:
                        print("不在确认付费刷新页面，无法点击。")

                else:
                    print("没有付费刷新按钮！ 退出循环")
                    break 
    ## 退出市场
    back_space_market_location = image_center_location( get_click_type_path('back_space_market'),confidence=0.8)
    while back_space_market_location != (None, None):
        search_and_click_image(click_type='back_space_market',clicks=1, interval=0.2, duration=0.2)
        sleep(1)
        back_space_market_location = image_center_location( get_click_type_path('back_space_market'),confidence=0.8)

    search_and_click_image(click_type='to_world',clicks=2, interval=0.2, duration=0.2)

    return 0
        

def get_figth_toushiji(direction='north'):
    """
    Purpose: 获取战斗任务, 现在的情况是不管输入哪个方向，都是能识别到投石机，但是分不清楚方向
    
    """
    toushiji_location = {'east':(240,250),'west':(260,250),'north':(250,260),'south':(250,240),'center':(250,250)}

    search_and_click_image(click_type=direction,clicks=2, interval=0.2, duration=0.2)
    
    return 1

# ----------------------------
# 以上是未完成功能函数
# ----------------------------


if __name__ == "__main__":
    #search_and_click_image(click_type='to_city',clicks=2, interval=0.2, duration=0.2)
    #sleep(1)
    # rebuild_main_city()
    # sleep(10)
    # get_dock_order(is_active=True,materials='橙')
    #get_study_art(True,['琴室','棋室','书房','画廊'])
    #get_free_honors(buy_bamboo_slip=True, buy_red_book_debris=True)
    #fix_click_library_red_book_location('red_book_bamboo_slip')
    #get_strength()
    

    get_login_character_info()
