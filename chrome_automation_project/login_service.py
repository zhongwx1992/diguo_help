import re
import sys
from time import sleep
import pyautogui
from package.screen import search_and_click_image,image_center_location,get_click_type_path,GAME_CENTER_LOCATION
from task_timer import print_status


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



def login_again(role_server=968):
    """
    Purpose: 重新登录
    """
    ## 直接刷新网页 

    refresh_web_location = (94,97) 
    pyautogui.moveTo(refresh_web_location, duration=0.2)
    pyautogui.click()
    sleep(10)

    ## 检查是否有开服公告，有说明网页刷出来了，可以开始进入下一步，如果没有，那就继续重新刷网页 
    max_retries = 5
    retries = 0
    sleep_time = 10
    start_page_location = image_center_location( get_click_type_path('start_page'),confidence=0.8)     
    while start_page_location == (None, None) and retries < max_retries:
        retries += 1
        pyautogui.moveTo(refresh_web_location, duration=0.2)
        pyautogui.click()
        sleep(sleep_time)
        sleep_time += 3
        start_page_location = image_center_location( get_click_type_path('start_page'),confidence=0.8) 

    close_start_page_location = image_center_location( get_click_type_path('close_start_page'),confidence=0.8) 

    while close_start_page_location != (None, None):
        pyautogui.moveTo(close_start_page_location, duration=0.2)
        pyautogui.click()
        sleep(0.2)
        close_start_page_location = image_center_location( get_click_type_path('close_start_page'),confidence=0.8) 


    search_and_click_image(click_type='server_list',clicks=2, interval=0.2, duration=0.2)

    # server_list_location = image_center_location( get_click_type_path('server_list'),confidence=0.8) 
    # if server_list_location != (None, None):
    #     pyautogui.moveTo(server_list_location, duration=0.2)
    #     pyautogui.click()
    #     sleep(0.5)

    # 选大区
    role_server_path = f'chrome_automation_project/diguo/login/severs/{role_server}.png'    
    role_server_location = image_center_location( role_server_path,confidence=0.8) 

    if role_server_location == (None, None):
        ### 直接点击开始！
        print_status(f"未识别到大区 {role_server}，跳过选择大区") 

    else:
        pyautogui.moveTo(role_server_location, duration=0.2)
        pyautogui.click()
        sleep(0.5)
    # 增加识别是否选对了大区

    # 点击开始游戏
    search_and_click_image(click_type='start_game',clicks=2, interval=0.2, duration=0.2)
    sleep(2)
    
    exit_welcome_page_location = image_center_location( get_click_type_path('exit_welcome_page'),confidence=0.8) 
    
    while exit_welcome_page_location == (None, None):
        sleep(2)
        exit_welcome_page_location = image_center_location( get_click_type_path('exit_welcome_page'),confidence=0.8) 

    
    while exit_welcome_page_location != (None, None):
        pyautogui.moveTo(exit_welcome_page_location, duration=0.2)
        pyautogui.click()
        sleep(0.2)
        exit_welcome_page_location = image_center_location( get_click_type_path('exit_welcome_page'),confidence=0.8) 

    return 1 


# 登录全局配置：启动时由 main 从 role_config.py 的 login_info 分组写入
LOGIN_CONFIG = {
    'is_login_again': False,
    'login_interval': 60 * 10,
    'role_server': 968,
}


def set_login_config(**kwargs):
    """
    Purpose: 用 role_config.py 中的 login_info 更新全局登录配置
    :param kwargs: 只接收 LOGIN_CONFIG 中已知的键，其余（如账号密码）忽略
    """
    for key in LOGIN_CONFIG:
        if key in kwargs:
            LOGIN_CONFIG[key] = kwargs[key]


def return_login_exit(is_login_again=None, login_interval=None, role_server=None):
    """
    Purpose: 检测到返回登录图片时终止整个程序
    参数为 None 时使用全局登录配置（来源于 role_config.py 的 login_info）
    """
    if is_login_again is None:
        is_login_again = LOGIN_CONFIG['is_login_again']
    if login_interval is None:
        login_interval = LOGIN_CONFIG['login_interval']
    if role_server is None:
        role_server = LOGIN_CONFIG['role_server']

    return_to_login_location = image_center_location(get_click_type_path('return_to_login'), confidence=0.8)
    if return_to_login_location != (None, None):
        print("检测到返回登录界面.是否重新登录?:",is_login_again)
        if is_login_again:
            ### 等十分钟 重新登录
            sleep(login_interval)
            login_again(role_server)

        else:
            print_status("程序退出前任务状态")
            sys.exit(0)
    return 1


def refresh_web():
    """
    Purpose: 刷新网页
    """
    refresh_web_location = (94,97) 
    pyautogui.moveTo(refresh_web_location, duration=0.2)
    pyautogui.click()
    sleep(15)


if __name__ == "__main__":

    # 检查有没有出现重新登录按钮，有则重新登录


    # 刷新页面
    # refresh_web_location = (94,97) 
    # pyautogui.moveTo(refresh_web_location, duration=0.2)
    # pyautogui.click()
    # sleep(15)

    # 708 707 968
    login_again(role_server=968)



    # #刷新后 检测是否在开始游戏界面    
    # start_game_button = image_center_location( get_click_type_path('start_game_button'),confidence=0.8)
    # if start_game_button != (None, None):
    #     search_and_click_image(click_type='close_notice',clicks=2, interval=0.2, duration=0.2)
    #     sleep(1)        
    #     search_and_click_image(click_type='server_list',clicks=2, interval=0.2, duration=0.2)
    #     sleep(1)
    #     search_and_click_image(click_type='h705',clicks=2, interval=0.2, duration=0.2)
    #     sleep(1)
    #     search_and_click_image(click_type='start_game_button',clicks=2, interval=0.2, duration=0.2)
        
    #     if login_staus():
    #     #这里可能会登录失败，返回token过期，需要重新登录

    #     #判断一下，然后进入游戏
    #         print("登录失败，重新登录")

    