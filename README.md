# python + request + pytest+ pytest-html集成的API自动化测试框架

**对于框架任何问题，欢迎联系我！**

#### 一、框架功能说明

**解决痛点：**

1. 通过**session会话方式**，解决了登录之后**cookie关联**处理

```
模块： case_utils.requests_handle 
相关代码：cls.session = requests.Session()
```

2. 框架天然支持接口**动态传参、关联**灵活处理

```
1) 通过全局变量替换用例数据值
用例数据中，存在如下格式 data: { "user_id": "${user_id}"}
全局变量GLOBAL_VAR中存在user_id=84522，通过替换后，最终变为：{ "user_id": 84522}

2) 通过执行函数替换用例数据值
用例数据中，存在如下格式 "repository_name": ${faker.name().replace(" ", "").replace(".", "")}。
通过代码替换后，最终变为："repository_name": "Mike"

```

3. 支持**Excel、Yaml文件**格式编写接口用例，通过简单配置框架自动读取并执行

```
通读取配置文件 config.settings.py中的CASE_FILE_TYPE决定是运行excel/yaml用例，也可都读取
```

4. 执行环境**一键切换**，解决**多环境**相互影响问题

```
1) 通过pytest_addoption将命令行参数--env添加到pytest配置对象中
2) 通过get_config去配置文件config.settings.py中读取不同环境的配置信息，包括域名，测试账号
3) 在主运行文件run.py中通过click模块，读取输入的-env的值
4) 最后在运行时输入 python run.py -env=test可以指定运行的环境
```

5. 支持**http/https协议各种请求、传参类型**接口


6. 响应数据格式支持**json、str类型**的提取操作

```
通过request_handle.after_extract根据响应数据进行提取
```

7. 断言方式支持**等于、包含、大于、小于、不等于**等方法

```
用例数据中通过字段validate进行断言。通过断言的关键字eq等，决定断言是等于、包含、大于、小于、不等于。
具体断言逻辑见case_utils.assert_util
```

8. 框架可以直接交给**不懂代码的功能测试人员使用**，只需要安装规范编写接口用例就行

```
只需要按照yaml或者excel格式正确编写测试用例，即可自动生成测试用例文件，运行测试用例
```

9. 框架也可以交给**懂代码的功能测试人员使用**，可以在test_case目录下通过python编写脚本

```
脚本的编写规范符合pytest要求即可。
注意：框架默认在pytest.ini中配置了只运行test_auto_case目录下的用例，如果需要运行其他符合pytest要求的用例，需要注释掉该配置：testpaths = ./test_auto_case
```

10. 采用luguru管理日志，可以输出更为优雅，简洁的日志

#### 二、框架使用说明

1. 拉取代码到本地

2. 使用pipenv管理安装环境。

```
python版本要求：3.9.5
安装pipenv: pip install pipenv（必须在项目根目录下）
创建虚拟环境：pipenv install （必须在项目根目录下执行）
激活已存在的虚拟环境（如果不存在会创建一个）：pipenv shell （必须在项目根目录下执行）
查看项目虚拟环境路径： pipenv --venv
退出虚拟环境：exit

注意：使用pipenv install会自动安装Pipfile里面的依赖包，该依赖包仅安装在虚拟环境里，不安装在测试机。

注意检查一下pip的安装源（位置：Pipfile）
以下安装源均可：
pip默认的镜像地址是：https://pypi.org/simple
清华大学：https://pypi.tuna.tsinghua.edu.cn/simple 清华大学的pip源是官网pypi的镜像，每隔5分钟同步一次，重点推荐！！！

阿里云：http://mirrors.aliyun.com/pypi/simple/

中国科技大学 https://pypi.mirrors.ustc.edu.cn/simple/

华中理工大学：http://pypi.hustunique.com/

山东理工大学：http://pypi.sdutlinux.org/

豆瓣：http://pypi.douban.com/simple/
```

3. 更改配置文件config.settings.py，修改用例文件读取来源CASE_FILE_TYPE，以及配置test和live环境及测试账号

4. 在data目录下新建测试用例数据文件，编写测试用例 （Excel或者Yaml）或者在test_case目录下通过python语言编写用例

5. 框架主入口为 run.py文件
```
	必须在项目根目录下，输入命令运行（如果依赖包是安装在虚拟环境中，需要先启动虚拟环境）。
    注意：本机环境中没有安装依赖包的情况下，不要直接在run.py中右键直接run
  > python run.py  (默认在test环境运行测试用例)
  > python run.py -env live 在live环境运行测试用例
  > python run.py -env=test 在test环境运行测试用例
```

#### 三、框架使用过程中遇到的问题
##### 测试机安装的是python3.7，但是本框架要求3.9.5，怎么办？
方法一：建议采纳此方法
1）首先在项目根目录下打开命令窗口，移除虚拟环境：pipenv --rm
2）安装虚拟环境时忽略锁定的版本号，同时安装依赖包：pipenv install --skip-lock
如果使用上述命令报错：Warning: Python 3.9 was not found on your system... Neither 'pyenv' nor 'asdf' could be found to install Python.
请使用如下命令：pipenv install --pyhon 3.7 --skip-lock  (注意：这里的版本号，如果你的是3.8，就应该如下写命令：pipenv install --python 3.8 --skip-lock)

3）激活虚拟环境：pipenv shell

4）运行框架：python run.py


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