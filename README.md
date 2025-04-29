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
## 五、分布式压测
### 5.1 master
### 5.2 worker
## 六、其他对象压测
### 6.1 pgsql
### 6.2 rpc接口压测