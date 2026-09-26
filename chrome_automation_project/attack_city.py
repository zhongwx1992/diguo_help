from pickle import TRUE
from time import sleep
import pyautogui
from package.screen import search_and_click_image,image_center_location,get_click_type_path,GAME_CENTER_LOCATION,image_center_location_all



def attack_city(city_name):
    """
    Purpose: 攻击城市
    """
    search_and_click_image(click_type=city_name,clicks=1, interval=0.2, duration=0.2)


if __name__ == "__main__":


    # 'yellow_arrow': 'chrome_automation_project/diguo/attack_city/yellow_arrows.png',
    # 'red_arrow': 'chrome_automation_project/diguo/attack_city/red_arrows.png',
    # 'blue_arrow': 'chrome_automation_project/diguo/attack_city/blue_arrows.png',


    # 获取屏幕截图
    # im = pyautogui.screenshot()
    # 获取特定坐标(x,y)的RGB颜色值
    # color = im.getpixel((100, 100))
    # print(f"坐标(100, 100)的颜色: {color}")

    # search_and_click_image(click_type='blue_arrow',clicks=1, interval=0.2, duration=0.2)

    # pyautogui.click(x=1200,y=240,clicks=2,interval=0.2,duration=0.2)
    # sleep(0.2)

    # loc = image_center_location(image_path=get_click_type_path('red_arrow'), confidence=0.8)
    # print( loc )

    # a = (538,278)
    # # 左侧边界： 515
    # # 右侧边界： 838
    # # 上边界： 388
    # # pyautogui.moveTo(x=838,y=278)
    # pyautogui.moveTo(x=515,y=368)
    loc = image_center_location(get_click_type_path('aim_city'),confidence=0.8 ) 
    print(loc)
    pyautogui.moveTo(x=loc[0],y=loc[1])
    sleep(1)
    pyautogui.click(x=loc[0],y=loc[1],clicks=3,interval=0.2,duration=0.2) 
    search_and_click_image(click_type='ready_attack_city',clicks=1, interval=0.2, duration=0.2)
    # loc = image_center_location_all(get_click_type_path('aim_city'),confidence=0.8 )
    # for item in loc:
    #     print(item)
    #     pyautogui.moveTo(x=item[0],y=item[1])
    #     sleep(1)
