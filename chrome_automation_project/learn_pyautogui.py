from math import fabs
import time
import pyautogui as pa

# 鼠标移动到这个位置 TODO：如果是多屏幕，这个如何处理？
pa.moveTo(100, 100, 0.5)
#pa.moveRel(100, 100)
# 屏幕分辨率    
pa.size()
# 鼠标位置
pa.position()

# 默认左键点击
pa.moveTo(100, 100)
time.sleep(1)   
pa.click()

pa.click(100, 100, button='left',clicks=2, interval=0.25, duration=0.25, tween=pa.linear, logScreenshot = False)
# 鼠标按住
pa.mouseDown(100, 100, button='left',tween=pa.linear)
pa.mouseUp(100, 100, button='left')

# 鼠标按住往上移动
pa.mouseDown(button='left')
time.sleep(0.25)
pa.moveRel(0, -100, duration=0.25)
pa.mouseUp(button='left')   

pa.screenshot('screenshot.png')

pa.alert("你好", title='提示', button='确定')

pa.prompt("请输入你的名字", title='提示', default='')

pa.locateAllOnScreen('click_dim.png', confidence=0.8)
pa.locateOnScreen('click_dim.png', confidence=0.8)
pa.locateOnWindow

x, y = pa.position()
# 实时获取鼠标当前位置
while True:
    # 鼠标移动到这个位置 TODO：如果是多屏幕，这个如何处理？
    #pa.moveTo(100, 100, 0.5)
    #pa.moveRel(100, 100)
    x1, y1 = pa.position()
    if x1 != x or y1!= y:
        x, y = x1, y1
        print("Mouse moved to: ", x1, y1)
        
