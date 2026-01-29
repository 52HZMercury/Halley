import time
import subprocess
import sys
import os
from datetime import datetime
import yaml
import schedule

# 读取配置
with open("config.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

# 使用配置
PYTHON_EXE = sys.executable
DOWNLOAD_SCRIPT = config['paths']['download_script']
EMAIL_SCRIPT = config['paths']['email_script']
OUTPUT_DIR = config['paths']['output_dir']

def run_task():
    print(f"\n⏰ [任务启动] 当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # --- 1. 执行下载任务 ---
    print(f"⬇️  开始运行下载脚本: {DOWNLOAD_SCRIPT}...")
    download_cmd = [PYTHON_EXE, DOWNLOAD_SCRIPT, "--latest", "-o", OUTPUT_DIR]

    try:
        result = subprocess.run(download_cmd, capture_output=False, text=True)

        # --- 2. 判断结果并执行邮件任务 ---
        if result.returncode == 0:
            print("✅ 下载任务执行成功。📧 准备发送邮件...")
            email_cmd = [PYTHON_EXE, EMAIL_SCRIPT, "--dir", OUTPUT_DIR]
            email_result = subprocess.run(email_cmd, capture_output=False, text=True)

            if email_result.returncode == 0:
                print("✅ 全流程结束：下载并发送成功。")
            else:
                print("⚠️ 下载成功，但邮件发送脚本报错。")
        else:
            print(f"⛔ 下载任务失败 (返回码 {result.returncode})。已取消邮件任务。")

    except Exception as e:
        print(f"❌ 调度器发生内部错误: {e}")

    print(f"💤 任务结束，等待下个周期: {config['scheduler']['run_day']} {config['scheduler']['run_time']}...\n")

# --- 启动调度逻辑 ---
run_day = config['scheduler']['run_day']
run_time = config['scheduler']['run_time']

# 动态绑定 schedule
getattr(schedule.every(), run_day).at(run_time).do(run_task)

print(f"🚀 Halley 自动调度器已启动 (PID: {os.getpid()})")
print(f"📅 计划任务: 每周 {run_day} {run_time} 执行")
print("⏳ 正在后台守候 (请勿关闭此窗口)...")

# 【关键：事件循环】让程序持续运行
try:
    while True:
        run_task()  # 取消注释即可立即执行一次测试
        schedule.run_pending()
        time.sleep(60) # 每分钟检查一次
except KeyboardInterrupt:
    print("\n🛑 调度器已手动停止。")