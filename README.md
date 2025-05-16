# locustpro
learn locust

## 一、安装locust，配置环境
```shell
mkdir locust_test
cd locust_test
virtualenv env
cd env 
source bin/active
pip install locust
```
## 二、压测的运行方式
### 2.1 任务和虚拟用户分别定义类
- 如下面的脚本
```python
from locust import HttpUser, TaskSet, task, between

class TestLogin(TaskSet):
    def on_start(self) -> None:
        pass
    
    @task
    def test_login(self):
        print("test login ...")
        self.client.get('wwww.baidu.com')

class LoginUsers(HttpUser):
    wait_time = between(1,3)
    tasks = [TestLogin]
    host = "127.0.0.1"
```
### 2.2 虚拟用户中包含任务
- 如下面的脚本
```python
from locust import HttpUser, task, between
class LoginUsers(HttpUser):
    def on_start(self) -> None:
        pass
    
    @task
    def test_login(self):
        self.client.get("www.baidu.com")
    @task
    def test_getAccount(self):
        self.client.post('/getAccount')

    wait_time = between(1,3)
    host = '127.0.0.1'
```
### 2.3 任务执行权重
- 使用@task(1)中传入数字标记，数字越大，权重越大，执行的概率就多,如下面的代码
```python
import os

from locust import HttpUser, task, between


class WightUser(HttpUser):

    @task(1)
    def test_login1(self):
        print("权重1...")

    @task(2)
    def test_login2(self):
        print("权重2...")

    @task(3)
    def test_login3(self):
        print("权重3...")

    host = "127.0.0.1"
    wait_time = between(1,3)


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    os.system("locust -f ./test_task_wight.py -u 1 -t 10s --headless ")
```
- 执行结果如下, 权重3的任务执行的次数最多
```shell
[2025-04-29 17:39:14,434] hb32366deMacBook-Pro/INFO/locust.main: Starting Locust 2.33.0
[2025-04-29 17:39:14,436] hb32366deMacBook-Pro/INFO/locust.main: Run time limit set to 10 seconds
Type     Name                                                                          # reqs      # fails |    Avg     Min     Max    Med |   req/s  failures/s
--------|----------------------------------------------------------------------------|-------|-------------|-------|-------|-------|-------|--------|-----------
--------|----------------------------------------------------------------------------|-------|-------------|-------|-------|-------|-------|--------|-----------
         Aggregated                                                                         0     0(0.00%) |      0       0       0      0 |    0.00        0.00

[2025-04-29 17:39:14,436] hb32366deMacBook-Pro/INFO/locust.runners: Ramping to 1 users at a rate of 1.00 per second
[2025-04-29 17:39:14,436] hb32366deMacBook-Pro/INFO/locust.runners: All users spawned: {"WightUser": 1} (1 total users)
权重3...
权重3...
Type     Name                                                                          # reqs      # fails |    Avg     Min     Max    Med |   req/s  failures/s
--------|----------------------------------------------------------------------------|-------|-------------|-------|-------|-------|-------|--------|-----------
--------|----------------------------------------------------------------------------|-------|-------------|-------|-------|-------|-------|--------|-----------
         Aggregated                                                                         0     0(0.00%) |      0       0       0      0 |    0.00        0.00

权重3...
Type     Name                                                                          # reqs      # fails |    Avg     Min     Max    Med |   req/s  failures/s
--------|----------------------------------------------------------------------------|-------|-------------|-------|-------|-------|-------|--------|-----------
--------|----------------------------------------------------------------------------|-------|-------------|-------|-------|-------|-------|--------|-----------
         Aggregated                                                                         0     0(0.00%) |      0       0       0      0 |    0.00        0.00

权重1...
Type     Name                                                                          # reqs      # fails |    Avg     Min     Max    Med |   req/s  failures/s
--------|----------------------------------------------------------------------------|-------|-------------|-------|-------|-------|-------|--------|-----------
--------|----------------------------------------------------------------------------|-------|-------------|-------|-------|-------|-------|--------|-----------
         Aggregated                                                                         0     0(0.00%) |      0       0       0      0 |    0.00        0.00

权重3...
Type     Name                                                                          # reqs      # fails |    Avg     Min     Max    Med |   req/s  failures/s
--------|----------------------------------------------------------------------------|-------|-------------|-------|-------|-------|-------|--------|-----------
--------|----------------------------------------------------------------------------|-------|-------------|-------|-------|-------|-------|--------|-----------
         Aggregated                                                                         0     0(0.00%) |      0       0       0      0 |    0.00        0.00

[2025-04-29 17:39:24,354] hb32366deMacBook-Pro/INFO/locust.main: --run-time limit reached, shutting down
[2025-04-29 17:39:24,388] hb32366deMacBook-Pro/INFO/locust.main: Shutting down (exit code 0)
Type     Name                                                                          # reqs      # fails |    Avg     Min     Max    Med |   req/s  failures/s
--------|----------------------------------------------------------------------------|-------|-------------|-------|-------|-------|-------|--------|-----------
--------|----------------------------------------------------------------------------|-------|-------------|-------|-------|-------|-------|--------|-----------
         Aggregated                                                                         0     0(0.00%) |      0       0       0      0 |    0.00        0.00

Response time percentiles (approximated)
Type     Name                                                                                  50%    66%    75%    80%    90%    95%    98%    99%  99.9% 99.99%   100% # reqs
--------|--------------------------------------------------------------------------------|--------|------|------|------|------|------|------|------|------|------|------|------
--------|--------------------------------------------------------------------------------|--------|------|------|------|------|------|------|------|------|------|------|------

```
### 2.4 debug模式运行
- 调试请求的时候，可以用debug模式运行，如下面的脚本
```python
from locust import  HttpUser, task, between, run_single_user

class Users(HttpUser):
    wait_time = between(1, 2)
    host = "https://"
    @task
    def test_baidu(self):
        with self.client.get("www.baidu.com", catch_response=True) as response:
            if response.status_code == 200:
                response.success()

if __name__ == "__main__":
    run_single_user(Users, include_context=True, loglevel="INFO")
```
- 上面的脚本运行结果如下, 输入的结果在run_single_user的参数中指定 
```shell
type	name                                              	resp_ms	exception	context		
GET	/                                                 	131    	         		
GET	/                                                 	36     	         		
GET	/                                                 	3163   	         		
GET	/                                                 	1092   	         		
GET	/                                                 	37     	         		
GET	/                                                 	36     	         		
GET	/                                                 	69     	         		
GET	/                                                 	70 
```
### 2.5 更快的vuser, FastHttpUser
- Locust 的默认 HTTP 客户端使用 python-requests。它提供了许多 python 开发人员都熟悉的不错 API，并且维护得非常好。但是，如果您计划以非常高的吞吐量运行测试，并且运行 Locust 的硬件有限，则有时效率不够。
- 因此，Locust 还附带了 FastHttpUser，它使用 geventhttpclient。它提供了一个非常相似的 API，并且使用的 CPU 时间明显减少，有时会将给定硬件上每秒的最大请求数增加多达 5 到 6 倍。
- 在最佳情况下 （在一段时间内执行小请求 True-loop），单个 Locust 进程（仅限于一个 CPU 内核） 可以使用 FastHttpUser 每秒处理大约 16000 个请求，使用 HttpUser 每秒处理 4000 个请求 （在 2021 M1 MacBook Pro 和 Python 3.11 上测试）
- 使用方法，vuser类直接继承 FastHttpUser， 如下面的代码, 它使用rest方法请求restful API， 与python-requests的post请求类似，它是 self.client.request 的包装器, 当然使用self.client.post也是可以的
```python
import random

from locust import FastHttpUser, task, between



headers = {
    'Content-Type': 'application/json',
    'Connection': 'keep-alive',
}
cust_no = ['800000015507',
            '800000026506',
            '800000020502',
            '800000007503',
            '800000018505',
            '800000007004',
            '800000019008',
            '800000002007',
            '800000003015',
            '800000018509',
            '800000003006',
            '800000014522',
            '800000027001',
            '800000006001',
            '800000011002',
            '800000026511',
            '800000008026',
            '800000018511',
            '800000024738',
            '800000007501',
            '800000024745',
            '800000027008',
            '800000008008',
            '800000026007',
            '800000027010',
            '800000026501',
            '800000011512',
            '800000018504'
           ]

class FeatureUser(FastHttpUser):
    wait_time = between(1, 2)
    host = "http://approve-fat.sandbox-shuangqiang.top"

    @task
    def test_feature(self):
        payload = {
            "custNo": random.choice(cust_no),
            "appSystem": "MEX001",
            "subPackage": "HOLA"
        }
        with self.rest("post","/loanapprove/appList/getAllAppListImpress", headers=headers, json=payload) as response:
            if response.status_code != 200:
                response.failure("响应异常！")
                print(response)
            elif response.js is None:
                response.failure("响应异常！")
            elif response.js["retCode"] != "000000":
                response.failure("响应异常！")
                print(response)
            else:
                # print(response.json())
                response.success()
```
### 2.6 Using Locust as a library 
- locust作为库的方式运行, 可以单独允许你的python脚本，而不必使用locust命令，如下面的脚本 test_as_library.py
```python
from locust import HttpUser, events, task
from locust.env import Environment
from locust.log import setup_logging
from locust.stats import stats_history, stats_printer

import gevent

setup_logging("INFO")


class MyUser(HttpUser):
    host = "https://www.baidu.com"

    @task
    def t(self):
        self.client.get("/")


# setup Environment and Runner
env = Environment(user_classes=[MyUser], events=events)
runner = env.create_local_runner()

# start a WebUI instance
web_ui = env.create_web_ui("127.0.0.1", 8089)

# execute init event handlers (only really needed if you have registered any)
env.events.init.fire(environment=env, runner=runner, web_ui=web_ui)

# start a greenlet that periodically outputs the current stats
gevent.spawn(stats_printer(env.stats))

# start a greenlet that save current stats to history
gevent.spawn(stats_history, env.runner)

# start the test
runner.start(1, spawn_rate=10)

# in 30 seconds stop the runner
gevent.spawn_later(30, runner.quit)

# wait for the greenlets
runner.greenlet.join()

# stop the web server for good measures
web_ui.stop()
```
- 则他会在终端窗口中允许测试，结果如下
```shell
/Users/hb32366/devs/locust_asset/venv/bin/python3.13 /Users/hb32366/devs/locust_asset/tests/test_as_library.py 
Type     Name                                                                          # reqs      # fails |    Avg     Min     Max    Med |   req/s  failures/s
--------|----------------------------------------------------------------------------|-------|-------------|-------|-------|-------|-------|--------|-----------
--------|----------------------------------------------------------------------------|-------|-------------|-------|-------|-------|-------|--------|-----------
         Aggregated                                                                         0     0(0.00%) |      0       0       0      0 |    0.00        0.00

[2025-05-15 19:19:37,008] hb32366deMacBook-Pro/INFO/locust.runners: Ramping to 1 users at a rate of 10.00 per second
[2025-05-15 19:19:37,008] hb32366deMacBook-Pro/INFO/locust.runners: All users spawned: {"MyUser": 1} (1 total users)
Type     Name                                                                          # reqs      # fails |    Avg     Min     Max    Med |   req/s  failures/s
--------|----------------------------------------------------------------------------|-------|-------------|-------|-------|-------|-------|--------|-----------
--------|----------------------------------------------------------------------------|-------|-------------|-------|-------|-------|-------|--------|-----------
         Aggregated                                                                         0     0(0.00%) |      0       0       0      0 |    0.00        0.00

Type     Name                                                                          # reqs      # fails |    Avg     Min     Max    Med |   req/s  failures/s
--------|----------------------------------------------------------------------------|-------|-------------|-------|-------|-------|-------|--------|-----------
GET      /                                                                                  2     0(0.00%) |   1622      36    3208     37 |    0.00        0.00
--------|----------------------------------------------------------------------------|-------|-------------|-------|-------|-------|-------|--------|-----------
         Aggregated                                                                         2     0(0.00%) |   1622      36    3208     37 |    0.00        0.00


```
## 三、hooks处理
### 3.1 events.init.add_listener
- 全局初始化处理，最先执行一次，为后续步骤准备
### 3.2 events.test_start.add_listener, events.test_stop.add_listener
- 全局前置处理，后置处理，在所有任务执行前执行一次，所有任务结束后执行一次
### 3.3 on_start(), on_stop()
- 位于测试类中，在所有测试任务执行前执行一次，所有任务结束后执行一次
- 如下面的脚本
```python
import os
from asyncio import tasks

from locust import HttpUser, task, between, events

@events.init.add_listener
def on_test_init(environment, **kwargs):
    print("EVENT ON TEST INIT")

@events.test_start.add_listener
def on_test_start(environment, **kwargs) -> None:
    print("EVENT ON TEST START...")

@events.test_stop.add_listener
def on_test_stop(environment, **kwargs) -> None:
    print("EVENT ON TEST STOP...")

class HangerUser(HttpUser):
    def on_start(self) -> None:
        print("ON START...")

    def on_stop(self) -> None:
        print("ON STOP...")

    @task(1)
    def test_hanger1(self):
        print("HANGER USER TEST 1...")

    @task(2)
    def test_hanger2(self):
        print("HANGER USER TEST 2...")

    wait_time = between(1, 3)



if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    os.system("locust -f ./test_hooks.py -u 1 -t 10s --headless --host 127.0.0.1 ")
```
- 执行结果如下
```shell
[2025-04-29 19:53:12,547] hb32366deMacBook-Pro/INFO/locust.main: Starting Locust 2.33.0
[2025-04-29 19:53:12,549] hb32366deMacBook-Pro/INFO/locust.main: Run time limit set to 10 seconds
Type     Name                                                                          # reqs      # fails |    Avg     Min     Max    Med |   req/s  failures/s
--------|----------------------------------------------------------------------------|-------|-------------|-------|-------|-------|-------|--------|-----------
--------|----------------------------------------------------------------------------|-------|-------------|-------|-------|-------|-------|--------|-----------
         Aggregated                                                                         0     0(0.00%) |      0       0       0      0 |    0.00        0.00

[2025-04-29 19:53:12,550] hb32366deMacBook-Pro/INFO/locust.runners: Ramping to 1 users at a rate of 1.00 per second
[2025-04-29 19:53:12,550] hb32366deMacBook-Pro/INFO/locust.runners: All users spawned: {"HangerUser": 1} (1 total users)
EVENT ON TEST INIT
EVENT ON TEST START...
ON START...
HANGER USER TEST 1...
HANGER USER TEST 1...
Type     Name                                                                          # reqs      # fails |    Avg     Min     Max    Med |   req/s  failures/s
--------|----------------------------------------------------------------------------|-------|-------------|-------|-------|-------|-------|--------|-----------
--------|----------------------------------------------------------------------------|-------|-------------|-------|-------|-------|-------|--------|-----------
         Aggregated                                                                         0     0(0.00%) |      0       0       0      0 |    0.00        0.00

Type     Name                                                                          # reqs      # fails |    Avg     Min     Max    Med |   req/s  failures/s
--------|----------------------------------------------------------------------------|-------|-------------|-------|-------|-------|-------|--------|-----------
--------|----------------------------------------------------------------------------|-------|-------------|-------|-------|-------|-------|--------|-----------
         Aggregated                                                                         0     0(0.00%) |      0       0       0      0 |    0.00        0.00

HANGER USER TEST 1...
Type     Name                                                                          # reqs      # fails |    Avg     Min     Max    Med |   req/s  failures/s
--------|----------------------------------------------------------------------------|-------|-------------|-------|-------|-------|-------|--------|-----------
--------|----------------------------------------------------------------------------|-------|-------------|-------|-------|-------|-------|--------|-----------
         Aggregated                                                                         0     0(0.00%) |      0       0       0      0 |    0.00        0.00

HANGER USER TEST 1...
Type     Name                                                                          # reqs      # fails |    Avg     Min     Max    Med |   req/s  failures/s
--------|----------------------------------------------------------------------------|-------|-------------|-------|-------|-------|-------|--------|-----------
--------|----------------------------------------------------------------------------|-------|-------------|-------|-------|-------|-------|--------|-----------
         Aggregated                                                                         0     0(0.00%) |      0       0       0      0 |    0.00        0.00

HANGER USER TEST 2...
[2025-04-29 19:53:22,448] hb32366deMacBook-Pro/INFO/locust.main: --run-time limit reached, shutting down
[2025-04-29 19:53:22,484] hb32366deMacBook-Pro/INFO/locust.main: Shutting down (exit code 0)
Type     Name                                                                          # reqs      # fails |    Avg     Min     Max    Med |   req/s  failures/s
--------|----------------------------------------------------------------------------|-------|-------------|-------|-------|-------|-------|--------|-----------
--------|----------------------------------------------------------------------------|-------|-------------|-------|-------|-------|-------|--------|-----------
         Aggregated                                                                         0     0(0.00%) |      0       0       0      0 |    0.00        0.00

Response time percentiles (approximated)
Type     Name                                                                                  50%    66%    75%    80%    90%    95%    98%    99%  99.9% 99.99%   100% # reqs
--------|--------------------------------------------------------------------------------|--------|------|------|------|------|------|------|------|------|------|------|------
--------|--------------------------------------------------------------------------------|--------|------|------|------|------|------|------|------|------|------|------|------

ON STOP...
EVENT ON TEST STOP...
```
## 四、标记成功或失败
### 4.1 标记失败
- 使用 response.failure(reason='响应失败！')， 如下面的脚本，所有请求都会被标记成失败
```python
import os

from locust import  HttpUser, task, between

class Users(HttpUser):
    wait_time = between(1, 2)
    host = "https://"
    @task
    def test_baidu(self):
        with self.client.get("www.baidu.com", catch_response=True) as response:
            if response.url != self.host:
                response.failure("域名错误！")
            # else:
            #     response.success()

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    os.system("locust -f test_success_failure.py -u 1 -t 10s --headless ")
```
```shell
[2025-05-07 19:20:33,922] hb32366deMacBook-Pro/INFO/locust.main: Shutting down (exit code 1)
Type     Name                                                                          # reqs      # fails |    Avg     Min     Max    Med |   req/s  failures/s
--------|----------------------------------------------------------------------------|-------|-------------|-------|-------|-------|-------|--------|-----------
GET      /                                                                                  7   7(100.00%) |     61      20     123     63 |    0.81        0.81
--------|----------------------------------------------------------------------------|-------|-------------|-------|-------|-------|-------|--------|-----------
         Aggregated                                                                         7   7(100.00%) |     61      20     123     63 |    0.81        0.81

Response time percentiles (approximated)
Type     Name                                                                                  50%    66%    75%    80%    90%    95%    98%    99%  99.9% 99.99%   100% # reqs
--------|--------------------------------------------------------------------------------|--------|------|------|------|------|------|------|------|------|------|------|------
GET      /                                                                                      63     64     85     85    120    120    120    120    120    120    120      7
--------|--------------------------------------------------------------------------------|--------|------|------|------|------|------|------|------|------|------|------|------
         Aggregated                                                                             63     64     85     85    120    120    120    120    120    120    120      7

Error report
# occurrences      Error                                                                                               
------------------|---------------------------------------------------------------------------------------------------------------------------------------------
7                  GET /: 域名错误！                                                                                        
------------------|---------------------------------------------------------------------------------------------------------------------------------------------

```
### 4.2 标记成功 
- 使用 response.success()，如下面的脚本, 则所有的请求都会被标记为成功
```python
import os

from locust import  HttpUser, task, between

class Users(HttpUser):
    wait_time = between(1, 2)
    host = "https://"
    @task
    def test_baidu(self):
        with self.client.get("www.baidu.com", catch_response=True) as response:
            if response.status_code == 200:
                response.success()

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    os.system("locust -f test_success_failure.py -u 1 -t 10s --headless ")
```
```shell
[2025-05-07 19:25:47,326] hb32366deMacBook-Pro/INFO/locust.main: --run-time limit reached, shutting down
[2025-05-07 19:25:47,362] hb32366deMacBook-Pro/INFO/locust.main: Shutting down (exit code 0)
Type     Name                                                                          # reqs      # fails |    Avg     Min     Max    Med |   req/s  failures/s
--------|----------------------------------------------------------------------------|-------|-------------|-------|-------|-------|-------|--------|-----------
GET      /                                                                                  5     0(0.00%) |    511      47    1163    140 |    0.56        0.00
--------|----------------------------------------------------------------------------|-------|-------------|-------|-------|-------|-------|--------|-----------
         Aggregated                                                                         5     0(0.00%) |    511      47    1163    140 |    0.56        0.00

Response time percentiles (approximated)
Type     Name                                                                                  50%    66%    75%    80%    90%    95%    98%    99%  99.9% 99.99%   100% # reqs
--------|--------------------------------------------------------------------------------|--------|------|------|------|------|------|------|------|------|------|------|------
GET      /                                                                                     140   1100   1100   1200   1200   1200   1200   1200   1200   1200   1200      5
--------|--------------------------------------------------------------------------------|--------|------|------|------|------|------|------|------|------|------|------|------
         Aggregated                                                                            140   1100   1100   1200   1200   1200   1200   1200   1200   1200   1200      5

```
## 五、分布式压测
### 5.1 master
- master表示主节点，用于控制压测，执行下面的命令后，会打开web服务，同时等待子节点的连接
```shell
locust -f risk/test_applist_feature.py --master
```
- master主节点启动成功后会输出web控制台地址，访问即可打开控制台
```shell
locust.main: Starting Locust 2.33.0
locust.main: Starting web interface at http://0.0.0.0:8089, press enter to open your default browser.
```
- 子节点连接成功后，会输出相应的节点
```shell
[2025-05-06 20:27:48,157] hb32366deMacBook-Pro/INFO/locust.runners: hb32366deMacBook-Pro.local_9256083c217b4d6189aa9c2d13bc22fb (index 0) reported as ready. 1 workers connected.
[2025-05-06 20:27:58,445] hb32366deMacBook-Pro/INFO/locust.runners: hb32366deMacBook-Pro.local_913c9ca6296847f6b594ebcd41305f97 (index 1) reported as ready. 2 workers connected.
[2025-05-06 20:28:09,595] hb32366deMacBook-Pro/INFO/locust.runners: hb32366deMacBook-Pro.local_5a72cb6d4dd043b3bc414edd961eb6ae (index 2) reported as ready. 3 workers connected.
[2025-05-06 20:28:15,723] hb32366deMacBook-Pro/INFO/locust.runners: hb32366deMacBook-Pro.local_3a31caa8d1174ba3ba770fdffc476276 (index 3) reported as ready. 4 workers connected.
[2025-05-06 20:28:25,514] hb32366deMacBook-Pro/INFO/locust.runners: hb32366deMacBook-Pro.local_ce356bb9ce97448f884eb81206c4a612 (index 4) reported as ready. 5 workers connected.
```
### 5.2 worker
- worker表示子节点，每个子节点会分配一定的vuser, 它使用的是协程，会占用一定的cpu和内存资源，开子节点时如果不指定host,默认事127.0.0.1
```shell
(venv) hb32366@hb32366deMacBook-Pro locust_asset % locust -f risk/test_applist_feature.py --worker --host 127.0.0.1 
[2025-05-07 19:38:55,104] hb32366deMacBook-Pro/INFO/locust.main: Starting Locust 2.33.0
```
- 使用 --host 参数指定 host后，就会连接到host对应的master节点上，master会输出
```shell
[2025-05-07 19:38:55,112] hb32366deMacBook-Pro/INFO/locust.runners: hb32366deMacBook-Pro.local_8238c824b4004fe299e82fa8533190db (index 0) reported as ready. 1 workers connected.

```
## 六、第三方扩展 locust-plugins
- 安装locust-plugins 其他协议负载测试
### 
- 