# -*- coding:utf-8 -*-
import re
import pytest
from utils.logger import log
from common.readconfig import ini
from page_object.baiduSearch_page import BaiduSearchPage


# sys.path.insert(0, dirname(dirname(abspath(__file__))))


class TestBaiduSearch:
    """ 百度搜索 """

    # pytest.fixture()实现了和unittest的setup、teardown一样的前置启动、后置清理的装饰器
    @pytest.fixture(scope='function', autouse=True)
    def open_baidu(self, drivers):
        """打开百度"""
        baidusearch = BaiduSearchPage(drivers)
        baidusearch.get_url(ini.url)

    def test_baidu_search_selenium_case(self, drivers):
        """
        名称：百度搜索selenium关键字
        步骤：打开浏览器-输入selenium-点击搜索按钮
        预期结果：检查搜索结果是否包含selenium关键字
        :param drivers:
        :return:
        """
        baidusearch = BaiduSearchPage(drivers)
        baidusearch.input_search("selenium")
        baidusearch.click()
        # 获取页面源代码
        result = re.search(r'selenium', baidusearch.get_source)
        log.info(result)
        assert result


    def test_baidu_search_pytest_case(self, browser, base_url):
        """
        名称：百度搜索pytest
        步骤：打开浏览器-输入pytest-点击搜索按钮
        预期结果：检查页面标题是否包含关键字
        :param browser:浏览器
        :param base_url:url
        :return:
        """
        page = BaiduSearchPage(browser)
        page.get(base_url)
        page.search_input = 'pytest'
        page.search_button.click()
        sleep(2)
        assert browser.title == 'pytest_百度搜索'

    def test_baidu_search_selenium_case(self, browser, base_url):
        """
        名称：百度搜索selenium
        步骤：打开浏览器-输入selenium-点击搜索按钮
        预期结果：检查页面标题是否包含关键字
        :param browser:
        :param base_url:
        :return:
        """
        page = BaiduSearchPage(browser)
        page.get(base_url)
        page.search_input = 'selenium'
        page.search_button.click()
        sleep(2)
        assert browser.title == 'selenium_百度搜索'


class TestSearchSetting:
    """ 百度搜索设置 """

    def test_baidu_search_setting_case(self, browser, base_url):
        """
        名称：百度搜索设置
        步骤：打开浏览器-点击设置链接-在下拉框中点击‘选择搜索’-点击保存设置-对弹出警告框保存
        预期结果：检查是否弹出提示框
        :param browser:
        :param base_url:
        :return:
        """
        page = BaiduSearchPage(browser)
        page.get(base_url)
        page.settings.click()
        page.search_setting.click()
        sleep(2)
        page.save_setting.click()
        # 获取弹框的文本内容
        alert_text = page.get_alert_text
        # 点击确定
        page.accept_alert()
        assert alert_text == "已经记录下您的使用偏好"


if __name__ == '__main__':
    pytest.main(["-v", "-s", "test_baidu_search.py"])
