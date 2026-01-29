import smtplib
import os
import glob
import argparse
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
import yaml


def find_latest_pdf(directory):
    """查找指定目录下最新的 epub 文件"""
    # 获取目录下所有 PDF
    search_path = os.path.join(directory, "*.epub")
    files = glob.glob(search_path)

    if not files:
        return None

    # 按修改时间排序，取最后一个 (最新的)
    latest_file = max(files, key=os.path.getctime)
    return latest_file


def send_email(file_path):
    with open("config.yaml", "r", encoding="utf-8") as f:
        conf = yaml.safe_load(f)['email']

    """发送带附件的邮件"""
    filename = os.path.basename(file_path)

    msg = MIMEMultipart()
    msg['From'] = conf['sender_email']
    # 1. 创建邮件对象
    # 设置邮件头：将列表转换为字符串 "a@b.com, c@d.com"
    # 这样收件人能看到这封邮件也是发给别人的
    msg['To'] = ", ".join(conf['receiver_emails'])

    msg['Subject'] = f"The Economist - {filename}"

    body = f"自动发送最新的 The Economist 期刊。\n文件名: {filename}\n发送时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    msg.attach(MIMEText(body, 'plain'))

    # 2. 添加正文 (可选)
    body = f"自动发送最新的 The Economist 期刊。\n文件名: {filename}\n发送时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    msg.attach(MIMEText(body, 'plain'))

    # 3. 添加附件
    try:
        with open(file_path, "rb") as attachment:
            # 创建 MIMEBase 对象
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())

        # 编码为 base64
        encoders.encode_base64(part)

        # 添加头部，定义文件名
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {filename}",
        )

        # 将附件挂载到邮件
        msg.attach(part)

        # 4. 连接服务器并发送
        print(f"📧 正在连接 SMTP 服务器 ({conf['smtp_server']})...")
        server = smtplib.SMTP(conf['smtp_server'], conf['smtp_port'])
        server.starttls()  # 启用安全传输
        server.login(conf['sender_email'], conf['sender_password'])

        # 发送邮件：sendmail 的第二个参数接受一个列表
        print(f"📤 正在群发邮件至: {conf['receiver_emails']}...")
        server.sendmail(conf['sender_email'], conf['receiver_emails'], msg.as_string())

        server.quit()
        print(f"✅ 群发成功! 文件: {filename}")

    except Exception as e:
        print(f"❌ 发送邮件失败: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="发送最新文件到邮箱")
    parser.add_argument("-d", "--dir", type=str, default=".", help="文件所在的目录 (默认为当前目录)")
    args = parser.parse_args()

    print(f"📂 正在目录 '{args.dir}' 中查找最新文件...")
    latest_pdf = find_latest_pdf(args.dir)

    if latest_pdf:
        print(f"📄 找到最新文件: {latest_pdf}")
        send_email(latest_pdf)
    else:
        print("❌ 未找到 epub 文件。请确认下载脚本是否执行成功。")