"""
屏幕 OCR 识别工具（基于 PaddleOCR）

提供：
  - ocr_region(x, y, w, h) → 识别固定屏幕区域的文字
  - ocr_interactive() → 交互式选区域识别
  - extract_number(text) → 从识别结果中提取数字
  - find_text_position(keyword, region) → 在区域中找关键词坐标

依赖：
  pip install paddlepaddle paddleocr opencv-python pyautogui numpy
"""

import re
import numpy as np
import cv2
import pyautogui

# PaddleOCR 全局单例（初始化慢，只建一次）
_ocr_engine = None


def _get_ocr():
    """延迟初始化 PaddleOCR，避免 import 时就下载模型"""
    global _ocr_engine
    if _ocr_engine is None:
        from paddleocr import PaddleOCR
        _ocr_engine = PaddleOCR(
            lang='ch',
            use_doc_orientation_classify=False,
            use_doc_unwarping=False,
            use_textline_orientation=False,
        )
    return _ocr_engine


def ocr_region(x: int, y: int, w: int, h: int) -> list[dict]:
    """
    识别指定屏幕区域的文字

    :param x: 区域左上角 x
    :param y: 区域左上角 y
    :param w: 区域宽度
    :param h: 区域高度
    :return: [{'text': '...', 'confidence': 0.99, 'box': [[x1,y1],[x2,y2],[x3,y3],[x4,y4]]}, ...]
             无文字时返回空列表
    """
    # 1. 截图
    img = pyautogui.screenshot(region=(x, y, w, h))
    img_bgr = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    # 2. OCR
    ocr = _get_ocr()
    result = ocr.predict(img_bgr)

    # 3. 格式化输出
    texts = []
    if result and len(result) > 0:
        item = result[0]
        if 'rec_texts' in item:
            for text, score, box in zip(
                item['rec_texts'],
                item['rec_scores'],
                item.get('rec_polys', item.get('rec_boxes', []))
            ):
                texts.append({
                    'text': text,
                    'confidence': round(float(score), 4),
                    'box': box,  # 区域内的相对坐标
                })
    return texts


def ocr_fullscreen() -> list[dict]:
    """识别整个屏幕的文字"""
    w, h = pyautogui.size()
    return ocr_region(0, 0, w, h)


def ocr_interactive():
    """
    交互式选区域：按回车确认截图起点和终点，Esc 取消

    使用方法：
      1. 调用后，终端提示"将鼠标移到区域左上角，按回车"
      2. 移鼠标到目标位置 → 按回车
      3. 移鼠标到区域右下角 → 按回车
      4. 自动识别并打印结果
    """
    print("=" * 50)
    print("交互式 OCR 区域选择")
    print("将鼠标移到区域左上角，按回车（Ctrl+C 取消）")
    try:
        input()
        x1, y1 = pyautogui.position()
        print(f"  起点: ({x1}, {y1})")

        print("将鼠标移到区域右下角，按回车")
        input()
        x2, y2 = pyautogui.position()
        print(f"  终点: ({x2}, {y2})")
    except KeyboardInterrupt:
        print("\n已取消")
        return

    x, y = min(x1, x2), min(y1, y2)
    w, h = abs(x2 - x1), abs(y2 - y1)
    print(f"\n识别区域: x={x}, y={y}, w={w}, h={h}")

    results = ocr_region(x, y, w, h)
    if not results:
        print("(未识别到文字)")
    else:
        print(f"\n识别到 {len(results)} 个文本块：")
        for r in results:
            print(f"  [{r['confidence']:.2f}] {r['text']}")
    return results


# ---------- 游戏专用识别（区域坐标已标定）----------

def make_region(x1: int, y1: int, x2: int, y2: int, name: str = "region") -> tuple[int, int, int, int]:
    """
    通过两个对角点坐标标定识别区域

    支持任意顺序的两个点（左上+右下 或 左下+右上 等），自动规范化为 (x, y, w, h)

    :param x1: 第一个点 x
    :param y1: 第一个点 y
    :param x2: 第二个点 x
    :param y2: 第二个点 y
    :param name: 区域名称（仅日志用）
    :return: (x, y, w, h)
    """
    x, y = min(x1, x2), min(y1, y2)
    w, h = abs(x2 - x1), abs(y2 - y1)
    print(f"【{name}】 区域标定: ({x1},{y1}) → ({x2},{y2}) → x={x}, y={y}, w={w}, h={h}")
    return (x, y, w, h)


def make_region_from_four_corners(
    tl: tuple[int, int],
    bl: tuple[int, int],
    tr: tuple[int, int],
    br: tuple[int, int],
    name: str = "region",
) -> tuple[int, int, int, int]:
    """
    通过四个角点坐标标定识别区域

    :param tl: 左上角 (x, y)
    :param bl: 左下角 (x, y)
    :param tr: 右上角 (x, y)
    :param br: 右下角 (x, y)
    :param name: 区域名称（仅日志用）
    :return: (x, y, w, h)
    """
    xs = [tl[0], bl[0], tr[0], br[0]]
    ys = [tl[1], bl[1], tr[1], br[1]]
    x, y = min(xs), min(ys)
    w, h = max(xs) - min(xs), max(ys) - min(ys)
    print(f"【{name}】 区域标定: x={x}, y={y}, w={w}, h={h}")
    return (x, y, w, h)





def get_today_rebel_count() -> tuple[int | None, int | None]:
    """
    识别游戏 UI 上"今日已剿灭叛军: X/Y"的区域
    :return: (已剿灭数, 总上限) 如 (300, 300)；识别失败返回 (None, None)
    """
    REBEL_COUNT_REGION = make_region_from_four_corners(
        tl=(624, 612), bl=(623, 630), tr=(728, 612), br=(728, 630),
        name="今日已剿灭叛军",
    )

    x, y, w, h = REBEL_COUNT_REGION
    results = ocr_region(x, y, w, h)
    if not results:
        return None, None

    # 找包含"已剿灭"的文本
    target = find_text('已剿灭', results)
    if not target:
        # 没找到关键词，取第一个文本块试试
        target = results[0]

    text = target['text']

    print("原始文本:", text)
    
    # 匹配 "X/Y" 格式
    match = re.search(r'(\d+)\s*/\s*(\d+)', text)
    if match:
        return int(match.group(1)), int(match.group(2))

    # 兜底：只找第一个数字
    num = extract_number(text)
    return num, None


# ---------- 工具函数 ----------

def extract_number(text: str) -> int | float | None:
    """
    从 OCR 文字中提取数字（支持整数、小数、带单位的如 '365.89万'）

    :return: 纯数字值，或 None
    """
    # 去掉中文单位
    cleaned = re.sub(r'[万亿千万百个,]', '', text)
    # 找数字
    match = re.search(r'-?\d+\.?\d*', cleaned)
    if not match:
        return None
    val = match.group()
    return float(val) if '.' in val else int(val)


def extract_numbers(results: list[dict]) -> list[int | float | None]:
    """从 ocr_region 结果列表中批量提取数字"""
    return [extract_number(r['text']) for r in results]


def find_text(keyword: str, results: list[dict]) -> dict | None:
    """
    在 OCR 结果中查找包含关键词的文本块

    :param keyword: 要搜索的文字（支持子串匹配）
    :return: 匹配的文本块 dict，未找到返回 None
    """
    for r in results:
        if keyword in r['text']:
            return r
    return None


def find_all_text(keyword: str, results: list[dict]) -> list[dict]:
    """在 OCR 结果中查找所有包含关键词的文本块"""
    return [r for r in results if keyword in r['text']]


if __name__ == '__main__':
    # 快速测试：python -m package.ocr_util
    print("选一个区域测试一下...")
    # ocr_interactive()

    a = get_today_rebel_count()
    print("识别结果:", a)