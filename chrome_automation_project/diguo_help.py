from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyautogui
import time
import os
import cv2
import numpy as np
from selenium.webdriver.chrome.service import Service


def change_working_directory(target_directory):
    """
    切换到指定的工作目录
    :param target_directory: 目标工作目录
    """
    print("当前工作目录:", os.getcwd())
    try:
        # 切换到指定工作目录
        os.chdir(target_directory)
        print(f"成功切换到工作目录: {os.getcwd()}")
    except FileNotFoundError:
        print(f"指定的目录 {target_directory} 不存在。")


def open_browser_and_page(chrome_driver_path, url):
    """
    打开 Chrome 浏览器并访问指定页面
    :param chrome_driver_path: ChromeDriver 的路径
    :param url: 要访问的页面 URL
    :return: 浏览器驱动对象
    """

    print("当前输入chrome_driver_path:", chrome_driver_path)

    service = Service(chrome_driver_path)

    # 创建 Chrome 浏览器实例
    #driver = webdriver.Chrome(service=service)
    driver = webdriver.Chrome()
    # 打开网页
    driver.get(url)
    # 最大化窗口，方便可视化交互
    driver.maximize_window()

    return driver


def perform_login(driver, account, password):
    """
    执行游戏登录操作
    :param driver: 浏览器驱动对象
    :param account: 游戏账号
    :param password: 游戏密码
    """
    try:
        # 输入账号
        account_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'input'))
        )
        account_input.send_keys(account)
        
        # 输入密码
        password_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'password-input'))
        )
        password_input.send_keys(password)
        
        # 点击同意协议
        agree_icon = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'i.icon-agree'))
        )
        agree_icon.click()
        
        # 点击登录按钮
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'button'))
        )
        login_button.click()
        
        print("游戏登录成功！")
        return True
    except Exception as e:
        print(f"游戏登录失败: {e}")
        return False


def find_and_attack_monster(monster_image_path, confidence=0.8):
    """
    查找并攻击怪物
    :param monster_image_path: 怪物图片路径
    :param confidence: 匹配置信度
    """
    try:
        # 查找怪物位置
        location = pyautogui.locateOnScreen(monster_image_path, confidence=confidence)
        if location:
            # 计算中心位置
            center_x, center_y = pyautogui.center(location)
            # 移动鼠标并点击
            pyautogui.moveTo(center_x, center_y, duration=0.5)
            pyautogui.click()
            print(f"成功攻击怪物！位置: ({center_x}, {center_y})")
            return True
        else:
            print("未找到怪物")
            return False
    except Exception as e:
        print(f"攻击怪物时出错: {e}")
        return False
        
import threading

# 全局状态变量
battle_paused = False


def auto_battle(monster_image_path, battle_count=300):
    """
    自动战斗主循环
    :param monster_image_path: 怪物图片路径
    :param battle_count: 战斗次数
    """
    global battle_paused
    
    # 启动控制线程
    control_thread = threading.Thread(target=control_loop)
    control_thread.daemon = True
    control_thread.start()
    
    for i in range(battle_count):
        while battle_paused:
            time.sleep(1)
            
        print(f"开始第 {i+1} 次战斗...")
        if find_and_attack_monster(monster_image_path):
            # 等待战斗完成
            time.sleep(5)
        else:
            # 如果没有找到怪物，等待2秒后继续寻找
            time.sleep(2)


def control_loop():
    """
    控制循环，监听用户输入
    """
    global battle_paused
    
    print("\n输入 'pause' 暂停战斗，'resume' 继续战斗\n")
    
    while True:
        cmd = input().strip().lower()
        if cmd == "pause":
            battle_paused = True
            print("战斗已暂停")
        elif cmd == "resume":
            battle_paused = False
            print("战斗已继续")


def main():
    target_directory = '/Users/zhongwenxin/Documents/git_zhong/diguo_help/chrome_automation_project'
    chrome_driver_path = '/Users/zhongwenxin/Documents/git_zhong/diguo_help/chrome-mac-arm64/chromedriver'
    game_url = 'https://webgame.tuanyx.com/2002292#/auth/login'
    account = 'vg1720318984'
    password = '555666'
    monster_image = '/Users/zhongwenxin/Documents/git_zhong/diguo_help/chrome_automation_project/diguo/H706.png'
    battle_count = 300

    # 切换工作目录
    change_working_directory(target_directory)

    # 打开浏览器和游戏页面
    driver = open_browser_and_page(chrome_driver_path, game_url)

    # 执行登录操作
    if perform_login(driver, account, password):
        # 等待游戏加载
        time.sleep(5)
        
        # 开始自动战斗
        auto_battle(monster_image, battle_count)
    
    # 使用输入等待
    input("按回车键关闭浏览器...")
    driver.quit()


if __name__ == "__main__":
    main()