import schedule
import time
import subprocess
import sys
import os
from datetime import datetime

# ================= 配置区域 =================

# Python 解释器路径 (通常用 sys.executable 即可获取当前环境的 python)
PYTHON_EXE = sys.executable

# 脚本文件名 (确保这些文件在同一目录下，或者填绝对路径)
DOWNLOAD_SCRIPT = "download_economist.py"
EMAIL_SCRIPT = "send_email.py"

# 文件保存目录
OUTPUT_DIR = "downloads"


# ===========================================

def run_task():
    print(f"\n⏰ [任务启动] 当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # --- 1. 执行下载任务 ---
    print(f"⬇️  开始运行下载脚本...")

    # 构建命令: python download_economist.py --latest -o "downloads"
    download_cmd = [
        PYTHON_EXE,
        DOWNLOAD_SCRIPT,
        "--latest",
        "-o", OUTPUT_DIR
    ]

    try:
        # subprocess.run 会等待脚本执行完毕
        # check=False 允许脚本报错而不抛出 Python 异常，让我们自己处理 returncode
        result = subprocess.run(download_cmd, capture_output=False, text=True)

        # --- 2. 判断结果并执行邮件任务 ---
        if result.returncode == 0:
            print("✅ 下载任务执行成功 (返回码 0)。")
            print("📧 准备执行邮件发送脚本...")

            # 构建命令: python send_email.py --dir "downloads"
            email_cmd = [
                PYTHON_EXE,
                EMAIL_SCRIPT,
                "--dir", OUTPUT_DIR
            ]

            email_result = subprocess.run(email_cmd, capture_output=False, text=True)

            if email_result.returncode == 0:
                print("✅ 全流程结束：下载并发送成功。")
            else:
                print("⚠️ 下载成功，但邮件发送脚本报错。")

        else:
            print(f"⛔ 下载任务失败 (返回码 {result.returncode})。")
            print("🚫以此取消邮件发送任务。")

    except Exception as e:
        print(f"❌ 调度器发生内部错误: {e}")

    print(f"💤 任务结束，等待下个周六...\n")


# --- 设置定时任务 ---
# 每周六 20:00 运行
schedule.every().saturday.at("20:00").do(run_task)
# schedule.every().sunday.at("14:46").do(run_task)

# 测试模式 (取消注释下面这行，运行脚本后会立即执行一次，用于测试是否配置正确)
# run_task()

print(f"🚀 自动调度器已启动 (PID: {os.getpid()})")
print(f"📅 计划任务: 每周六 20:00 执行下载并发送")
print("⏳ 正在后台守候 (请勿关闭此窗口)...")

while True:
    schedule.run_pending()
    time.sleep(60)  # 每分钟检查一次时间
