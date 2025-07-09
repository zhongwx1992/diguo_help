
from time import sleep
import pyautogui
from package.region import primary_region_to_screen_region
from package.screen import PRIMARY_MONITOR_INFO,search_and_click_image,get_click_type_path


def is_in_holy_place():
    """
    Purpose: 判断地图是否在圣域
    :return: 在圣域返回 True 不在返回 False
    """
    holy_place_region = (620, 230, 120, 50)
    holy_place_path = get_click_type_path( 'holy_place')

    try:
        is_in_holy_place = pyautogui.locateOnScreen(
            holy_place_path, 
            confidence=0.8,  # 降低置信度
            region=primary_region_to_screen_region(holy_place_region, PRIMARY_MONITOR_INFO)
        ) is not None
        return is_in_holy_place
    except Exception as e:
        #print(f"不在圣域: {e}")
        return False

# def is_in_work_place(level:num):
#     """
#     Purpose: 判断地图是否在工作区
#     :return: 在工作区返回 True 不在返回 False
#     """
#     check_region = (620, 230, 120, 50)
#     work_place_path = get_click_type_path( 'work_place')
#     return False




def random_move():
    """
    Purpose: 随机迁城
    """
    # 打开背包
    # print("路径：", get_click_type_path('backpack'))    
    # print("坐标：", image_center_location(get_click_type_path('backpack')))    

    search_and_click_image(click_type='backpack',clicks=2, interval=0.2, duration=0.2)
    sleep(0.5)
    # 选择战斗
    search_and_click_image(click_type='backpack_attack',clicks=1, interval=0.2, duration=0.2)
    # 选择随机迁城
    search_and_click_image(click_type='random_move',clicks=1, interval=0.2, duration=0.2)
    # 使用随机迁城
    search_and_click_image(click_type='random_move_use',clicks=1, interval=0.2, duration=0.2)    

    # 这里需要加个容错，如果背包页面还打开，需要关闭一下背包
    search_and_click_image(click_type='backspace',clicks=1, interval=0.2, duration=0.2)    

    return True

def return_to_holy_place(active=True):
    """
    Purpose: 回到圣域
    """
    # 强制进入世界界面
    #search_and_click_image(click_type='to_world',clicks=2, interval=0.2, duration=0.2)
    #sleep(2)
    #print("是否在圣域：", is_in_holy_place())

    # 点击回城按钮
    search_and_click_image(click_type='back_home', clicks=1, interval=0.2, duration=0.2)

    while not is_in_holy_place() and active:  # 直接使用布尔值判断
        
        random_move()
        print("回到圣域中...")
        sleep(1)

    if not active:
        print("飞圣域功能未打开")
    else:
        print("回到圣域")
    return True

if __name__ == "__main__":
    # 测试代码
    # search_and_click_image(click_type='to_world',clicks=2, interval=0.2, duration=0.2)
    # sleep(2)

    print("是否在圣域：", is_in_holy_place())
    sleep(2)
    return_to_holy_place(active=True)
    
    #random_move()
    #search_and_click_image(click_type='attack_my_city',clicks=1, interval=0.2, duration=0.2)    

    


    