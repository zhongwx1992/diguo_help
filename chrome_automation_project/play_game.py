from time import sleep
import pyautogui
from package.region import primary_region_to_screen_region

from package.screen import search_and_click_image,get_click_type_path,image_center_location,PRIMARY_MONITOR_INFO,SCREEN_CENTER_INFO




#game_region = (516,267,323,540)
game_region = (1032, 534, 646, 1080)


step1 = (623, 362)


def search_and_hit_dishu():
    """
    Purpose: 实现选中图片中心位置进行点击等功能
    """
    while True:
        # # 优先点击高价值地鼠
        # for dish_type in ['dishu_3', 'dishu_2', 'dishu_1']:
        #     loc = image_center_location(get_click_type_path(dish_type), confidence=0.8, region=primary_region_to_screen_region(game_region,PRIMARY_MONITOR_INFO))
        #     if loc != (None, None):
        #         pyautogui.click(loc[0], loc[1], clicks=2, interval=0.1)
        #         break        
        search_and_click_image(click_type='dishu_3',clicks=2,interval=0.05, duration=0.01,confidence=0.7,region=game_region)
        search_and_click_image(click_type='dishu_2',clicks=2,interval=0.05, duration=0.01,confidence=0.7,region=game_region)
        search_and_click_image(click_type='dishu_1',clicks=2,interval=0.05, duration=0.01,confidence=0.7,region=game_region)

        #search_and_click_image(click_type='dishu_eyes',clicks=2,interval=0.05, duration=0.01,confidence=0.7,region=game_region)
        # if image_center_location(get_click_type_path('dishu_game_over'), confidence=0.8) != (None, None):
        #     print("游戏结束")
        #     break

def hit_dishu():
    # 检测开始游戏按钮
    start_loc = image_center_location(get_click_type_path('dishu_start_game'), confidence=0.8, region=game_region)
    if start_loc == (None, None):
        print("未找到开始游戏按钮")
        return False
        
    print("开始游戏")
    pyautogui.click(start_loc[0], start_loc[1], clicks=2, interval=0.2)
    #sleep(1)
    search_and_hit_dishu()
    return True

if __name__ == "__main__":
    # 测试代码
    #hit_dishu()
    #search_and_hit_dishu()
    # print(primary_region_to_screen_region(game_region,PRIMARY_MONITOR_INFO))

    #start_loc = image_center_location(get_click_type_path('dishu_start_game'), confidence=0.8, region=primary_region_to_screen_region(game_region,PRIMARY_MONITOR_INFO))
    # print( get_click_type_path('football_step1') )

    # print( image_center_location(get_click_type_path('football_step1'), confidence=0.8) )

    # 点击足球第一步
    # pyautogui.click(623, 362, clicks=2, interval=0.2)
    # sleep(2)
    # pyautogui.click(678, 702, clicks=1, interval=0.2)
    # sleep(3)
    # # pyautogui.click(676, 439, clicks=1000, interval=0.1)
    
    # pyautogui.click(x=676, y=439, clicks=1100, interval=0.075, button='left', duration=0.0)
    pyautogui.click(x=676, y=439, clicks=1100, interval=0.08, button='left', duration=0.0)

    # pyautogui.click(x=676, y=439, clicks=1600, interval=0.05, button='left', duration=0.0)

    # print( image_center_location(get_click_type_path('football_start_game'), confidence=0.8) )
    # pyautogui.moveTo(x=676, y=439)