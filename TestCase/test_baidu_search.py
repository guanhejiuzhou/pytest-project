# -*- coding:utf-8 -*-
import re
import pytest
from utils.logger import log
from common.readconfig import ini
from page_object.baiduSearch_page import BaiduSearchPage


class TestBaiduSearch:
    """ 百度搜索 """

    # pytest.fixture()实现了和unittest的setup、teardown一样的前置启动、后置清理的装饰器
    @pytest.fixture(scope='function', autouse=True)
    def open_baidu(self, drivers):
        """打开百度"""
        search = BaiduSearchPage(drivers)
        search.get_url(ini.url)

    def test_baidu_search_selenium_case(self, drivers):
        """
        名称：百度搜索selenium关键字
        步骤：打开浏览器-输入selenium-点击搜索按钮
        预期结果：检查搜索结果是否包含selenium关键字
        """
        search = BaiduSearchPage(drivers)
        search.input_search("selenium")
        search.click_search()
        # 获取页面源代码
        result = re.search(r'selenium', search.get_source)
        log.info(result)
        assert result


class TestSearchSetting:
    """百度搜索设置"""

    @pytest.fixture(scope='function', autouse=True)
    def open_baidu(self, drivers):
        """打开百度"""
        search = BaiduSearchPage(drivers)
        search.get_url(ini.url)

    def test_baidu_search_settings_case(self, drivers):
        """
        名称：百度搜索设置
        步骤：打开浏览器-点击设置链接-在下拉框中点击‘选择搜索’-点击保存设置-对弹出警告框保存
        预期结果：检查是否弹出提示框
        """
        search = BaiduSearchPage(drivers)
        search.settings()
        search.search_setting()
        search.save_setting()
        alert_text = search.is_alert()
        search.accept_alert()
        assert alert_text == "已经记录下您的使用偏好"


if __name__ == '__main__':
    pytest.main(["-v", "-s", "TestCase/test_baidu_search.py"])
