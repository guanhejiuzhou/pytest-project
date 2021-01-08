"""
conftest.py特点：
1.可以跨.py文件调用，有多个.py文件调用时，可以让conftest.py只调用一次fixture
2.不需要import导入conftest.py，pytest用例会自动识别该文件，放在项目的根目录下就可以全局目录调用，如果放在
某个package下，那就在该package内有效，可以有多个conftest.py
3.conftest.py配置脚本名称是固定的，不能修改名称
4.conftest.py文件不能被其他文件导入
5.所有同目录测试文件运行前都会执行conftest.py文件
"""

"""
conftest.py用法：
conftest.py文件实际应用需要结合fixture来使用
1.fixture源码详解：
fixture(scope='function',params=None,autouse=False,ids=None,name=None):
scope参数可以控制fixture的作用范围
params:一个可选的参数列表，它将导致多个参数调用fixture功能和所有测试使用它
autouse：如果True，则为所有测试激活fixture func可以看到它；如果为False，则显示需要参考来激活fixture
ids:每个字符串ID的列表，每个字符串对应于params这样他们就是测试ID的一部分，如果没有提供ID他们将从params自动化
生成
name：fixture的名称，默认为装饰函数的名称
"""

"""
fixture的作用范围：
scope控制fixture的作用范围，有四个级别参数 function（默认）、class、module、session
function：每一个函数或方法都会调用
class：每一个类调用一次，一个类中可以有多个方法
module：每一个.py文件调用一次，该文件内可以有多个function和class
session：多个文件调用一次，可以跨.py文件调用，每个.py文件就是module
"""

"""
conftest应用场景:
1.每个接口需共用到的token
2.每个测试需共用到的测试用例数据
3.每个测试需共用到的配置信息
"""

import pytest
from py.xml import html
from selenium import webdriver

from config.config import rc
from common.readconfig import ini
from utils.times import timestamp
from utils.send_mail import send_report

driver = None


@pytest.fixture(scope='session', autouse=True)  # 多个.py文件只调用一次fixture
def drivers(request):
    global driver
    if driver is None:
        driver = webdriver.Chrome()
        driver.maximize_window()

    def fn():
        driver.quit()

    request.addfinalizer(fn)
    return driver


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    """
    用于向测试用例中添加开始时间、内部注释和失败截图等
    当测试失败的时候，自动截图，展示到HTML报告中
    pytest_runtest_makereport()钩子函数的主要功能是判断每条测试用例的运行情况，当测试用例错误或失败后会
    调用capture_screenshot()函数进行截图并将测试用例的文件名+类名+方法名作为截图的名称保存于image目录中
    :param item:
    :return:
    """
    pytest_html = item.config.pluginmanager.getplugin('html')
    outcome = yield
    report = outcome.get_result()
    report.description = str(item.function.__doc__)
    extra = getattr(report, 'extra', [])

    if report.when == 'call' or report.when == 'setup':
        xfail = hasattr(report, 'wasxfail')
        if (report.skipped and xfail) or (report.failed and not xfail):
            screen_img = _capture_screenshot()
            if screen_img:
                html = '<div><img src="data:image/png;base64,%s" alt="screenshot" style="width:1024px;height:768px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % screen_img
                extra.append(pytest_html.extras.html(html))
        report.extra = extra


# 设置HTML报告中添加用例描述头
def pytest_html_results_table_header(cells):
    cells.insert(1, html.th('用例名称'))
    cells.insert(2, html.th('Test_nodeid'))
    cells.pop(2)


# 设置HTML报告中添加用例描述表格
def pytest_html_results_table_row(report, cells):
    cells.insert(1, html.td(report.description))
    cells.insert(2, html.td(report.nodeid))
    cells.pop(2)


def pytest_html_results_table_html(report, data):
    if report.passed:
        del data[:]
        data.append(html.div('通过的用例未捕获日志输出.', class_='empty log'))


def pytest_html_report_title(report):
    report.title = "pytest项目测试报告"


def pytest_configure(config):
    config._metadata.clear()
    config._metadata['测试项目'] = "测试百度官网搜索"
    config._metadata['测试地址'] = ini.url


def pytest_html_results_summary(prefix, summary, postfix):
    prefix.extend([html.p("所属部门：牛逼的效率体系")])
    prefix.extend([html.p("测试执行人：关河九州")])


# def pytest_terminal_summary(terminalreporter, exitstatus, config):
#     """收集测试结果"""
#     result = {
#         "total": terminalreporter._numcollected,
#         "passed": len(terminalreporter.stats.get('passed', [])),
#         "failed": len(terminalreporter.stats.get('failed', [])),
#         "error": len(terminalreporter.stats.get('error', [])),
#         "skipped": len(terminalreporter.stats.get('skipped', [])),
#         "total times": timestamp() - terminalreporter._sessionstarttime
#     }
#     print(result)
#     if result['failed'] or result['error']:
#         send_report()


def _capture_screenshot():
    """截图保存为base64"""
    # now_time, screen_file = rc.screen_path
    #     # driver.save_screenshot(screen_file)
    #     # allure.attach.file(screen_file,
    #     #                    "失败截图{}".format(now_time),
    #     #                    allure.attachment_type.PNG)
    #     # with open(screen_file, 'rb') as f:
    #     #     imagebase64 = base64.b64encode(f.read())
    #     # return imagebase64.decode()
    return driver.get_screenshot_as_base64()



