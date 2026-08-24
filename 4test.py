import time
import pydirectinput

X = 855

# 从最高到最低的 25 个 Y 坐标
Y_VALUES = [
    230, 255, 285, 320, 345,
    370, 395, 420, 450, 485,
    510, 535, 565, 595, 620,
    650, 670, 700, 730, 760,
    790, 810, 835, 865, 900
]

print("7 秒后开始演奏 25 个音，请切换到《遗忘之海》")
time.sleep(7)

for i, y in enumerate(Y_VALUES, start=1):
    print(f"Playing note {i}/25: ({X}, {y})")

    # 瞬间移动到目标音高
    pydirectinput.moveTo(X, y, duration=0)

    # 给游戏一点时间读取新的鼠标位置
    time.sleep(0.08)

    # 吹一下
    pydirectinput.press("space")

    # 音与音之间的间隔
    time.sleep(0.35)

print("25 音测试完成")