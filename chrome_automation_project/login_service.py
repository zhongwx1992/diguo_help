from time import sleep
import pyautogui
from package.screen import search_and_click_image,image_center_location,get_click_type_path,GAME_CENTER_LOCATION


def login_staus():
    """
    Purpose: 检测登录状态
    """
    return_to_login_location = image_center_location( get_click_type_path('return_to_login'),confidence=0.8) 

    if return_to_login_location!= (None, None):
        print("返回登录")
        search_and_click_image(click_type='return_to_login',clicks=2, interval=0.2, duration=0.2)
        return True
    else:    
        return False    



if __name__ == "__main__":

    # 检查有没有出现重新登录按钮，有则重新登录
    # login_staus()
    # sleep(10)

    # 刷新页面
    refresh_web_location = (94,97) 
    pyautogui.moveTo(refresh_web_location, duration=0.2)
    pyautogui.click()
    sleep(15)


    #刷新后 检测是否在开始游戏界面    
    start_game_button = image_center_location( get_click_type_path('start_game_button'),confidence=0.8)
    if start_game_button != (None, None):
        search_and_click_image(click_type='close_notice',clicks=2, interval=0.2, duration=0.2)
        sleep(1)        
        search_and_click_image(click_type='server_list',clicks=2, interval=0.2, duration=0.2)
        sleep(1)
        search_and_click_image(click_type='h705',clicks=2, interval=0.2, duration=0.2)
        sleep(1)
        search_and_click_image(click_type='start_game_button',clicks=2, interval=0.2, duration=0.2)
        
        if login_staus():
        #这里可能会登录失败，返回token过期，需要重新登录

        #判断一下，然后进入游戏
            print("登录失败，重新登录")