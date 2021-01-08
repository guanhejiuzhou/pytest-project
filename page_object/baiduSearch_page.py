# -*- coding:utf-8 -*-
from page.basepage import BasePage, sleep
from common.readelement import Element

"""
百度首页页面搜索封装
"""
baidusearch = Element('baidusearch')


class BaiduSearchPage(BasePage):
    """搜索类"""

    def input_search(self, content):
        """搜索框输入"""
        self.input_text(baidusearch['搜索框'], text=content)
        sleep()

    def click_search(self):
        """点击搜索按钮"""
        self.click(baidusearch['搜索按钮'])

    def settings(self):
        """点击设置按钮"""
        self.click(baidusearch['设置下拉框'])
        sleep(2)

    def search_setting(self):
        """点击搜索设置选项"""
        self.click(baidusearch['搜索设置选项'])
        sleep(2)

    def save_setting(self):
        """点击保存设置"""
        self.click(baidusearch['保存设置'])
        sleep(2)


if __name__ == '__main__':
    pass
