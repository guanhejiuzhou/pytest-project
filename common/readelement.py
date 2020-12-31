# -*- coding:utf-8 -*-
""" 读取元素定位文件 """

import os
import yaml
from config.config import rc


class Element(object):
    """获取元素"""

    def __init__(self, name):
        self.file_name = '%s.yaml' % name
        self.element_path = os.path.join(rc.ELEMENT_PATH, self.file_name)
        if not os.path.exists(self.element_path):
            raise FileNotFoundError("%s 文件不存在！" % self.element_path)
        with open(self.element_path, encoding='utf-8') as f:
            self.data = yaml.safe_load(f)

    # 通过特殊方法__getitem__ 实现调用任意属性，读取yaml中的值
    def __getitem__(self, item):
        """获取属性"""
        data = self.data.get(item)
        if data:
            name, value = data.split('==')
            return name, value
        raise ArithmeticError("{}中不存在关键字：{}".format(self.file_name, item))


if __name__ == '__main__':
    baidusearch = Element('baidusearch')
    print(baidusearch['搜索框'])
    print(baidusearch['搜索按钮'])
