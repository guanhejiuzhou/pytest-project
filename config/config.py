import os
from selenium.webdriver.common.by import By
from utils.times import dt_strftime

# 返回脚本上两层目录路径
PRO_PATH = os.path.dirname(os.path.abspath(__file__))


class RunConfig(object):
    """
    运行测试配置
    """
    # 项目目录
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # 页面元素目录
    ELEMENT_PATH = os.path.join(BASE_DIR, 'page_element')

    # 报告文件
    REPORT_FILE = os.path.join(BASE_DIR, 'report.html')

    # 元素定位的类型
    LOCATE_MODE = {
        'css': By.CSS_SELECTOR,
        'xpath': By.XPATH,
        'name': By.NAME,
        'id': By.ID,
        'class': By.CLASS_NAME
    }

    # 邮件信息
    EMAIL_INFO = {
        'username': '18021055980@163.com',
        'password': 'CJMZQXCYQMHPKLNP',
        'smtp_host': 'smtp.163.com',
        'smtp_port': 465
    }

    # 收件人
    ADDRESSEE = {
        'L18021055980@126.com',
        '1255783906@qq.com'
    }

    # 创建只读属性，@property装饰器会将方法转换为相同名称的只读属性，可以与所定义的属性配合使用，防止属性被修改
    @property
    def log_file(self):
        """日志目录"""
        log_dir = os.path.join(self.BASE_DIR, 'logs')
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        return os.path.join(log_dir, '{}.log'.format(dt_strftime()))

    @property
    def screen_path(self):
        """截图目录"""
        screenshot_dir = os.path.join(self.BASE_DIR, 'screen_capture')
        if not os.path.exists(screenshot_dir):
            os.makedirs(screenshot_dir)
            now_time = dt_strftime("%Y%m%d%H%M%S")
            screen_file = os.path.join(screenshot_dir, "{}.png".format(now_time))
            return now_time, screen_file

    @property
    def ini_file(self):
        """配置文件"""
        ini_file = os.path.join(self.BASE_DIR, 'config', 'config.ini')
        if not os.path.exists(ini_file):
            raise FileNotFoundError("配置文件%s不存在！" % ini_file)
        return ini_file

    # 运行测试用例的目录或文件
    cases_path = os.path.join(PRO_PATH, 'test_dir')

    # 配置浏览器驱动类型
    driver_type = "chrome"

    # 配置运行的url
    url = "https://www.baidu.com"

    # 失败重跑次数
    rerun = "1"

    # 当达到最大失败数，停止执行
    max_fail = "5"

    # 浏览器驱动-不需要修改
    driver = None

    # 报告路劲-不需要修改
    NEW_REPORT = None


rc = RunConfig()
if __name__ == '__main__':
    print(rc.BASE_DIR)
