
from locust import HttpUser, task, tag, run_single_user

'''
只定义virtual user 继承自 HttpUser
在内部定义 方法，使用@task 装饰器装载任务
使用@tag(str) 来加标签, 执行任务时使用 -T tag1 tag2 来执行任务， 使用 -E tag1  tag2 来过滤掉任务
'''

class CheckUser(HttpUser):
    headers = {"appSystem": "MEX001",
               "subPackage": "HOLA",
               "prodCode": "02",
               "secret": "0",
               "versionCode": "2",
               "Content-Type": "application/json",
               "User-Agent": "locust"}

    @task(0)
    @tag('check0')
    def check(self):
        for num in range(9100000000, 9100000099):
            with self.client.post('/loanapp/api/intent/checkRegisterUser', headers=self.headers,
                                  json={"phone": str(num)}, catch_response=True, name="check1") as e:
                # print(e.text,{"phone": str(num)})
                res = e.json()
                if res['success'] is False:
                    e.failure("失败")
                e.success()
    @task(0)
    @tag('check1')
    def check2(self):
        for num in range(9100000000, 9100000099):
            with self.client.post('/loanapp/api/intent/checkRegisterUser', headers=self.headers,
                                  json={"phone": str(num)}, catch_response=True, name="check2") as e:
                # print(e.text,{"phone": str(num)})
                res = e.json()
                if res['success'] is False:
                    e.failure("失败")
                e.success()

    @task(10)
    @tag(' heartBeat')
    def heartBeat(self):
        with self.client.get('/loanapp/HeartBeat/heartBeat', headers=self.headers, catch_response=True, name="heartBeat") as e:
            res = e.json()
            if res['success'] is False:
                e.failure()
            e.success()

    host = "http://app-fat.sandbox-shuangqiang.top"
    min_wait = 1000
    max_wait = 3000


if __name__ == '__main__':
    run_single_user(CheckUser, include_context=True, loglevel="INFO")