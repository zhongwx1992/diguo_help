from selenium import webdriver
from selenium.webdriver.common.by import By
import pyautogui
import time
import os

print("当前工作目录:", os.getcwd()) 
target_directory = '/Users/zhongwenxin/Documents/git_zhong/diguo_help/chrome_automation_project'
try:
    # 切换到指定工作目录
    os.chdir(target_directory)
    print(f"成功切换到工作目录: {os.getcwd()}")
except FileNotFoundError:
    print(f"指定的目录 {target_directory} 不存在。")


# 创建 Chrome 浏览器实例
driver = webdriver.Chrome()
# 打开网页
# driver.get('https://www.baidu.com')
driver.get('https://www.4399.com/flash/196157_4.htm')
# 最大化窗口，方便可视化交互
driver.maximize_window()

# 如果弹出需要输入账号密码，那么等待输入，并且检测账号密码输入完成后，点击登录按钮

try:
    # 查找登录按钮
    login_button = driver.find_element(By.ID, 'login')
    # 点击登录按钮
    login_button.click()
    print("登录操作执行成功！") 
except:
    print(f"执行登录操作时出现错误：{e}")   



# 这里可以添加更多的交互代码，例如查找搜索框并输入内容
try:
    # # 查找百度搜索框
    # search_box = driver.find_element(By.ID, 'kw')
    # # 在搜索框中输入关键词
    # search_box.send_keys('Python 自动化')
    # # 查找搜索按钮
    # search_button = driver.find_element(By.ID, 'su')
    # # 点击搜索按钮
    # search_button.click()
    # print("搜索操作执行成功！")

    location = pyautogui.locateOnScreen('click_dim.png', confidence=0.8)  # 查找图像
    print("地鼠: ", location)

except Exception as e:
    print(f"执行操作时出现错误：{e}")

# 等待一段时间以便查看效果
time.sleep(10)

# 使用输入等待
input("按回车键关闭浏览器...")
driver.quit()