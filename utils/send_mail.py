# -*- coding:utf-8 -*-
import zmail
from config.config import rc


def send_report():
    """
    发送报告
    :return:
    """
    with open(rc.REPORT_FILE, encoding='utf-8') as f:
        content_html = f.read()
    try:
        mail = {
            'from': '18021055980@163.com',
            'subject': '最新的测试报告邮件',
            'content_html': content_html,
            'attachments': [rc.REPORT_FILE, ]
        }
        server = zmail.server(*rc.EMAIL_INFO.values())
        server.send_mail(rc.ADDRESSEE, mail)
        print("测试邮件发送成功!")
    except Exception as e:
        print("Error: 无法发送邮件，{}!", format(e))


if __name__ == '__main__':
    """现在config.py文件设置邮箱账号和密码"""
    send_report()
