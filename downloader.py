import requests
import os
import argparse
from datetime import datetime, timedelta
import sys
import yaml

# 基础URL配置
BASE_URL = "https://raw.githubusercontent.com/hehonghui/awesome-english-ebooks/master/01_economist"


def get_latest_saturday():
    """获取最近的一个周六的日期"""
    today = datetime.now()
    # weekday() 返回 0(周一) 到 6(周日)。周六是 5。
    # 计算当前日期距离上一个周六（或者今天就是周六）差几天
    days_to_subtract = (today.weekday() - 5) % 7
    latest_saturday = today - timedelta(days=days_to_subtract)
    return latest_saturday


def validate_date(date_str):
    """验证并解析日期字符串 (格式: YYYY.MM.DD)"""
    try:
        dt = datetime.strptime(date_str, "%Y.%m.%d")
        if dt.weekday() != 5:
            print(f"⚠️  警告: {date_str} 不是周六。The Economist 通常在周六发行，文件可能不存在。")
        return dt
    except ValueError:
        print("❌ 错误: 日期格式必须为 YYYY.MM.DD (例如: 2023.11.15)")
        sys.exit(1)


def download_file(date_obj, output_dir="."):
    with open("config.yaml", "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    """执行下载逻辑"""
    # 格式化日期字符串
    date_str = date_obj.strftime("%Y.%m.%d")

    # 构建目标 URL
    # 结构: .../te_2025.11.15/TheEconomist.2025.11.15.epub
    folder_name = f"te_{date_str}"
    file_name = f"TheEconomist.{date_str}.epub"
    url = f"{BASE_URL}/{folder_name}/{file_name}"

    print(f"🌐 正在尝试下载: {file_name}")
    print(f"🔗 链接: {url}")

    try:
        # 发送请求 (stream=True 用于大文件)
        proxies = config.get('proxy') # 直接获取整个代理字典
        response = requests.get(url, stream=True, timeout=30, proxies=proxies)
        # response = requests.get(url, stream=True, timeout=15)

        if response.status_code == 200:
            # 确保输出目录存在
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            output_path = os.path.join(output_dir, file_name)

            # 获取文件大小用于显示（可选）
            total_size = int(response.headers.get('content-length', 0))

            with open(output_path, 'wb') as f:
                downloaded = 0
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        # 简单的进度显示
                        if total_size > 0:
                            percent = int(downloaded / total_size * 100)
                            print(f"\r📥 下载进度: {percent}%", end="")

            print(f"\n✅ 下载成功! 文件已保存至: {output_path}")
        elif response.status_code == 404:
            print(f"\n❌ 错误 (404): 未找到该日期的文件。")
            print("   可能原因：")
            print("   1. 该日期的期刊尚未上传。")
            print("   2. 日期输入错误（请确认该日期是否为周六）。")
            # 【新增】返回非0状态码，告诉外部脚本“我失败了”
            sys.exit(1)
        else:
            print(f"\n❌ 下载失败，状态码: {response.status_code}")
            sys.exit(1)

    except requests.exceptions.RequestException as e:
        print(f"\n❌ 网络请求错误: {e}")
        print("   提示: 由于 GitHub Raw 在某些地区(如中国大陆)可能无法直接访问，你可能需要开启代理。")
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="下载 The Economist PDF")

    # 参数设置
    parser.add_argument("-d", "--date", type=str, help="指定日期，格式: YYYY.MM.DD (例如 2025.11.15)")
    parser.add_argument("-l", "--latest", action="store_true", help="自动下载最近的一个周六的期刊")
    parser.add_argument("-o", "--output", type=str, default=".", help="文件保存目录 (默认为当前目录)")

    args = parser.parse_args()

    target_date = None

    if args.date:
        target_date = validate_date(args.date)
    elif args.latest:
        target_date = get_latest_saturday()
        print(f"📅 自动检测到最近的周六为: {target_date.strftime('%Y.%m.%d')}")
    else:
        # 如果没有参数，默认询问用户输入
        input_str = input("请输入日期 (格式 YYYY.MM.DD) 或按回车下载最近一期: ").strip()
        if input_str:
            target_date = validate_date(input_str)
        else:
            target_date = get_latest_saturday()
            print(f"📅 自动选择最近的周六: {target_date.strftime('%Y.%m.%d')}")

    download_file(target_date, args.output)