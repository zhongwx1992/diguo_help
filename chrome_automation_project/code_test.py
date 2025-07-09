import pyautogui
import time
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
# 新增导入语句
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ... existing code ...


url = 'https://www.baidu.com'

driver = webdriver.Chrome()
# 打开网页
driver.get(url)
# 最大化窗口，方便可视化交互
driver.maximize_window()


# 打印浏览器相关信息
print("浏览器名称:", driver.name)
print("浏览器版本:", driver.capabilities['browserVersion'])
print("当前页面的URL:", driver.current_url)
print("当前页面的标题:", driver.title)
# 打印浏览器窗口的尺寸
width, height = driver.get_window_size().values()
print(f"浏览器窗口尺寸: 宽度 {width}, 高度 {height}")
# 打印浏览器的用户代理信息
user_agent = driver.execute_script("return navigator.userAgent;")
print("浏览器用户代理信息:", user_agent)



"""
# 切换到新标签页
driver.switch_to.window(driver.window_handles[-1])
# 模拟打开新标签页
driver.execute_script("window.open('');")
# 切换到每个标签页并检查标题
for handle in driver.window_handles:
    driver.switch_to.window(handle)
    if driver.title == "百度":
        driver.close()
# 切换回剩余的第一个标签页
if driver.window_handles:
    driver.switch_to.window(driver.window_handles[0])
"""

diguo_url='https://webgame.tuanyx.com/2002292#/auth/login'

driver = webdriver.Chrome()
driver.get(diguo_url)
# 最大化窗口，方便可视化交互
driver.maximize_window()    

#driver.close()

account = driver.find_element(By.CLASS_NAME, 'input')
account.clear()
account.send_keys('vg1720318984')

# 定位密码输入框，通过类名定位
password = driver.find_element(By.CLASS_NAME, 'password-input')
password.send_keys('555666')



# 显式等待账号输入框加载完成
wait = WebDriverWait(driver, 20)
account = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'input')))
account.clear()
account.send_keys('vg1720318984')

# 显式等待密码输入框加载完成
password = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'password-input')))
password.send_keys('555666')

# 同意协议点击 TODO：这段代码有问题，点击之后会报错，暂时先跳过
try:
    # 使用 CSS 选择器定位元素
    agree_icon = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'i.icon-agree')))
    # 检查元素是否可见
    if agree_icon.is_displayed():
        # 点击元素以实现打勾选中
        agree_icon.click()
        print("成功点击同意图标")
    else:
        print("同意图标不可见，无法点击")
except Exception as e:
    print(f"点击同意图标时出现错误: {e}")



try:
    login_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'button')))
    # 点击登录按钮
    login_button.click()
    print("成功点击登录按钮")
except Exception as e:
    print(f"点击登录按钮时出现错误: {e}")