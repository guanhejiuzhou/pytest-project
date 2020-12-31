# -*- coding:utf-8 -*-
"""对所有的元素定位yaml文件进行审查，尽量是每一项元素不出错"""
import os
import yaml
from config.config import rc
from utils.times import running_time


@running_time
def inspect_element():
    """检查所有的元素是否正确
    只能做一个简单的检查
    """
    for files in os.listdir(rc.ELEMENT_PATH):
        _path = os.path.join(rc.ELEMENT_PATH, files)
        with open(_path, encoding='utf-8') as f:
            data = yaml.safe_load(f)
        for k in data.values():
            try:
                pattern, value = k.split('==')
            except ValueError:
                raise Exception("元素表达式中没有`==`")
            if pattern not in rc.LOCATE_MODE:
                raise Exception('%s中元素【%s】没有指定类型' % (_path, k))
            elif pattern == 'xpath':
                assert '//' in value, \
                    '%s中元素【%s】xpath类型与值不配' % (_path, k)
            elif pattern == 'css':
                assert '//' not in value, \
                    '%s中元素【%s]css类型与值不配' % (_path, k)
            else:
                assert value, '%s中元素【%s】类型与值不匹配' % (_path, k)


if __name__ == '__main__':
    inspect_element
