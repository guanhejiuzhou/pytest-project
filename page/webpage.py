# -*- coding:utf-8 -*-
"""
selenium基类
存放selenium基类的封装方法
"""
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException

from config.config import rc
from utils.times import sleep
from utils.logger import log


class WebPage(object):
    """selenium基类"""
