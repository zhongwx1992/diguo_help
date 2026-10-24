
from re import S
from time import sleep
import pyautogui
from package.screen import search_and_click_image,image_center_location,get_click_type_path,GAME_CENTER_LOCATION,image_center_location_all
from pyautogui import moveTo, click
from login_service import return_login_exit




def get_online_reward():
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

    search_and_click_image('get_online_reward',clicks=1, interval=0.2, duration=0.2,confidence=0.8)
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
    sleep(1)         

    ## 需要增加一个判断，判断在线奖励是否退出 
    online_reward_main_page_position = image_center_location(get_click_type_path('online_reward_main_page'))
    while online_reward_main_page_position[0] is not None and online_reward_main_page_position[1] is not None:
        search_and_click_image(click_type='exit_online_reward',clicks=2, interval=0.2, duration=0.2)
        online_reward_main_page_position = image_center_location(get_click_type_path('online_reward_main_page'))
        sleep(1)

    sleep(1)
    search_and_click_image(click_type='to_world',clicks=2, interval=0.2, duration=0.2)
    sleep(1)
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



def get_free_honors(buy_duanjian=False, buy_hongshu=False):
    """
    Purpose: 获取免费荣誉

    :param buy_duanjian: 是否花费 8000 荣誉购买断简
    :param buy_hongshu: 是否花费 13000 荣誉购买红书碎片
    """


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
    sleep(2)

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
    if image_center_location( get_click_type_path('pay_honors_8000'),confidence=0.8) != (None, None) and buy_duanjian:
        search_and_click_image(click_type='pay_honors_8000',clicks=2, interval=0.2, duration=0.2)

        ### 需要增加断简不足情况处理逻辑
        sleep(1)
    if image_center_location( get_click_type_path('pay_honors_13000'),confidence=0.8) != (None, None) and buy_hongshu:
        search_and_click_image(click_type='pay_honors_13000',clicks=2, interval=0.2, duration=0.2)
        sleep(1)

    # 增加广告免费刷新逻辑
    if image_center_location( get_click_type_path('free_ad_refresh'),confidence=0.8) != (None, None):
        search_and_click_image(click_type='free_ad_refresh',clicks=2, interval=0.2, duration=0.2)
        sleep(1)
        search_and_click_image(click_type='free_get',clicks=2, interval=0.2, duration=0.2)
        sleep(1)
        if image_center_location( get_click_type_path('pay_honors_8000'),confidence=0.8) != (None, None) and buy_duanjian:
            search_and_click_image(click_type='pay_honors_8000',clicks=2, interval=0.2, duration=0.2)
            sleep(1)
        if image_center_location( get_click_type_path('pay_honors_13000'),confidence=0.8) != (None, None) and buy_hongshu:
            search_and_click_image(click_type='pay_honors_13000',clicks=2, interval=0.2, duration=0.2)
            sleep(1)


    search_and_click_image(click_type='back_space',clicks=2, interval=0.2, duration=0.2)
    sleep(1)
    search_and_click_image(click_type='back_space',clicks=2, interval=0.2, duration=0.2)
    sleep(2)
    search_and_click_image(click_type='to_world',clicks=2, interval=0.2, duration=0.2)
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
            print(f"✓ 已完成学习: {art}")
        
    search_and_click_image(click_type='art_back_space', clicks=2, interval=0.2, duration=0.2)
    sleep(1)
    search_and_click_image(click_type='art_back_space', clicks=2, interval=0.2, duration=0.2)
    sleep(1)
    search_and_click_image(click_type='to_world', clicks=2, interval=0.2, duration=0.2)
    sleep(1)
    return True

def get_dock_order(is_active=False):
    """
    Purpose: 跑船
    """
    # 找到船坞
    #dock_location = image_center_location( get_click_type_path('dock'),confidence=0.8)

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

    while True:
        get_order = image_center_location( get_click_type_path('dock_get_order'),confidence=0.8)
        if get_order != (None, None):
            search_and_click_image(click_type='dock_get_order',clicks=1, interval=0.2, duration=0.2)
            # 橙色订单坐标
            pyautogui.click(x=715,y=399,clicks=2)

            paper_use_out_location = image_center_location( get_click_type_path('paper_use_out'),confidence=0.8)
            if paper_use_out_location != (None, None):
                print("图纸用完，退出开船函数")
                search_and_click_image(click_type='exit_order',clicks=1, interval=0.2, duration=0.2,confidence=0.8)
                sleep(1)
                # search_and_click_image(click_type='quit_dock',clicks=1, interval=0.2, duration=0.2,confidence=0.8)
                # sleep(1)
                break

            search_and_click_image(click_type='dock_get_order_confirm',clicks=1, interval=0.2, duration=0.2,confidence=0.8)
            

            resource_status_location = image_center_location( get_click_type_path('resource_exhausted'),confidence=0.8)
            if resource_status_location != (None, None):
                search_and_click_image(click_type='cancel_order',clicks=1, interval=0.2, duration=0.2,confidence=0.8)
                sleep(1)
                search_and_click_image(click_type='exit_order',clicks=1, interval=0.2, duration=0.2,confidence=0.8)
                sleep(1)
                break            
            print("获取订单成功")


        else:
            center_x, center_y = GAME_CENTER_LOCATION['location']
            pyautogui.moveTo(center_x,center_y, duration=0.2)
            pyautogui.mouseDown(button='left')
            pyautogui.dragRel(0, -300, duration=0.5, button='left')
            pyautogui.mouseUp(button='left')
            sleep(1)
            get_order = image_center_location( get_click_type_path('dock_get_order'),confidence=0.8)
            if get_order == (None, None):
                break

    ### 所有都填满之后记得退出船坞 TODO: 添加退出船坞
    # in_dock = image_center_location( get_click_type_path('in_dock'),confidence=0.8) 
    while image_center_location( get_click_type_path('in_dock'),confidence=0.8) != (None, None):    
        search_and_click_image(click_type='quit_dock',clicks=1, interval=0.2, duration=0.2,confidence=0.8)
        sleep(1)

    search_and_click_image(click_type='to_world',clicks=2, interval=0.2, duration=0.2)
    center_x, center_y = GAME_CENTER_LOCATION['location']
    pyautogui.moveTo(center_x,center_y, duration=0.2)

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
    battle_retry = 0  # 🔴 轮次限制，最多循环 4 次
    while buy_energy_location == (None, None) and battle_retry < 4:
        print("还有体力啦 ，继续干")
        search_and_click_image(click_type='back_to_real_battle_2',clicks=1, interval=0.2, duration=0.2) 
        sleep(1)
        search_and_click_image(click_type='real_battle_2',clicks=2, interval=0.2, duration=0.2)
        sleep(1)
        buy_energy_location = image_center_location( get_click_type_path('buy_energy'),confidence=0.8)
        battle_retry += 1
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
    return 1
    # 成功之后就是退出

def get_strength():
    """
    Purpose: 获取日常福利 体力
    'benefit'
    'back_space_benefit'
    'strength'
    """
    return_login_exit()
    search_and_click_image(click_type='to_city',clicks=2, interval=0.2, duration=0.2)
    sleep(1)
    rebuild_city()

    search_and_click_image(click_type='benefit',clicks=2, interval=0.2, duration=0.2)
    sleep(1)
    search_and_click_image(click_type='strength',clicks=2, interval=0.2, duration=0.2)
    sleep(1)
    search_and_click_image(click_type='get_free_strength',clicks=2, interval=0.2, duration=0.2)
    sleep(1)
    pyautogui.click(x=GAME_CENTER_LOCATION['location'][0], y=GAME_CENTER_LOCATION['location'][1] ,clicks=2)
    sleep(1)
    back_space_benefit_location = image_center_location( get_click_type_path('back_space_benefit'),confidence=0.8)
    while back_space_benefit_location != (None, None):
        search_and_click_image(click_type='back_space_benefit',clicks=1, interval=0.2, duration=0.2)
        sleep(1)
        back_space_benefit_location = image_center_location( get_click_type_path('back_space_benefit'),confidence=0.8)
    search_and_click_image(click_type='to_world',clicks=2, interval=0.2, duration=0.2)

    return 1


def get_market():
    """
    Purpose: 获取市场
    'market'
    """

    return 1
    


def get_figth_toushiji(direction='north'):
    """
    Purpose: 获取战斗任务, 现在的情况是不管输入哪个方向，都是能识别到投石机，但是分不清楚方向
    
    """
    toushiji_location = {'east':(240,250),'west':(260,250),'north':(250,260),'south':(250,240),'center':(250,250)}

    search_and_click_image(click_type=direction,clicks=2, interval=0.2, duration=0.2)
    
    return 1


if __name__ == "__main__":
    #search_and_click_image(click_type='to_city',clicks=2, interval=0.2, duration=0.2)
    #sleep(1)
    # get_online_reward()
    #rebuild_city()
    # rebuild_main_city()
    # sleep(10)
    # get_dock_order(TRUE)
    #get_study_art(True,['琴室','棋室','书房','画廊'])
    get_free_honors(buy_duanjian=True, buy_hongshu=True)

    # get_dock_order(True)
    #print(image_center_location( get_click_type_path('buy_energy'),confidence=0.8))
    # get_study_art(['书房'])
    # attack_status_check()
