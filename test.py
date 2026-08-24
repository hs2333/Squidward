import pyautogui
import time

# ==========================
# 基础设置
# ==========================

PLAY_X = 1281

# PyAutoGUI 使用左上角为原点
# 下面已经替你把 ScreenCoordinates 的坐标转换好了

NOTES = {
    # 最高一组
    "H1":   350,
    "H7":   385,
    "H6.5": 430,
    "H6":   480,
    "H5.5": 520,
    "H5":   560,
    "H4.5": 600,
    "H4":   630,
    "H3":   670,
    "H2.5": 720,
    "H2":   770,
    "H1.5": 820,

    # 中间的 1
    "M1":   850,

    # 最低一组
    "L7":   895,
    "L6.5": 930,
    "L6":   980,
    "L5.5": 1010,
    "L5":   1050,
    "L4.5": 1100,
    "L4":   1140,
    "L3":   1180,
    "L2.5": 1230,
    "L2":   1250,
    "L1.5": 1310,
    "L1":   1345,
}


# ==========================
# 基本操作
# ==========================

def move_to_note(note):
    """把鼠标移动到指定音高。"""
    y = NOTES[note]

    # duration 可以调小
    # 0 = 瞬间移动
    pyautogui.moveTo(PLAY_X, y, duration=0.03)


def tap(note, duration=0.3):
    """
    短吹一次
    duration = 吹完以后等多久再进行下一个音
    """
    move_to_note(note)

    pyautogui.press("space")

    time.sleep(duration)


def hold(note, duration):
    """持续吹奏一个音。"""

    move_to_note(note)

    # 避免接近游戏约5秒的强制喘气
    duration = min(duration, 4.5)

    pyautogui.keyDown("space")
    time.sleep(duration)
    pyautogui.keyUp("space")


def rest(duration):
    """休止"""
    time.sleep(duration)


# ==========================
# 开始
# ==========================

print("5 秒后开始！")
print("现在切换到《遗忘之海》窗口。")

for i in range(5, 0, -1):
    print(i)
    time.sleep(1)


# ==========================
# 测试
# ==========================

tap("L1", 0.4)
tap("L2", 0.4)
tap("L3", 0.4)
tap("L4", 0.4)
tap("L5", 0.4)
tap("L6", 0.4)
tap("L7", 0.4)

tap("M1", 0.4)

tap("H2", 0.4)
tap("H3", 0.4)
tap("H4", 0.4)
tap("H5", 0.4)
tap("H6", 0.4)
tap("H7", 0.4)

hold("H1", 1.0)

print("测试完成")