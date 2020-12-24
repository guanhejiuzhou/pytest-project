基于pytest进行UI自动化测试特点：

`全局配置浏览器启动/关闭`

`测试用例运行失败自动截图`

`测试用例运行失败重跑`

`测试数据参数化`

**1.项目结构：**

page/:用于存放page层的封装

test_dir/:存放测试用例

test_report/:存放测试报告

conftest.py：pytest配置文件

run_tests.py:测试运行文件

**2.命名与设计规范：**

(1).对于page层的封装存放于page目录，命名规范为 XXX_page.py

(2).对于测试用例的编写存放于test_dir目录，命名规范为 test_xxx.py

(3).每一个功能点对应一个测试类，并且以 Test 开头，

(4).在一个测试类下编写功能点的所有的测试用例，如test_login_user_null、test_login_pawd_null等等

**3.安装依赖及依赖库说明：**

pip install -r requirements.txt

安装requirements.txt指定依赖库的版本

(1).selenium：WebUI自动化测试

(2).pytest:Python第三方单元测试框架

(3).pytest-html:pytest扩展，生成HTML格式的测试报告

(4).pytest-rerunfailures:pytest扩展，实现测试用例运行失败重跑

(5).click:命令行工具开发库

(6).poium:基于selenium/appium的Page Object测试库，简化page层元素定义
