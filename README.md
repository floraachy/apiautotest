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
* 数据库断言: 直接在测试用例中写入查询的sql即可断言，无需编写代码 
* 动态多断言: 如接口需要同时校验响应数据和sql校验，支持多场景断言
* 框架天然支持接口动态传参、关联灵活处理
* 支持测试数据分析，测试数据不符合规范有预警机制
* 支持通过用例数据动态配置pytest.mark， 包括自定义标记，pytest.mark.skip以及pytest,mark.usefixtues
* 测试数据隔离, 实现数据驱动
* 自动生成用例代码: 测试人员在yaml/excel文件中填写好测试用例, 程序可以直接生成用例代码，纯小白也能使用
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
│    ├────assert_handle.py  断言处理， 包括响应断言和数据库断言
│    ├────case_data_analysis  分析用例数据是否符合规范
│    ├────case_fun_handle.py   根据配置文件，从指定类型文件中读取用例数据，并调用生成用例文件方法，生成用例文件
│    ├────data_handle.py    数据处理
│    ├────extract_data_handle.py    提取数据的一些方法
│    ├────get_results_handle.py   从pytest-html/allure测试报告中获取测试结果
│    ├────platform_handle.py  跨平台的支持allure，用于生成allure测试报告
│    ├────request_data_handle.py   针对用例数据进行请求前后的处理
│    └────send_result_handle.py   根据配置文件，从html测试报告中获取测试结果，发送指定类型的通知
├────common_utils/  公共的工具类
│    ├────__init__.py
│    ├────base_request.py   封装的requests请求
│    ├────bs4_handle.py  bs4（BeautifulSoup4）是Python中的第三方库。可以从HTML或XML文件中提取数据的Python库。
│    ├────dingding_handle.py   封装的钉钉机器人
│    ├────excel_handle.py  处理excel
│    ├────files_handle.py   处理文件相关操作
│    ├────func_handle.py   函数装饰器
│    ├────http_server.py   封装的HTTP服务
│    ├────mysql_handle.py  使用pymysql模块连接mysql数据库的公共方法
│    ├────time_handle.py  封装处理时间操作的一些方法
│    ├────wechat_handle.py  封装企业微信机器人
│    ├────yagmail_handle.py  封装通过yagmail发送邮件的方法
│    └────yaml_handle.py  处理yaml文件
├────config/
│    ├────__init__.py
│    ├────allure_config/
│    │    ├────gitlinklogo.jpg    保存用来替换allure报告的logo的，在代码中无用处
│    │    ├────http_server.exe    http服务，用来放置在allure压缩包中，方便在不安装allure环境下打开allure报告
│    │    ├────logo.svg   保存用来替换allure报告的logo的，在代码中无用处
│    │    ├────双击打开Allure报告.bat    .bat文件，用来放置在allure压缩包中，方便在不安装allure环境下打开allure报告
│    ├────pytest_html_config/
│    │    ├────pytest_html_report.css  改变pytest-html测试报告的样式文件
│    ├────case_template.txt  自动生成的测试用例文件模板
│    ├────global_vars.py    保存的一些全局变量
│    ├────path_config.py    项目路径管理
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
│    ├────test_auto_case/     自动生成的测试用例目录
│    │    ├────test_login_demo.py
│    │    ├────test_login_excel_demo.py
│    │    └────test_new_project_demo.py
│    └────test_manual_case/   手动编写的测试用例目录
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
case_common ：公共参数
  allure_epic：用作于@allure.epic()装饰器中的内容。
  allure_feature：用作于@allure.feature()装饰器中的内容。
  allure_story：用作于@allure.story()装饰器中的内容。
  case_markers: 给测试方法添加标记，支持自定义标记，skip, usefixtures。 格式是列表嵌套字符串或者字典。例如：['glcc', {'skip': '跳过执行该用例'}]
                  
case_001：用例ID
  feature：用例所属模块， 类似于@allure.feature()。
  title：用例标题
  run：是否执行用例，为空或者True都会执行，为False则不执行。
  url：请求路径（可填写全路径 或者 资源路径）。通常我们填写资源路径。在用例执行前，会针对路径进行处理。具体可见case_utils.request_data_handle.py.RequestPreDataHandle.url_handle。注：请求路径=基准路径（host/base_url）+资源路径(url)。
  method：请求方式，例如：GET, POST, DELETE, PUT, PATCH等
  headers：请求头，注意如果在headers里面防止cookies，其值类型需要是字符串
  cookies：请求cookies，格式是：DICT， CookieJar对象
  request_type：请求数据类型：params, json, file, data
  payload：请求参数
  files: 需要上传的文件，参考如下传参：{接口中文件参数的名称:'文件路径地址'/['文件地址1', '文件地址2']}
  extract：后置提取参数
  assert_response：响应断言
  assert_sql：数据库断言
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

## 七、运行自动化测试
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

## 八、查看测试报告
### pytest-html测试报告
如果是pytest-html生成的测试报告，直接打开`outputs`目录下的`.html`报告即可。支持通过任意浏览器打开查看

### Allure测试报告
1. 如果是Allure生成的测试报告，支持通过pycharm，点击`outputs/report/allure_html/index.html`打开查看测试报告
2. 如果不通过pycharm打开，直接通过文件夹打开，windows系统环境下，可以点击`outputs/report/allure_html/双击打开Allure报告.bat`打开查看测试报告

注意：
- 通过点击`outputs/report/allure_html/双击打开Allure报告.bat`打开测试报告的方法，暂时不支持mac系统
- 如果通过点击`outputs/report/allure_html/双击打开Allure报告.bat`打开测试报告，命令窗口显示乱码，或者打不开，可以把`.bat`的文件名称修改为英文的名称，里面的所有中文注释全部移除，再次尝试


## 九 、详细功能说明
- [如何实现动态数据、随机数据的热加载？](https://www.gitlink.org.cn/zone/tester/newdetail/236)
我们有些特殊的场景，可能会涉及到一些定制化的数据，每次执行数据，需要按照指定规则随机生成，实时加载数据，那么这部分应该如何处理呢？
  
- [如何处理同一环境存在多域名的情况？](https://www.gitlink.org.cn/zone/tester/newdetail/234)
很多公司，通常一套环境是由多个微服务组成。每一个微服务具备不同的域名。那么针对这种同一环境存在多域名的情况，我们应该如何处理呢？

- [如何处理同一套框架测试多套环境的情况？](https://www.gitlink.org.cn/zone/tester/newdetail/233)
假如我想要我的自动化代码分别在不同环境执行，如何处理呢？

- [如何处理用例中需要依赖登录的token/cookies的情况？](https://www.gitlink.org.cn/zone/tester/newdetail/235)
我们进行测试的时候，很多接口都是需要先登录之后再进行操作。但是我们不可能每测试一次接口，都登录一次吧，这样有点冗余了。那么，针对这种情况如何处理呢？
  
- [如何测试上传文件接口？](https://www.gitlink.org.cn/zone/tester/newdetail/238)
我们通过MultipartEncoder的方式进行文件上传。

- [如何通过用例数据动态配置pytest.mark](https://www.gitlink.org.cn/zone/tester/newdetail/257)
在测试过程中，我们经常需要对测试用例进行分类，运行时仅执行这一类用例。为了实现这一功能，我在测试用例中引入了添加pytest的自定义标记的功能，同时扩展支持了pytest.mark.skip以及pytest,mark.usefixtues。
注意：目前这一功能，仅支持通过YAML格式编写用例。EXCEL用例暂时不支持。

- [如何提取响应数据作为全局变量并使用？](https://www.gitlink.org.cn/zone/tester/newdetail/237)
在测试过程中，通常下一个接口需要用到上一个接口的响应数据，这个时候就涉及到参数的提取。

- [如何进行响应数据断言？](https://www.gitlink.org.cn/zone/tester/newdetail/239)
目前支持5种响应断言方式：eq， in， gt， lt， not。

- [如何进行数据库断言？](https://www.gitlink.org.cn/zone/tester/newdetail/240)
目前暂时支持两种数据库断言方式：len， eq。其他方式待扩展。

- [如何配置邮箱通知？](https://www.gitlink.org.cn/zone/tester/newdetail/242)
我们通过第三方模块yagmail发送邮件。

- [如何配置钉钉通知？](https://www.gitlink.org.cn/zone/tester/newdetail/243)
我们通过封装钉钉机器人发送钉钉通知。

- [如何配置企业微信通知？](https://www.gitlink.org.cn/zone/tester/newdetail/241)
我们通过封装企业微信机器人发送通知。



## 十、初始化项目可能遇到的问题
- [测试机安装的是python3.7，但是本框架要求3.9.5，怎么办？](https://www.gitlink.org.cn/zone/tester/newdetail/245)
- [无法安装依赖包或者安装很慢，怎么办？](https://www.gitlink.org.cn/zone/tester/newdetail/244)

