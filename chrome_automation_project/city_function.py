
from pickle import TRUE
from time import sleep
import pyautogui
from package.screen import search_and_click_image,image_center_location,get_click_type_path,GAME_CENTER_LOCATION



def get_online_reward():
    """
    Purpose: 领取在线奖励
    """
    search_and_click_image(click_type='to_city',clicks=2, interval=0.2, duration=0.2)
    sleep(1)

    search_and_click_image(click_type='online_reward',clicks=2, interval=0.2, duration=0.2,confidence=0.7)
    search_and_click_image(click_type='get_online_reward',clicks=1, interval=0.2, duration=0.2)
    search_and_click_image(click_type='online_reward_exit',clicks=2, interval=0.2, duration=0.2)


def rebuild_city():
    """
    Purpose: 重建城市
    """
    search_and_click_image(click_type='rebuild_city',clicks=1, interval=0.2, duration=0.2)
    search_and_click_image(click_type='rebuild_city_confirm',clicks=1, interval=0.2, duration=0.2)


def get_dock_order(is_active=False):
    """
    Purpose: 跑船
    """
    # 找到船坞
    #dock_location = image_center_location( get_click_type_path('dock'),confidence=0.8)

    if not is_active:
        return 0

    search_and_click_image(click_type='to_city',clicks=2, interval=0.2, duration=0.2)
    sleep(1)
    rebuild_city()
    find_dock = False
    while not find_dock:
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
            print("未找到船坞，重新查找 拖动屏幕")
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

    search_and_click_image(click_type='dock',clicks=2, interval=0.2, duration=0.2)
    sleep(1)
    # 进入船坞
    search_and_click_image(click_type='dock_in',clicks=1, interval=0.2, duration=0.2)
    # 获取订单 TODO: 这里需要加一个循环逻辑，把所有坑位都填满

    while True:
        get_order = image_center_location( get_click_type_path('dock_get_order'),confidence=0.8)
        if get_order != (None, None):
            search_and_click_image(click_type='dock_get_order',clicks=1, interval=0.2, duration=0.2)
            # 橙色订单坐标
            pyautogui.click(x=715,y=399,clicks=2)
            search_and_click_image(click_type='dock_get_order_confirm',clicks=1, interval=0.2, duration=0.2,confidence=0.8)
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

def ship():
    while True:
        get_dock_order(TRUE)
        sleep(120)


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




if __name__ == "__main__":
    #search_and_click_image(click_type='to_city',clicks=2, interval=0.2, duration=0.2)
    #sleep(1)
    #get_online_reward()
    #rebuild_city()
    # rebuild_main_city()
    sleep(10)
    # get_dock_order(TRUE)
