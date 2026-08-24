import time
import pydirectinput

print("5秒后开始读取鼠标坐标，请切换到游戏")
time.sleep(5)

print("按 Ctrl+C 结束")

while True:
    x, y = pydirectinput.position()
    print(f"\rX={x:4d}, Y={y:4d}", end="")
    time.sleep(0.05)