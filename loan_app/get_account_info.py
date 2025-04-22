import random

"""
locust 的前后置处理
@events.init.add_listener 初始化前置，在左右任务启动前执行
@events.test_start.add_listener  所有任务开始前，执行一次
@events.test_stop.add_listener   所有任务执行结束后，执行一次
def on_test_start(**kwargs):  每个user启动器执行一次
def on_test_stop(**kwargs): 每个user结束时执行一次
"""
from locust import task, HttpUser, between, TaskSet, events
from locust.runners import MasterRunner

@events.init.add_listener
def on_locust_init(environment, **kwargs):
    if isinstance(environment.runner, MasterRunner):
        print("I'm on master node")
    else:
        print("I'm on a worker or standalone node")

@events.test_start.add_listener
def on_test_start(**kwargs):
    print("全部开始........................")

@events.test_stop.add_listener
def on_test_stop(**kwargs):
    print("全部结束.......................")

class AccountTaskSet(TaskSet):
    headers = {"appSystem": "MEX001",
               "subPackage": "HOLA",
               "prodCode": "02",
               "secret": "0",
               "versionCode": "2",
               "Content-Type": "application/json",
               "User-Agent": "locust"}
    def on_start(self):
        """
        :return: token
        """
        payload = {
            "phone": "8100000001",
            "password": "123456",
            "appsflyerId": "17407335963650-16001159720116582816",
            "fireBaseId": "",
            "isNew": "false"}
        with self.client.post("/loanapp/api/intent/loginPwd", headers=self.headers,
                              json=payload, catch_response=True) as response:
            print("每个user开始 ...............")
            json_data = response.json()
            if json_data["success"] is True:
                response.success()
                self.headers.update({"token": json_data["data"]["token"]})
                self.headers.update({"uid": json_data["data"]["custNo"]})
            else:response.failure("失败")

    @task
    def expect_credit(self):
        payload = {"expectCreditAmount": random.randint(200, 30000)}
        # print(self.headers)
        with self.client.post("/loanapp/api/custAccountInfo/editExpectCredit", headers=self.headers, json=payload,
                              catch_response=True) as response:
            # print(response.json())
            json_data = response.json()
            if json_data["success"] is True:
                response.success()
            else: response.failure("失败")
    @task
    def test_on_start_stop(self):
        print("test_on_start_stop...")

    def on_stop(self):
        self.headers.pop("token", None)
        print("每个user结束 ...............")

class AccountUser(HttpUser):
    wait_time = between(1, 2)
    tasks = [AccountTaskSet]
    host = "http://app-fat.sandbox-shuangqiang.top"
