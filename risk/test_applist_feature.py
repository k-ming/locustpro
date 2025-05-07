import os
import random

from locust import HttpUser, TaskSet, task, between

class FeatureTaskSet(TaskSet):
    def on_start(self):
        pass

    def on_stop(self):
        pass

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

    @task
    def test_feature(self):
        payload = {
            "custNo": random.choice(self.cust_no),
            "appSystem": "MEX001",
            "subPackage": "HOLA"
        }
        with self.client.post("/loanapprove/appList/getAllAppListImpress", headers=self.headers, json=payload, catch_response=True) as response:
            if response.status_code != 200:
                response.failure("响应异常！")
                print(response)
            elif not response.json():
                response.failure("响应异常！")
                print(response)
            elif response.json().get("retCode") != "000000":
                response.failure("响应异常！")
                print(response)
            else:
                # print(response.json())
                response.success()
            # print(payload)

class FeatureUser(HttpUser):
    tasks = [FeatureTaskSet]
    wait_time = between(1, 2)
    host = "http://approve-fat.sandbox-shuangqiang.top"
