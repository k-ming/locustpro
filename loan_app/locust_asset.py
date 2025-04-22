import random

from locust import HttpUser, TaskSet, task, tag, between
from setuptools.command.alias import alias


class Tasks(TaskSet):
    headers = {"appSystem": "MEX001",
               "subPackage": "HOLA",
               "prodCode": "02",
               "secret": "0",
               "versionCode": "2",
               "Content-Type": "application/json",
               "User-Agent": "locust"}
    path = "/loanapp/api/intent/sendSmsCode"

    @task(1)
    def confirm_credit(self):
        for num in range(9100000000, 9100000099):
            with self.client.post(self.path, headers=self.headers, json={"phone": num, "verifyType": "02"},
                                  name="发送验证码", catch_response=True) as response:
                # print(response.text, {"phone": num})
                json_data = response.json()
                if json_data["success"] is False:
                    response.failure("失败")
                response.success()

class VirUser(HttpUser):
    tasks = [Tasks]
    host = "http://app-fat.sandbox-shuangqiang.top"
    wait_time = between(1, 3)
    # min_wait = 1000
    # max_wait = 5000
