ATTACKED_LOCATIONS=[]

def get_attacked_locations( rebel_location ):
    """
    获取已经攻击过的叛军坐标列表
    """
    global ATTACKED_LOCATIONS
    x , y = rebel_location
    for index, i in enumerate(ATTACKED_LOCATIONS):
        b_x , b_y = i
        ATTACKED_LOCATIONS[index] = (2 * b_x - x, 2 * b_y - y)

    ATTACKED_LOCATIONS.append(rebel_location)

    print("已攻击过目标：", ATTACKED_LOCATIONS, "总数量：", len(ATTACKED_LOCATIONS))
    return ATTACKED_LOCATIONS
