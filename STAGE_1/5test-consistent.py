import time
import pydirectinput

X = 855

LOW_Y = 900
HIGH_Y = 230

print("5 秒后开始测试，请切换到游戏")
time.sleep(5)

# 先移动到最低音
pydirectinput.moveTo(X, LOW_Y, duration=0)

# 等 2 秒，让游戏里的 UI 跟上
time.sleep(2)

print("开始长按并滑音")

# 按住空格
pydirectinput.keyDown("space")

# 从低音滑到高音
pydirectinput.moveTo(
    X,
    HIGH_Y,
    duration=2.0
)

# 稍微停一下
time.sleep(0.3)

# 再从高音滑回低音
pydirectinput.moveTo(
    X,
    LOW_Y,
    duration=2.0
)

# 松开空格
pydirectinput.keyUp("space")

print("测试完成")