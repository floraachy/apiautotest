## 前言

  公司突然要求你做自动化，但是没有代码基础不知道怎么做？或者有自动化基础，但是不知道如何系统性的做自动化， 放在yaml文件中维护，不知道如何处理多业务依赖的逻辑？

  那么本自动化框架，将为你解决这些问题。
  - 框架主要使用 python 语言编写，结合 pytest 进行二次开发，用户仅需要在 yaml 或者 excel 文件中编写测试用例， 编写成功之后，会自动生成测试用例代码，零基础代码小白，也可以操作。 
  - 如果是具备代码基础的，也可以直接通过 py 文件编写测试用例。 
  - 使用 pytest-html / Allure 生成报告，并针对测试报告样式进行了调整，使得报告更加美观； 
  - 测试完成后，支持发送 企业微信通知/ 钉钉通知/ 邮箱通知，灵活配置。


## 一、框架介绍

本框架主要是基于 Python + pytest + pytest-html/Allure + loguru  + 邮件通知/企业微信通知/钉钉通知 实现的接口自动化框架。

* git地址: [https://www.gitlink.org.cn/floraachy/apiautotest](https://www.gitlink.org.cn/floraachy/apiautotest)
* 项目参与者: floraachy
* 技术支持邮箱: 1622042529@qq.com
* 个人博客地址:  [https://blog.csdn.net/FloraCHY](https://blog.csdn.net/FloraCHY)

对于框架任何问题，欢迎联系我！


## 二、实现功能

* 通过session会话方式，解决了登录之后cookie关联处理
* 框架天然支持接口动态传参、关联灵活处理
* 测试数据隔离, 实现数据驱动
* 自动生成用例代码: 测试人员在yaml/excel文件中填写好测试用例, 程序可以直接生成用例代码，纯小白也能使用
* 动态多断言: 支持响应断言和数据库断言
* 多种报告随心选择：框架支持pytest-html以及Allure测试报告，可以动态配置所需报告
* 日志模块: 采用loguru管理日志，可以输出更为优雅，简洁的日志
* 钉钉、企业微信通知: 支持多种通知场景，执行成功之后，可选择发送钉钉、或者企业微信、邮箱通知
* 执行环境一键切换，解决多环境相互影响问题
* 使用pipenv管理虚拟环境和依赖文件，提供了一系列命令和选项来帮助你实现各种依赖和环境管理相关的操作。


## 三、目录结构
```
├────case_utils/ 测试框架相关工具类
│    ├────__init__.py
│    ├────allure_handle.py  操作allure的相关方法
│    ├────platform_handle.py  跨平台的支持allure，用于生成allure测试报告
│    ├────assert_handle.py  断言处理， 包括响应断言和数据库断言
│    ├────case_handle.py   根据配置文件，从指定类型文件中读取用例数据，并调用生成用例文件方法，生成用例文件
│    ├────data_handle.py    数据处理
│    ├────request_data_handle.py   针对用例数据进行请求前后的处理
│    ├────get_results_handle.py   从pytest-html/allure测试报告中获取测试结果
│    └────send_result_handle.py   根据配置文件，从html测试报告中获取测试结果，发送指定类型的通知
├────common_utils/  公共的工具类
│    ├────__init__.py
│    ├────base_request.py   封装的requests请求
│    ├────bs4_handle.py  bs4（BeautifulSoup4）是Python中的第三方库。可以从HTML或XML文件中提取数据的Python库。
│    ├────dingding_handle.py   封装的钉钉机器人
│    ├────excel_handle.py  处理excel
│    ├────files_handle.py   处理文件相关操作
│    ├────func_handle.py   函数装饰器
│    ├────wechat_handle.py  封装企业微信机器人
│    ├────yagmail_handle.py  封装通过yagmail发送邮件的方法
│    ├────time_handle.py  封装处理时间操作的一些方法
│    └────yaml_handle.py  处理yaml文件
├────config/
│    ├────__init__.py
│    ├────case_template.txt  自动生成的测试用例文件模板
│    ├────global_vars.py    保存的一些全局变量
│    ├────project_path.py    项目路径管理
│    ├────report.css    优化html测试报告的样式文件
│    └────settings.py   配置文件
├────conftest.py
├────data/  测试用例数据
│    ├────test_login_demo.yaml
│    ├────test_login_excel_demo.xlsx
│    └────test_new_project_demo.yaml
├────outputs/
│    └────report/  保存测试报告的目录
│     └────log/   保存日志文件的目录
├────Pipfile
├────pytest.ini
├────README.md
├────run.py      运行入口  
└────test_case/   测试用例
│    ├────conftest.py
│    ├────test_auto_case/
│    │    ├────test_login_demo.py
│    │    ├────test_login_excel_demo.py
│    │    └────test_new_project_demo.py
│    └────test_manual_case/
│    │    ├────__init__.py
│    │    ├────test_demo.py
│    │    └────test_login_demo.py
 ```   

## 四、依赖库
```
python_version = "3.9"
pymysql = "*"
loguru = "*"
requests-toolbelt = "*"
beautifulsoup4 = "*"
requests = "*"
openpyxl = "*"
sshtunnel = "*"
yagmail = "*"
pyyaml = "*"
click = "*"
faker = "*"
jsonpath = "*"
pytest = "==6.2.5"
pytest-html = "==2.1.1"
pytest-rerunfailures = "*"
allure-pytest = "==2.9.45"
```


## 五、安装教程

1. 通过Git工具clone代码到本地 或者 直接下载压缩包ZIP
2. 本地电脑搭建好 python环境，我使用的python版本是3.9
3. 安装pipenv: pip install pipenv（必须在项目根目录下）
4. 使用pipenv管理安装环境依赖包：pipenv shell （必须在项目根目录下执行）
```
   注意：使用pipenv install会自动安装Pipfile里面的依赖包，该依赖包仅安装在虚拟环境里，不安装在测试机。
```
6. 激活已存在的虚拟环境（如果不存在会创建一个）：pipenv shell （必须在项目根目录下执行）
7. 更改配置文件config.settings.py，适配你需要测试的环境
8. 在data目录下新建测试用例数据文件，编写测试用例 （Excel或者Yaml）或者在test_case目录下通过python语言编写用例
9. 框架主入口为 run.py文件
```
	必须在项目根目录下，输入命令运行（如果依赖包是安装在虚拟环境中，需要先启动虚拟环境）。
    注意：本机环境中没有安装依赖包的情况下，不要直接在run.py中右键直接run
  > python run.py  (默认在test环境运行测试用例)
  > python run.py -env live 在live环境运行测试用例
  > python run.py -env=test 在test环境运行测试用例
```

### 初始化项目可能遇到的问题
#### 1. 测试机安装的是python3.7，但是本框架要求3.9.5，怎么办？
方法一：建议采纳此方法
1）首先在项目根目录下打开命令窗口，移除虚拟环境：pipenv --rm
2）安装虚拟环境时忽略锁定的版本号，同时安装依赖包：pipenv install --skip-lock
如果使用上述命令报错：Warning: Python 3.9 was not found on your system... Neither 'pyenv' nor 'asdf' could be found to install Python.
请使用如下命令：pipenv install --python 3.7 --skip-lock  (注意：这里的版本号，如果你的是3.8，就应该如下写命令：pipenv install --python 3.8 --skip-lock)

3）激活虚拟环境：pipenv shell

4）运行框架：python run.py

<br/>

方法二：
1）首先在项目根目录下打开命令窗口，移除虚拟环境：pipenv --rm
2）更改项目根目录下的Pipfile文件
```
# 如下所示，3.9更改为3.7
[requires]
python_version = "3.7"
```
3）更改项目根目录下的Pipfile.lock文件
```
# 如下所示，3.9更改为3.7
        "requires": {
            "python_version": "3.7"
        },
```
4）安装虚拟环境，同时安装依赖包：pipenv install

5）激活虚拟环境：pipenv shell

6）运行框架：python run.py

#### 2. 无法安装依赖包或者安装很慢，怎么办？
检查一下Pipfile文件中的pip的安装源（位置：Pipfile）
以下安装源均可：
```
pip默认的镜像地址是：https://pypi.org/simple
清华大学：https://pypi.tuna.tsinghua.edu.cn/simple 清华大学的pip源是官网pypi的镜像，每隔5分钟同步一次，重点推荐！！！

阿里云：http://mirrors.aliyun.com/pypi/simple/

中国科技大学 https://pypi.mirrors.ustc.edu.cn/simple/

华中理工大学：http://pypi.hustunique.com/

山东理工大学：http://pypi.sdutlinux.org/

豆瓣：http://pypi.douban.com/simple/
```