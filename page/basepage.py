# -*- coding:utf-8 -*-
"""
selenium基类
存放selenium基类的封装方法
"""
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementNotVisibleException

from config.config import rc
from utils.times import sleep
from utils.logger import log


class LocatorTypeError(Exception):
    pass


class ElementNotFound(Exception):
    pass


class BasePage(object):
    """selenium基类"""

    def __init__(self, driver, timeout=10, t=0.5):
        self.driver = driver
        self.timeout = timeout
        self.t = t
        self.wait = WebDriverWait(self.driver, self.timeout)

    def get_url(self, url):
        """
        打开网址并验证
        :param url:
        :return:
        """
        self.driver.maximize_window()
        self.driver.set_page_load_timeout(60)
        try:
            self.driver.get(url)
            self.driver.implicitly_wait(10)
            log.info("打开网址：%s" % url)
        except TimeoutException:
            raise TimeoutException("打开%s超时请检查网络或网址服务器" % url)

    @staticmethod  # 静态方法，类或实例均可调用，该静态方法函数里不传入self或cls
    def element_locator(func, locator):
        """
        元素定位器
        :param func:
        :param locator:
        :return:
        """
        id, value = locator
        return func(rc.LOCATE_MODE[id], value)

    def find_element(self, locator):
        """
        定位单个元素，定位到元素，返回元素对象，没定位到，Timeout异常
        :param locator:
        :return:
        """
        if not isinstance(locator, tuple):
            raise LocatorTypeError(log.info("参数类型错误，locator必须是元组类型：loc = ('id', 'value')"))
        else:
            log.info("正在定位元素信息：定位方式->%s,value值->%s" % (locator[0], locator[1]))
            try:
                ele = WebDriverWait(self.driver, self.timeout, self.t).until(
                    EC.presence_of_element_located(locator)
                )
            except TimeoutException as msg:
                log.info("定位元素出现超时！")
                raise msg
            return ele
        # return BasePage.element_locator(lambda *args: self.wait.until(
        #     EC.presence_of_element_located(args)), locator)

    def find_elements(self, locator):
        """
        查找多个相同的元素,复数定位，返回elements对象 list
        :param locator:
        :return:
        """
        if not isinstance(locator, tuple):
            raise LocatorTypeError(log.info("参数类型错误，locator必须是元组类型：loc = ('id', 'value')"))
        else:
            log.info("正在定位元素信息：定位方式->%s,value值->%s" % (locator[0], locator[1]))
            try:
                eles = WebDriverWait(self.driver, self.timeout, self.t).until(
                    EC.presence_of_all_elements_located(locator)
                )
            except TimeoutException as msg:
                log.info("定位元素出现超时！")
                raise msg
            return eles
        # return BasePage.element_locator(lambda *args: self.wait.until(
        #     EC.presence_of_all_elements_located(args)), locator)

    def elements_num(self, locator):
        """
        获取相同元素的个数
        :param locator:
        :return:
        """
        number = len(self.find_elements(locator))
        log.info("相同元素: {}".format((locator, number)))
        return number

    def input_text(self, locator, text):
        """
        文本框输入，写入文本
        :param locator:
        :param txt:
        :return:
        """
        ele = self.find_element(locator)
        # is_displayed()用于判断某个元素是否存在页面上
        # 这里的存在不是肉眼看到的存在，而是HTML代码的存在。某些情况元素的visibility为hidden或者display
        # 属性为None，我们在页面看不到但是实际是存在页面的一些元素
        if ele.is_displayed():
            ele.send_keys(text)
        else:
            raise ElementNotVisibleException(log.info("输入文本：{}元素不可见或者不唯一无法输入".format(text)))
        # ele.send_keys(text)
        # log.info("输入文本: {}".format(text))

    def click(self, locator):
        """
        点击元素
        :param locator:
        :return:
        """
        ele = self.find_element(locator)
        if ele.is_displayed():
            ele.click()
        else:
            raise ElementNotVisibleException(log.info("点击元素：{}元素不可见或者不唯一无法点击".format(locator)))

    def clear(self, locator):
        """
        清空输入框文本
        :param locator:
        :return:
        """
        ele = self.find_element(locator)
        if ele.is_displayed():
            ele.clear()
        else:
            raise ElementNotVisibleException(log.info("元素不可见或者不唯一"))

    def get_text(self, locator):
        """
        获取当前的text文本
        :param locator:
        :return:
        """
        if not isinstance(locator, tuple):
            raise LocatorTypeError(log.info("参数类型错误，locator必须是元组类型：loc = ('id','value')"))
        try:
            t = self.find_element(locator).text
            return t
        except:
            log.info("获取text失败，返回''")
            return ""

    @property  # 既拥有get、set方法的灵活性，又具有属性直接赋值取值的简便性
    def get_source(self):
        """
        获取页面源代码
        :return:
        """
        return self.driver.page_source

    def refresh(self, url=None):
        """
        刷新页面F5  如果url是空值，就刷新当前页面，否则就刷新指定页面
        :param url: 默认值是空的
        :return:
        """
        if url is None:
            self.driver.refresh()
            self.driver.implicitly_wait(30)
        else:
            self.driver.get(url)

    def is_selected(self, locator, Type=''):
        """
        判断元素是否被选中，返回bool值（选中/取消选中）
        :param locator:
        :param Type:
        :return:
        """
        ele = self.find_element(locator)
        try:
            if Type == "":  # 如果Type参数为空，返回元素是否为选中状态，True/False（默认）
                r = ele.is_displayed()
                return r
            elif Type == "click":  # 如果Type参数为click，执行元素的点击操作
                ele.click()
            else:
                log.info(f"type参数 {type} 错误，仅可为click或''")
        except:
            return False

    def is_element_exist(self, locator):
        """
        判断单个元素是否在DOM里面（是否存在）
        :param locator:
        :return:
        """
        try:
            self.find_element(locator)
            return True
        except:
            return False

    def is_element_exists(self, locator):
        """
        判断一组元素是否在DOM里面（是否存在），若不存在，返回一个空的list
        :param locator:
        :return:
        """
        eles = self.find_elements(locator)
        n = len(eles)
        if n == 0:
            return False
        elif n == 1:
            return True
        else:
            log.info("定位到元素的个数：{n}")
            return True

    def title(self, title, Type='contains'):
        """
        根据传入的Type类型判断title
        :param title:
        :param Type:
        :return:
        """
        try:
            if Type == "is":  # 判断当前网页title名为title，返回bool值
                result = WebDriverWait(self.driver, self.timeout, self.t).until(EC.title_is(title))
                return result
            elif Type == "contains":  # 判断当前网页title名包含title，返回bool值（默认）
                result = WebDriverWait(self.driver, self.timeout, self.t).until(EC.title_contains(title))
                return result
            else:
                log.info(f"type参数 {type} 错误，仅可为is、contains")
        except:
            return False

    def in_element(self, locator, value, Type='text'):
        """
        根据传入的type判断内容是否在指定的元素里面
        :param locator:
        :param value:
        :param Type:
        :return:
        """
        if not isinstance(locator, tuple):
            log.info("locator参数类型错误，必须传元组类型：loc = ('id', 'value')")
        try:
            if Type == 'text':  # 判断当前获取到的text包含value，返回bool值（默认）
                result = WebDriverWait(self.driver, self.timeout, self.t).until(
                    EC.text_to_be_present_in_element(locator, value)
                )
                return result
            elif Type == 'value':  # 判断当前获取到的value包含value，返回bool值，value为空字符串，返回False
                result = self.find_element(locator, value)
                return result
            else:
                log.info(f"type参数 {type} 错误，仅可使用text或value属性定位")
                return False
        except:
            return False

    def is_alert(self, timeout=10):
        """
        判断alert弹窗
        :param timeout:
        :return:
        """
        try:
            result = WebDriverWait(self.driver, timeout, self.t).until(EC.alert_is_present())
            return result
        except:
            return False

    def get_title(self):
        """
        获取title
        :return:
        """
        return self.driver.title

    def get_attribute(self, locator, name):
        """
        获取属性
        :param locator:
        :param name:
        :return:
        """
        if not isinstance(locator, tuple):
            raise LocatorTypeError(log.info("参数类型错误，locator必须是元组类型：loc = ('id','value')"))
        try:
            element = self.find_element(locator)
            return element.get_attribute(name)
        except:
            log.info("获取%s属性失败，返回''" % name)
            return ''

    def js_focus_element(self, locator):
        """
        聚焦元素
        :param locator:
        :return:
        """
        if not isinstance(locator, tuple):
            raise LocatorTypeError(log.info("参数类型错误"))
        target = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView();", target)

    def js_scroll_top(self):
        """
        滚到顶部
        :return:
        """
        js = "window.scrollTo(0,0)"
        self.driver.execute_script(js)

    def js_scroll_end(self, x=0):
        """
        滚到底部
        :param x:
        :return:
        """
        js = "window.scrollTo(%s, document.body.scrollHeight)" % x
        self.driver.execute_script(js)

    def select_by_index(self, locator, index=0):
        """
        通过索引定位选择，index是索引第几个，从0开始，默认第一个
        :param locator:
        :param index:
        :return:
        """
        if not isinstance(locator, tuple):
            raise LocatorTypeError(log.info("参数类型错误"))
        element = self.find_element(locator)
        Select(element).select_by_index(index)

    def select_by_value(self, locator, value):
        """
        通过value属性选择
        :param locator:
        :param value:
        :return:
        """
        if not isinstance(locator, tuple):
            raise LocatorTypeError(log.info("参数类型错误"))
        element = self.find_element(locator)
        Select(element).select_by_value(value)

    def select_by_text(self, locator, text):
        """
        通过文本值定位
        :param locator:
        :param text:
        :return:
        """
        element = self.find_element(locator)
        Select(element).select_by_visible_text(text)

    def switch_iframe(self, id_index_locator):
        """
        切换iframe
        :param id_index_locator:
        :return:
        """
        try:
            if isinstance(id_index_locator, int):
                self.driver.switch_to.frame(id_index_locator)
            elif isinstance(id_index_locator, str):
                self.driver.switch_to.frame(id_index_locator)
            elif isinstance(id_index_locator, tuple):
                ele = self.find_element(id_index_locator)
                self.driver.switch_to.frame(ele)
        except:
            log.info("iframe切换异常")

    def switch_to_default(self):
        """
        切换到默认窗口
        :return:
        """
        self.driver.switch_to.default_content()

    def switch_to_window_by_title(self, title):
        """
        切换不同页面窗口
        :param title:
        :return:
        """
        for handle in self.driver.window_handles:
            self.driver.switch_to.window(handle)
            if self.driver.title == title:
                break
            self.driver.switch_to.default_content()

    def move_to_element(self, locator):
        """
        鼠标悬停操作
        :param locator:
        :return:
        """
        try:
            ele = self.find_element(locator)
            ActionChains(self.driver).move_to_element(ele).perform()
        except:
            log.info("鼠标悬停操作失败")
            return False

    def _locate_elements(self, locator):
        """
        通过选择器定位元素
        选择器应通过带有"i,xxx"的示例传递
        "x, //*[@id='langs']/button"
        :param locator:
        :return:
        """
        if locator is not None:
            elements = self.driver.find_elements(*locator)
        else:
            raise NameError("请输入目标元素的有效定位器")
        return elements

    def right_click(self, locator):
        """
        鼠标右击
        :param locator:
        :return:
        """
        el = self.find_element(locator)
        ActionChains(self.driver).context_click(el).perform()

    def double_click(self, selector):
        """
        鼠标双击
        :param selector:想要双击的元素，元素定位
        :return:
        """
        ele = self._locate_elements(selector)
        ActionChains(self.driver).double_click(ele).perform()

    def drag_element(self, source, target):
        """
        拖拽元素
        :param source:来源
        :param target:目标
        :return:
        """
        el_source = self.find_element(source)
        el_target = self.find_element(target)

        if self.driver.w3c:
            ActionChains(self.driver).drag_and_drop(el_source, el_target).perform()
        else:
            ActionChains(self.driver).click_and_hold(el_source).perform()
            ActionChains(self.driver).move_to_element(el_target).perform()
            ActionChains(self.driver).release(el_target).perform()

    def upload_input(self, locator, file):
        """
        上传文件（标签为input类型，此类型最常见，最简单）
        :param locator:上传按钮定位
        :param file:将要上传的文件（绝对路径）
        :return:
        """
        self.find_element(locator).send_keys(file)


if __name__ == "__main__":
    pass


