import os
import time
import pandas as pd
import subprocess

# ---------- 配置参数 ----------
emulator_name = "emulator-5554"  # Android 模拟器设备名
apk_folder = "./apks"            # APK 文件夹路径
output_folder = "./experiment_data"  # 保存数据路径
apps = ["Telegram.apk", "WhatsApp.apk"]  # 示例 APK 列表
actions_per_app = 10  # 每个 app 模拟操作次数

# 创建输出文件夹
os.makedirs(output_folder, exist_ok=True)

# ---------- 工具函数 ----------
def install_apk(apk_path):
    subprocess.run(["adb", "-s", emulator_name, "install", "-r", apk_path], check=True)

def launch_app(package_name):
    subprocess.run(["adb", "-s", emulator_name, "shell", "monkey", "-p", package_name, "-c", "android.intent.category.LAUNCHER", "1"], check=True)

def enable_talkback():
    subprocess.run(["adb", "-s", emulator_name, "shell", "settings", "put secure enabled_accessibility_services com.google.android.marvin.talkback/.TalkBackService"], check=True)
    subprocess.run(["adb", "-s", emulator_name, "shell", "settings", "put secure accessibility_enabled 1"], check=True)

def perform_click(x, y):
    subprocess.run(["adb", "-s", emulator_name, "shell", "input", "tap", str(x), str(y)], check=True)

def perform_swipe(x1, y1, x2, y2, duration=300):
    subprocess.run(["adb", "-s", emulator_name, "shell", "input", "swipe", str(x1), str(y1), str(x2), str(y2), str(duration)], check=True)

def input_text(text):
    subprocess.run(["adb", "-s", emulator_name, "shell", "input", "text", text], check=True)

def take_screenshot(filename):
    local_path = os.path.join(output_folder, filename)
    subprocess.run(["adb", "-s", emulator_name, "shell", "screencap", "-p", f"/sdcard/{filename}"], check=True)
    subprocess.run(["adb", "-s", emulator_name, "pull", f"/sdcard/{filename}", local_path], check=True)

# ---------- 主实验流程 ----------
experiment_records = []

# 启用 TalkBack
enable_talkback()
time.sleep(2)

for apk_name in apps:
    apk_path = os.path.join(apk_folder, apk_name)
    install_apk(apk_path)
    package_name = apk_name.replace(".apk", "")
    launch_app(package_name)
    time.sleep(2)
    
    for i in range(actions_per_app):
        # 示例操作：点击 + 滑动 + 文本输入
        x, y = random.randint(100, 800), random.randint(100, 1600)
        perform_click(x, y)
        take_screenshot(f"{package_name}_click_{i}.png")
        
        perform_swipe(100, 1200, 100, 400)
        take_screenshot(f"{package_name}_swipe_{i}.png")
        
        input_text("test123")
        take_screenshot(f"{package_name}_input_{i}.png")
        
        # 记录数据
        experiment_records.append({
            "App": package_name,
            "Action_Index": i,
            "Click_Pos": (x, y),
            "Screenshots": [f"{package_name}_click_{i}.png", f"{package_name}_swipe_{i}.png", f"{package_name}_input_{i}.png"]
        })
    
    # 清理 app，便于下一个实验
    subprocess.run(["adb", "-s", emulator_name, "uninstall", package_name], check=True)

# 保存实验记录
df = pd.DataFrame(experiment_records)
df.to_excel(os.path.join(output_folder, "experiment_records.xlsx"), index=False)
print("实验数据已保存！")
