import time
import pydirectinput

X = 1281

time.sleep(5)

# -------------------------
# 1. 测试鼠标移动
# -------------------------

# # 高音
# pydirectinput.moveTo(X, 800)
# time.sleep(2)

# # 中间
# pydirectinput.moveTo(X, 850)
# time.sleep(2)

# # 低音
# pydirectinput.moveTo(X, 900)
# time.sleep(2)

print("移动到高音位置")
pydirectinput.moveTo(X, 350)
time.sleep(1)

print("移动到中间位置")
pydirectinput.moveTo(X, 850)
time.sleep(1)

print("移动到低音位置")
pydirectinput.moveTo(X, 1345)
time.sleep(1)



# -------------------------
# 2. 测试鼠标左键点击
# -------------------------

print("测试左键点击")

pydirectinput.moveTo(X, 850)
time.sleep(0.5)

pydirectinput.click()

time.sleep(2)


# -------------------------
# 3. 测试空格短按
# -------------------------

print("测试空格短按")

pydirectinput.moveTo(X, 850)
time.sleep(0.5)

pydirectinput.press("space")

time.sleep(2)


# -------------------------
# 4. 测试空格长按
# -------------------------

print("测试空格长按 2 秒")

pydirectinput.moveTo(X, 850)
time.sleep(0.5)

pydirectinput.keyDown("space")
time.sleep(2)
pydirectinput.keyUp("space")

time.sleep(2)


# -------------------------
# 5. 测试连续点击
# -------------------------

print("测试连续点击")

pydirectinput.moveTo(X, 850)
time.sleep(0.5)

for _ in range(5):
    pydirectinput.click()
    time.sleep(0.15)

time.sleep(2)


# -------------------------
# 6. 测试连续空格
# -------------------------

print("测试连续空格")

for _ in range(5):
    pydirectinput.press("space")
    time.sleep(0.15)


print("测试完成")