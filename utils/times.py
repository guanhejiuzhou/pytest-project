# -*- coding:utf-8 -*-
"""
很多模块会用到时间戳，或者日期等字符串，先单独将时间封装成一个模块，方便其他模块调用
"""
import time
import datetime
from functools import wraps


def timestamp():
    """时间戳"""
    return time.time()


def dt_strftime(fmt="%Y%m"):
    """
    datetime格式化时间
    :param fmt:%Y%m%d %H%M%S
    :return:
    """
    return datetime.datetime.now().strftime(fmt)


def sleep(seconds=1.0):
    """
    睡眠时间
    :param seconds:
    :return:
    """
    time.sleep(seconds)


def running_time(func):
    """函数运行时间"""

    @wraps(func)
    # 增添或修改功能的函数
    def wrapper(*args, **kwargs):
        start = timestamp()
        # 执行被装饰的函数
        res = func(*args, **kwargs)
        print("检验元素done!用时%.3f秒!" % (timestamp() - start))
        return res
    return wrapper()


if __name__ == '__main__':
    print(dt_strftime("%Y%m%d%H%M%S"))
