""" pytest配置文件 """
import os
import pytest
from py.xml import html
from selenium import webdriver
from selenium.webdriver import Remote
from selenium.webdriver.chrome.options import Options as CH_Options
from selenium.webdriver.firefox.options import Options as FF_Options
from config import RunConfig

# 项目目录配置
# 返回脚本上两层目录路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPORT_DIR = BASE_DIR + "/test_report"


# 定义基本测试环境
# 使用装饰器标记fixture的功能，pytest.fixture()如果不写参数，默认就是scope='function'，作用范围为每个
# 测试用例之前运行一次，销毁代码在测试用例之后运行
@pytest.fixture(scope='function')
def base_url():
    return RunConfig.url


# 设置html报告中添加用例描述头
def pytest_html_results_table_header(cells):
    cells.insert(2, html.th('Description'))
    cells.pop()


# 设置HTML报告中添加用例描述表格
def pytest_html_results_table_row(report, cells):
    cells.insert(2, html.td(report.description))
    cells.pop()


@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    """
    用于向测试用例中添加开始时间、内部注释和失败截图等

    pytest_runtest_makereport()钩子函数的主要功能是判断每条测试用例的运行情况，当测试用例错误或失败后会
    调用capture_screenshot()函数进行截图并将测试用例的文件名+类名+方法名作为截图的名称保存于image目录中
    :param item:
    :return:
    """

    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    report.description = description_html(item.function.__doc__)
    extra = getattr(report, 'extra', [])
    if report.when == 'call' or report.when == 'setup':
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            case_path = report.nodeid.replace("::", "_") + ".png"
            if "[" in case_path:
                case_name = case_path.split("-")[0] + "].png"
            else:
                case_name = case_path
            capture_screenshots(case_name)
            img_path = "image/" + case_name.split("/")[-1]
            # 将截图插入HTML格式的报告中
            # 添加<img>标签，通过src属性指定图片的路径
            if img_path:
                html = '<div><img src="%s" alt="screenshot" style="width:304px;height:228px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % img_path
                extra.append(pytest_html.extras.html(html))
            report.extra = extra


def description_html(desc):
    """
    将用例中的描述转成HTML对象
    :param desc: 描述
    :return:
    """
    if desc is None:
        return "No case description"
    desc_ = ""
    for i in range(len(desc)):
        if i == 0:
            pass
        elif desc[i] == '\n':
            desc_ = desc_ + ";"
        else:
            desc_ = desc_ + desc[i]

    desc_lines = desc_.split(";")
    desc_html = html.html(
        html.head(
            html.meta(name="Content-Type", value="text/html; charset=latin1")),
        html.body(
            [html.p(line) for line in desc_lines]))
    return desc_html


def capture_screenshots(case_name):
    """
    配置用例失败截图路径
    :param case_name: 用例名
    :return:
    """
    global driver
    file_name = case_name.split("/")[-1]
    if RunConfig.NEW_REPORT is None:
        raise NameError('没有初始化测试报告目录')
    else:
        image_dir = os.path.join(RunConfig.NEW_REPORT, "image", file_name)
        RunConfig.driver.save_screenshot(image_dir)


# 启动浏览器
# scope=session表示多个文件调用一次，可以跨.py文件调用
# autouse=True自动使用
@pytest.fixture(scope='session', autouse=True)
def browser():
    """
    全局定义浏览器驱动
    :return:
    """

    global driver

    if RunConfig.driver_type == "chrome":
        # 本地Chrome浏览器
        driver = webdriver.Chrome()
        driver.maximize_window()

    elif RunConfig.driver_type == "firefox":
        # 本地Firefox浏览器
        driver = webdriver.Firefox()
        driver.maximize_window()

    elif RunConfig.dirver_type == "chrome-headless":
        # chrome headless模式-谷歌自己出的无头浏览器模式
        chrome_options = CH_Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(options=chrome_options)

    elif RunConfig.driver_type == "firefox-headless":
        # firefox headless模式
        firefox_options = FF_Options()
        firefox_options.headless = True
        driver = webdriver.Firefox(firefox_options=firefox_options)

    else:
        raise NameError("driver驱动类型定义错误！")

    RunConfig.driver = driver
    return driver


# 关闭浏览器
@pytest.fixture(scope='session', autouse=True)
def browser_close():
    yield driver
    driver.quit()
    print("test end!")


if __name__ == '__main__':
    capture_screenshots("test_dir/test_baidu_search.test_search_python.png")
