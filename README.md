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
* 支持测试数据分析，测试数据不符合规范有预警机制
* 测试数据隔离, 实现数据驱动
* 自动生成用例代码: 测试人员在yaml/excel文件中填写好测试用例, 程序可以直接生成用例代码，纯小白也能使用
* 动态多断言: 支持响应断言和数据库断言
* 多种报告随心选择：框架支持pytest-html以及Allure测试报告，可以动态配置所需报告
* 日志模块: 采用loguru管理日志，可以输出更为优雅，简洁的日志
* 钉钉、企业微信通知: 支持多种通知场景，执行成功之后，可选择发送钉钉、或者企业微信、邮箱通知
* 执行环境一键切换，解决多环境相互影响问题
* 使用pipenv管理虚拟环境和依赖文件，提供了一系列命令和选项来帮助你实现各种依赖和环境管理相关的操作



## 三、目录结构
```
├────case_utils/ 测试框架相关工具类
│    ├────__init__.py
│    ├────allure_handle.py  操作allure的相关方法
│    ├────platform_handle.py  跨平台的支持allure，用于生成allure测试报告
│    ├────assert_handle.py  断言处理， 包括响应断言和数据库断言
│    ├────case_fun_handle.py   根据配置文件，从指定类型文件中读取用例数据，并调用生成用例文件方法，生成用例文件
│    ├────case_data_analysis  分析用例数据是否符合规范
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
├────files 存放测试过程中需要上传的文件
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
pydantic = "*"
xpinyin = "*"
```


## 五、安装教程

1. 通过Git工具clone代码到本地 或者 直接下载压缩包ZIP
```
git clone https://gitlink.org.cn/floraachy/uiautotest.git
```

3. 本地电脑搭建好 python环境，我使用的python版本是3.9

4. 安装pipenv
```
# 建议在项目根目录下执行命令安装
pip install pipenv
```


6. 使用pipenv管理安装环境依赖包：pipenv install （必须在项目根目录下执行）
```
   注意：使用pipenv install会自动安装Pipfile里面的依赖包，该依赖包仅安装在虚拟环境里，不安装在测试机。
```
如上环境都已经搭建好了，包括框架依赖包也都安装好了。


## 六、如何创建用例
### 1. 修改配置文件  `config.settings.py`
1）确认用例是通过YAML还是Excel编写，由CASE_FILE_TYPE控制
2）确认测试完成后是否发送测试结果，由SEND_RESULT_TYPE控制，并填充对应邮件/钉钉/企业微信配置信息
3）确认测试是否需要进行数据库断言，如有需求，填充数据库配置信息
4）指定日志收集级别，由LOG_LEVEL控制

### 2. 修改全局变量，增加测试数据  `config.global_vars.py`
1) ENV_VARS["common"]是一些公共参数，如报告标题，报告名称，测试者，测试部门。后续会显示在测试报告上。如果还有其他，可自行添加
2）ENV_VARS["test"]是保存test环境的一些测试数据。ENV_VARS["live"]是保存live环境的一些测试数据。如果还有其他环境可以继续增加，例如增加ENV_VARS["dev"] = {"host": "", ......}

### 3. 删除框架中的示例用例数据
1）删除 `data`目录下所有的YAML和EXCEL文件
2）删除 `test_case/test_manual_case`目录下所有手动编写的用例

### 4. 编写测试用例（两种方式任选其一或者都选）
#### 1 自动生成测试用例  `data`  `test_case.test_auto_case`
- 在目录`data`下新建一个YAML/Excel文件。按照如下字段要求进行测试用例数据添加
- 注意：如果需要自动创建测试用例文件，YAML/Excel文件的文件名需要以"test"开头。


#### 2. 手动编写测试用例 `data`  `test_case.test_manual_case`
- 原则上，如果是手动编写测试用例（python代码）， 测试用例数据文件不要以"test"开头。 如果以“test”开头，可能导致用例运行多次。
1）在目录`data`下新建一个YAML/Excel文件，按照要求编写测试用例数据
2）在test_case.test_manual_case下新建一个以"test"开头的测试方法，进行测试用例方法编写。

### 5. 用例中相关字段的介绍

```yaml
- case_common ：公共参数
	- allure_epic：用作于@allure.epic()装饰器中的内容。如果是使用Excel管理用例数据，这个目前是写死的。可在case_utils.case_handle.py中更改。
	- allure_feature：用作于@allure.feature()装饰器中的内容。如果是使用Excel管理用例数据， 这个用的是excel的表单名称。
	- allure_story：用作于@allure.story()装饰器中的内容。如果是使用Excel管理用例数据， 这个用的是excel的表单名称。
- case_info：用例数据
	- feature：用例所属模块， 类似于@allure.feature()。
	- title：用例标题
	- run：是否执行用例，为空或者True都会执行，为False则不执行。
	- url：请求路径（可填写全路径 或者 资源路径）。通常我们填写资源路径。在用例执行前，会针对路径进行处理。具体可见case_utils.request_data_handle.py.RequestPreDataHandle.url_handle。注：请求路径=基准路径（host/base_url）+资源路径(url)。
	- method：请求方式，例如：GET, POST, DELETE, PUT, PATCH等
	- headers：请求头，注意如果在headers里面防止cookies，其值类型需要是字符串
	- cookies：请求cookies，格式是：DICT， CookieJar对象
	- request_type：请求数据类型：params, json, file, data
	- payload：请求参数
	- files：上传附件接口所需的文件绝对路径
	- extract：后置提取参数
	- assert_response：响应断言
	- assert_sql：数据库断言
```
### 6. Excel用例单独说明
框架支持excel多表单自动生成测试用例，每一个表单作为一个测试用例模块。
例如：
excel表格名称是：test_demo.xlsx
excel表单1名称是：GitLink-登录模块
excel表单2名称是：示例模块


生成规则： 
- 如果excel表单中存在"-"，我们将取"-"后面的部分的首字母拼接excel文件名称作为测试用例模块/测试用例类/测试用例方法名称
- 如果excel表单中不存在"-"，我们将直接获取表单名称首字母拼接excel文件名称作为测试用例模块/测试用例类/测试用例方法名称
- 测试用例模块/测试用例类/测试用例方法名称同时也将遵循python语法规则进行适当调整

基于上述规则：
- excel第一个表单生成的测试用例
测试用例模块：test_demo_dlmk.py
测试用例类：TestDemoDlmkAuto
测试用例方法：test_demo_dlmk_auto

- excel第二个表单生成的测试用例
测试用例模块：test_demo_slmk.py
测试用例类：TestDemoSlmkAuto
测试用例方法：test_demo_slmk_auto

## 六、运行自动化测试
### 1.  激活已存在的虚拟环境
- （如果不存在会创建一个）：pipenv shell （必须在项目根目录下执行）

### 2. 运行
```
在pycharm>terminal或者电脑命令窗口，进入项目根路径，执行如下命令（如果依赖包是安装在虚拟环境中，需要先启动虚拟环境）。
  > python run.py  (默认在test环境运行测试用例, 报告采用allure)
  > python run.py -env live 在live环境运行测试用例
  > python run.py -env=test 在test环境运行测试用例
  > python run.py -report=pytest-html (默认在test环境运行测试用例, 报告采用pytest-html)
```
注意：
- 如果pycharm.interpreter拥有了框架所需的所有依赖包，可以通过pycharm直接在`run.py`中右键运行

## 七、查看测试报告
### pytest-html测试报告
如果是pytest-html生成的测试报告，直接打开`outputs`目录下的`.html`报告即可。支持通过任意浏览器打开查看

### Allure测试报告
1. 如果是Allure生成的测试报告，支持通过pycharm，点击`outputs/report/allure_html/index.html`打开查看测试报告
2. 如果不通过pycharm打开，直接通过文件夹打开，windows系统环境下，可以点击`outputs/report/allure_html/双击打开Allure报告.bat`打开查看测试报告

注意：
- 通过点击`outputs/report/allure_html/双击打开Allure报告.bat`打开测试报告的方法，暂时不支持mac系统
- 如果通过点击`outputs/report/allure_html/双击打开Allure报告.bat`打开测试报告，命令窗口显示乱码，或者打不开，可以把`.bat`的文件名称修改为英文的名称，里面的所有中文注释全部移除，再次尝试


## 八 、详细功能说明
### 1. 用例中如何生成随机数据
在测试过程中，可能涉及到一些特殊场景，需要生成定制化的数据。每次运行测试，都需要按照指定规则随机生成。
例如：`data/test_new_project_demo.yaml` 中payload.name就是使用Faker随机生成的。
我这里写了一个表达式：`${faker.name().replace(" ", "").replace(".", "")}`
- 在测试方法中`case_data = RequestPreDataHandle(case).request_data_handle()`会进行用例数据处理
- 处理过程中会调用`common_utils.data_handle.data_replace`进行数据处理
- 在`common_utils.data_handle `有导入Faker包，并且初始化了faker对象。因此上述表达式能成功运行获取其结果

这里需要注意以下几点：
- 如果是python自带的一些方法，不需要额外导包，或者写方法，就会直接处理。
- Faker这个Python库，已经可以满足生成各种各样的伪数据，这个我已经在`common_utils.data_handle `中定义好了。
- 如果还有一些其他的定制化数据，可以在`common_utils.data_handle `中进行添加。

### 2. 用例中如何提取响应数据作为全局变量并使用
在测试过程中，通常下一个接口需要用到上一个接口的响应数据，这个时候就涉及到参数的提取。
我们在用例数据中定义了参数：`extract`进行后置参数的提取，根据接口返回数据的类型（JSON或者Text）采取不同的方法，从响应数据中提取参数，保存在全局变量中。
例如：
- 登录接口中定义了需要提取的参数：`data/test_login_demo.yaml`
```yaml
  extract:
    nickname: $.username
    login: $.login
    user_id: $.user_id
```
- 请求结束后，`case_utils/request_data_handle.py.after_request_extract`就会接口返回数据的类型（JSON或者Text）采取不同的方法，从响应数据中提取参数，保存在全局变量中。
- 下一个接口需要用到user_id，只需要在用例中以如下格式书写`${user_id}`即可。
```yaml
  payload:
    "user_id": ${user_id}
    "name": ${faker.name().replace(" ", "").replace(".", "")}
    "repository_name": ${faker.name().replace(" ", "").replace(".", "")}
```

### 3. 如何进行响应数据断言
以下是支持的几种响应断言：
|  断言方式 |  说明  |
| ------------ | ------------ |
| eq |  相等，判断预期结果是否等于实际结果 |
| in  |  包含， 判断实际结果是否包含预期结果 |
| gt |  大于， 判断预期结果是否大于实际结果 |
| lt  |  小于， 判断预期结果是否小于实际结果 |
| not | 非，判断预期结果不等于实际结果  |

以下是响应断言示例：
```yaml
  assert_response:
    eq:
      http_code: 200
      $.user_id: ${user_id}
    in:
      $.login: ${login}
    gt:
      $.user_id: 84955
    lt:
      $.user_id: 84953
    not:
      $.user_id: 85390
```
- 预期结果：http_code；实际结果：200；  会从接口获取响应码，判断预期结果是否等于实际结果。
- 预期结果：`$.user_id`， 实际结果：`${user_id}`； 会从接口响应数据中通过表达式`$.user_id`提取user_id作为预期结果， 从全局变量中替换变量`${user_id}`获取user_id作为实际结果，判断预期结果是否等于实际结果。
- 预期结果：`$.login`， 实际结果：`${login}`； 会从接口响应数据中通过表达式`$.login`提取login作为预期结果， 从全局变量中替换变量`${login}`获取login作为实际结果，判断实际结果是否包含预期结果。
-  预期结果：`$.user_id`， 实际结果：84955； 会从接口响应数据中通过表达式`$.user_id`提取user_id作为预期结果，判断预期结果是否大于实际结果。
-  预期结果：`$.user_id`， 实际结果：84953； 会从接口响应数据中通过表达式`$.user_id`提取user_id作为预期结果，判断预期结果是否小于实际结果。
-  预期结果：`$.user_id`， 实际结果：85390； 会从接口响应数据中通过表达式`$.user_id`提取user_id作为预期结果，判断预期结果是否不等于实际结果。


### 4. 如何进行数据库断言
以下是支持的几种数据库断言：
|  断言方式 |  说明  |
| ------------ | ------------ |
| len |  数据库SQL查询结果的数量 是否 等于预期结果 |
| eq  | 从数据库SQL查询结果中通过jsonpath表达式提取值，判断是否等于预期结果  |
|...... | 其他断言方式待扩展 |

以下是数据库断言示例-1：
```yaml
  assert_sql:
    eq:
      sql: select count(*) from tokens where user_id=${user_id};
      len: 1
```
- sql表示需要查询的SQL， 这里调用的是`common_utils/mysql_handle.py.MysqlServer.query_one`, 返回的数据类型是字典。
- len:1， 判断的是查询结果的个数是否等于1.
- 该场景一般用于某操作往数据库中插入了一条数据，判断是否插入成功，而不需要去校验其数据准确性。
- 例如上述数据库断言示例中，我是去查询tokens中是否存在指定user_id的数据，其实际场景是只要登录成功，就会往token表里面插入登录用户的token。因此要判断实际是否登录成功，只需要判断表里面有没有针对该用户插入一条数据即可。


以下是数据库断言示例-2：
```yaml
  assert_sql:
    eq:
      sql: select id, `name`, identifier from projects where user_id=${user_id} ORDER BY created_on DESC;
      $.id: ${project_id}
      $.name: ${project_name}
      $.identifier: ${project_identifier}
```
-  sql表示需要查询的SQL， 这里调用的是`common_utils/mysql_handle.py.MysqlServer.query_one`, 返回的数据类型是字典。
- 这里是在projects表里面查询指定用户创建的项目信息（id, `name`, identifier），并按创建时间倒序排序。
- 预期结果：`$.id`， 实际结果：`${project_id}`， 从数据库查询结果中通过表达式`$.id`提取id作为实际结果， 从全局变量中替换变量`${project_id}`获取project_id作为实际结果，判断预期结果是否等于实际结果。
- 预期结果：`$.name`， 实际结果：`${project_name}`， 从数据库查询结果中通过表达式`$.name`提取name作为实际结果， 从全局变量中替换变量`${project_name}`获取project_name作为实际结果，判断预期结果是否等于实际结果。
- 预期结果：`$.identifier`， 实际结果：`${project_identifier}`， 从数据库查询结果中通过表达式`$.identifier`提取identifier作为实际结果， 从全局变量中替换变量`${project_identifier}`获取project_identifier作为实际结果，判断预期结果是否等于实际结果。

注意：
- 关于数据库断言，需要考虑实际使用场景，来综合考虑调整。这里我考虑的可能还有局限性。欢迎大家来反馈。
- 另外，其实sql有很大程度影响数据库断言的走向， 我们写sql的时候尽量写的精准一些。

### 5. 配置邮箱通知
- 首先我们需要在配置文件`config/settings.py`中选择邮件发送方式：SEND_RESULT_TYPE = 3
- 获取邮件的相关信息，并填写到配置文件`config/settings.py`中。这些配置信息可以从邮箱设置中获取。不知道如何配置的，可以直接互联网上搜索。

```python
# 发送邮件的相关配置信息
email = {
    "user": "******",  # 发件人邮箱
    "password": "******",  # 发件人邮箱授权码/发件人邮箱密码
    "host": "smtp.qq.com",
    "to": ["******", "******"]  # 收件人邮箱
}

```

- 在配置文件`config/settings.py`中配置邮件发送的标题以及内容。
注意：
1）以下`${变量名}`是已经定义好的。只能减，不能增。
2）邮件标题以及内容也可自行调整。

```python
# ------------------------------------ 邮件通知内容 ----------------------------------------------------#
email_subject = f"接口自动化报告"
email_content = """
           各位同事, 大家好:

           自动化用例于 <strong>${start_time} </strong> 开始运行，运行时长：<strong>${run_time} s</strong>， 目前已执行完成。
           ---------------------------------------------------------------------------------------------------------------
           测试人：<strong> ${tester} </strong> 
           所属部门：<strong> ${department} </strong>
           项目环境：<strong> ${run_env} </strong>
           ---------------------------------------------------------------------------------------------------------------
           执行结果如下:
           &nbsp;&nbsp;用例运行总数:<strong> ${total} 个</strong>
           &nbsp;&nbsp;通过用例个数（passed）: <strong><font color="green" >${passed} 个</font></strong>
           &nbsp;&nbsp;失败用例个数（failed）: <strong><font color="red" >${failed} 个</font></strong>
           &nbsp;&nbsp;异常用例个数（error）: <strong><font color="orange" >${broken} 个</font></strong>
           &nbsp;&nbsp;跳过用例个数（skipped）: <strong><font color="grey" >${skipped} 个</font></strong>
           &nbsp;&nbsp;失败重试用例个数 * 次数之和（rerun）: <strong>${rerun} 个</strong>
           &nbsp;&nbsp;成  功   率:<strong> <font color="green" >${pass_rate} %</font></strong>

           **********************************
           附件为具体的测试报告，详细情况可下载附件查看， 非相关负责人员可忽略此消息。谢谢。
       """
```


### 6. 配置钉钉通知
- 首先我们需要在配置文件`config/settings.py`中选择钉钉发送方式：SEND_RESULT_TYPE = 1
- 获取钉钉的相关信息，并填写到配置文件`config/settings.py`中。具体可以参考：[钉钉机器人](https://blog.csdn.net/FloraCHY/article/details/130618777?spm=1001.2014.3001.5502 "钉钉机器人")

```python
# ------------------------------------ 钉钉相关配置 ----------------------------------------------------#
ding_talk = {
    "webhook_url": "https://oapi.dingtalk.com/robot/send?access_token=***********",
    "secret": "***********"
}

```
- 在配置文件`config/settings.py`中配置钉钉发送的标题以及内容。
注意：
1）以下`${变量名}`是已经定义好的。只能减，不能增。
2）邮件标题以及内容也可自行调整。
```python
# ------------------------------------ 钉钉通知内容 ----------------------------------------------------#
ding_talk_title = f"接口自动化报告"
ding_talk_content = """
           各位同事, 大家好:

           ### 自动化用例于 ${start_time} 开始运行，运行时长：${run_time} s， 目前已执行完成。
            ---------------------------------------------------------------------------------------------------------------
           #### 测试人： ${tester}
           #### 所属部门： ${department}
           #### 项目环境： ${run_env} 
           ---------------------------------------------------------------------------------------------------------------
           #### 执行结果如下:
           - 用例运行总数: ${total} 个
           - 通过用例个数（passed）: ${passed} 个
           - 失败用例个数（failed）: ${failed} 个
           - 异常用例个数（error）: ${broken} 个
           - 跳过用例个数（skipped）: ${skipped} 个
           - 失败重试用例个数 * 次数之和（rerun）: ${rerun} 个
           - 成  功   率: ${pass_rate} %

           **********************************
           附件为具体的测试报告，详细情况可下载附件查看， 非相关负责人员可忽略此消息。谢谢。
       """
```


### 7. 配置企业微信通知
- 首先我们需要在配置文件`config/settings.py`中选择企业微信发送方式：SEND_RESULT_TYPE = 2
- 获取企业微信的相关信息，并填写到配置文件`config/settings.py`中。具体可以参考：[企业微信](https://blog.csdn.net/FloraCHY/article/details/130624354?spm=1001.2014.3001.5502 "企业微信")
```python
# ------------------------------------ 企业微信相关配置 ----------------------------------------------------#
wechat = {
    "webhook_url": "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=********",
}
```
- 在配置文件`config/settings.py`中配置企业微信发送内容。
注意：
1）以下`${变量名}`是已经定义好的。只能减，不能增。
2）邮件标题以及内容也可自行调整。

```python
# ------------------------------------ 企业微信通知内容 ----------------------------------------------------#
wechat_content = """
           各位同事, 大家好:

           ### 自动化用例于 ${start_time} 开始运行，运行时长：${run_time} s， 目前已执行完成。
           --------------------------------
           #### 测试人： ${tester}
           #### 所属部门： ${department}
           #### 项目环境： ${run_env} 
           --------------------------------
           #### 执行结果如下:
           - 用例运行总数: ${total} 个
           - 通过用例个数（passed）:<font color=\"info\"> ${passed} 个</font>
           - 失败用例个数（failed）: <font color=\"warning\"> ${failed}  个</font>
           - 异常用例个数（error）: <font color=\"warning\"> ${broken} 个</font>
           - 跳过用例个数（skipped）: <font color=\"comment\"> ${skipped} 个</font>
           - 失败重试用例个数 * 次数之和（rerun）: <font color=\"comment\"> ${rerun} 个</font>
           - 成  功   率: <font color=\"info\"> ${pass_rate} % </font>

           **********************************
           附件为具体的测试报告，详细情况可下载附件查看， 非相关负责人员可忽略此消息。谢谢。
       """

```

### 7. 上传文件接口支持
#### 熟悉接口
- 确定上传文件接口的URL
- 确定上传文件接口的METHOD
- 确定上传文件接口请求头里面的Content-Type， 我这边调试的接口都是：multipart/form-data;
- 确定上传文件接口请求参数， 我调试的接口有两种参数形式：

```python
# 第一种
file: 文件二进制内容
	
	
# 第二种
file: 文件二进制内容
language: zh
```
#### 文件上传的逻辑
`common_utils/base_request.py` 中封装的request请求，是使用`from requests_toolbelt import MultipartEncoder`进行文件上传的。

- 针对单文件上传，我们需要传递一个字典，参考如下：
```python
field = {
	{
		'file': (filename, file_content),   # file是接口中文件参数的名称， filename是文件名，file_content是文件二进制内容
		"key": v    # 这里是文件上传的其他参数
	}
}
```

- 针对多文件上传，我们需要传递一个列表嵌套元祖，参考如下：
```python
field =[
	('file', (filename, file_content)),  # file是接口中文件参数的名称， filename是文件名，file_content是文件二进制内容
	('file', (filename, file_content)), # 这里是文件上传的其他参数
	(k, v)  
	]
```


#### 上传文件，不带其他参数
- 我们需要设置： request_type=file
- 然后在files中按照如下格式书写：{接口中文件参数的名称:"文件路径地址"/["文件地址1", "文件地址2"]}

- 参考如下：

```yaml
# 公共参数
case_common:
  allure_epic: GitLink接口（手动编写用例）
  allure_feature: 上传文件模块
  allure_story: 上传文件

# 用例数据
case_upload_demo_01:
  feature: 上传文件
  title: 测试单文件上传
  run: True
  url: /api/attachments.json
  method: POST
  headers:
    cookies: ${login_cookie}
  cookies:
  request_type: file
  payload:
  files:
    file: TOC出库订单导入模板(2).xlsx   # 此处file对应接口中文件参数的名称
  extract:
    file_id: $.id
  assert_response:
    eq:
      http_code: 200
  assert_sql:

case_upload_demo_02:
  feature: 上传文件
  title: 测试多文件上传(该接口不支持多文件上传，这是一个示例)
  run: False
  url: /api/attachments.json
  method: POST
  headers:
    cookies: ${login_cookie}
  cookies:
  request_type: file
  payload:
  files:
    file:
      - 导入TOC订单.xls
      - toc.xls
  extract:
    file_id: $.id
  assert_response:
    eq:
      http_code: 200
  assert_sql:
```

#### 上传文件，带其他参数
- 我们需要设置： request_type=file
- 然后在files中按照如下格式书写：{接口中文件参数的名称:"文件路径地址"/["文件地址1", "文件地址2"]}
- 由于请求参数里面还传递了`language:zh`， 因此我们需要写在`payload`中
- 在`common_utils/base_request.py` 中，我们会将`language:zh`以元祖形式处理到files里面

- 参考如下：

```yaml
# 公共参数
case_common:
  allure_epic: OWMS系统（自动生成用例）  # 敏捷里面的概念，定义史诗，相当于module级的标签, 往下是 feature
  allure_feature: 出库模块  # 功能点的描述，相当于class级的标签, 理解成模块往下是 story
  allure_story: TOC扫描签出接口    # 故事，可以理解为场景，相当于method级的标签, 往下是 title

# 用例数据
case_import_toc_01:
  feature: OMS系统
  title: 导入TOC订单（01）
  run: True
  url:  /oms/retailGoodsTmp/selfImportExcel
  method: POST
  headers:
    Cookietoken: ${oms_cookieToken}
  request_type: file
  payload:
    language: zh
  files:
    file: TOC出库订单导入模板(2).xlsx
  extract:
  assert_response:
    eq:
      $.msg: 成功
  assert_sql:

case_import_toc_02:
  feature: OMS系统
  title: 导入TOC订单（02）
  run: True
  url:  /oms/retailGoodsTmp/selfImportExcel
  method: POST
  headers:
    Cookietoken: ${oms_cookieToken}
  request_type: file
  payload:
    language: zh
  files:
    file:
      - 导入TOC订单.xls
      - toc.xls
  extract:
  assert_response:
    eq:
      $.msg: 成功
  assert_sql:
```




## 初始化项目可能遇到的问题
### 1. 测试机安装的是python3.7，但是本框架要求3.9.5，怎么办？
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

### 2. 无法安装依赖包或者安装很慢，怎么办？
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