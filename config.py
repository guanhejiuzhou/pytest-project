import os
# 返回脚本上两层目录路径
PRO_PATH = os.path.dirname(os.path.abspath(__file__))


class RunConfig:
    """
    运行测试配置
    """
    # 运行测试用例的目录或文件
    cases_path = os.path.join(PRO_PATH, 'test_dir')

    # 配置浏览器驱动类型
    driver_type = "chrome"

    # 配置运行的url
    url = "https://www.baidu.com"

    # 失败重跑次数
    rerun = "1"

    # 当达到最大失败数，停止执行
    max_fail = "5"

    # 浏览器驱动-不需要修改
    driver = None

    # 报告路劲-不需要修改
    NEW_REPORT = None

