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
                print(response.text)
            elif response.js is None:
                response.failure("响应异常！")
            elif response.js["retCode"] != "000000":
                response.failure("响应异常！")
                print(response.text)
            else:
                response.success()

        # with self.client.post("/loanapprove/appList/getAllAppListImpress", headers=headers, json=payload, catch_response=True) as response:
        #     if response.status_code != 200:
        #         response.failure("响应异常！")
        #         print(response)
        #     elif response.json() is None:
        #         response.failure("响应异常！")
        #     elif response.json().get("retCode") != "000000":
        #         response.failure("响应异常！")
        #         print(response)
        #     else:
        #         # print(response.json())
        #         response.success()
        #     # print(payload)

