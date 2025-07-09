

def primary_region_to_screen_region(primary_region,primary):
    """
    将主显示器区域转换为屏幕区域
    :param primary_region: (x, y, width, height) 主显示器区域
    :param primary: (x, y, width, height) 主显示器信息
    :return: (x, y, width, height) 屏幕区域
    """
    #primary = PRIMARY_MONITOR_INFO
    g_a_x = primary_region[0]
    g_a_y = primary_region[1]
    g_a_w = primary_region[2]
    g_a_h = primary_region[3]

    g_b_x = g_a_x + g_a_w
    g_b_y = g_a_y + g_a_h

    screen_a_x = g_a_x * 2 + primary.x
    screen_a_y = g_a_y * 2 + primary.y
    screen_b_x = g_b_x * 2 + primary.x
    screen_b_y = g_b_y * 2 + primary.y

    screen_w = screen_b_x - screen_a_x
    screen_h = screen_b_y - screen_a_y

    screen_region = (screen_a_x, screen_a_y, screen_w, screen_h)
    return screen_region
