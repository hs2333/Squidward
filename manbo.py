import time
import pydirectinput

X = 855

Y_VALUES = [
    230, 255, 285, 320, 345,
    370, 395, 420, 450, 485,
    510, 535, 565, 595, 620,
    650, 670, 700, 730, 760,
    790, 810, 835, 865, 900
]

print("5 秒后开始")
time.sleep(5)

# 最高 -> 最低
print("Descending...")
for y in Y_VALUES:
    pydirectinput.moveTo(X, y, duration=0)
    time.sleep(0.08)
    pydirectinput.press("space")
    time.sleep(0.35)

time.sleep(1)

# 最低 -> 最高
print("Ascending...")
for y in reversed(Y_VALUES):
    pydirectinput.moveTo(X, y, duration=0)
    time.sleep(0.08)
    pydirectinput.press("space")
    time.sleep(0.35)

print("测试完成")