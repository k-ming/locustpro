from locust import HttpUser, TaskSet, task, between
'''
tasks 和 virtual users 分开定义
task类需继承自TaskSet， 方法需加@task装饰器
前置处理 on_start() 方法用户来获取token 和 user信息
virtual user 继承自HttpUser, 使用tasks=[TaskClass] 来装置任务
virtual user 可设置 wait_time(max, min), host 等
'''

class EventReport(TaskSet):
    headers = {"appSystem": "MEX001",
               "subPackage": "HOLA",
               "prodCode": "02",
               "secret": "0",
               "versionCode": "2",
               "Content-Type": "application/json",
               "User-Agent": "locust"}
    cust_no = None
    token = None

    def on_start(self):
        payload = {
            "phone": "8100000004",
            "password": "123456",
            "appsflyerId": "17407335968660-16001159720116582542",
            "fireBaseId": "",
            "isNew": 'false'
        }
        with self.client.post("/loanapp/api/intent/loginPwd", headers=self.headers, json=payload,
                             catch_response=True) as response:
            # print(response.json())
            if response.json()['success'] is True :
                response.success()
                self.cust_no = response.json()['data']['custNo']
                self.token = response.json()['data']['token']
                # print(response.text)
            else:
                response.failure('登录失败')
    @task(1)
    def report_t1(self):
        payload = {
            "appVersion": "1.0.1",
            "custNo": self.cust_no,
            "screenWidth": "720.0",
            "tempDeviceId": "KH5zyWfuUEVoKwyTt0mBCC4tPWynOWbR1741845232921",
            "ip": "172.17.171.12",
            "module": "Home",
            "screenHeight": "1604.0",
            "eventScene": "Home",
            "isFirstDayVisit": 'false',
            "deviceTime": 1741845948034,
            "isUsingWifi": 'true',
            "currentChannel": "com.android.shell",
            "deviceId": "2089422a027bc36da94af301a9ca65e50",
            "operatingSystem": "android",
            "operatingSystemVersion": "34",
            "carrierName": "",
            "currentSubpackage": "HOLA",
            "firebaseId": "",
            "subEventType": "Home- Solicitar un pr?stamoHome-Exposure",
            "subModule": "Home",
            "deviceModel": "CPH2669",
            "appSystem": "MEX001",
            "networkType": "wifi",
            "deviceBrand": "OPPO"
        }
        with self.client.post("/loanapp/api/event/appReport", headers=self.headers, json=payload,
                             catch_response=True) as response:
            # print(response.json())
            if response.json()['success']:
                response.success()
                # print(response.text)
            else:
                response.failure('上报失败')
    @task(2)
    def report_t2(self):
        payload = {"appVersion": "1.0.1", "custNo": self.cust_no, "screenWidth": "720.0",
                   "tempDeviceId": "KH5zyWfuUEVoKwyTt0mBCC4tPWynOWbR1741845232921", "ip": "172.17.171.12",
                   "module": "Start", "screenHeight": "1604.0", "eventScene": "Background app",
                   "isFirstDayVisit": 'false', "deviceTime": 1741846445145, "isUsingWifi": 'true',
                   "currentChannel": "com.android.shell", "deviceId": "2089422a027bc36da94af301a9ca65e50",
                   "operatingSystem": "android", "operatingSystemVersion": "34", "carrierName": "",
                   "currentSubpackage": "HOLA", "firebaseId": "",
                   "subEventType": "Background -Background -Background  app", "subModule": "Background app",
                   "deviceModel": "CPH2669", "appSystem": "MEX001", "networkType": "wifi", "deviceBrand": "OPPO"}
        with self.client.post("/loanapp/api/event/appReport", headers=self.headers, json=payload,
                             catch_response=True) as response:
            # print(response.json())
            if response.json()['success']:
                response.success()
                # print(response.text)
            else:
                response.failure('上报失败')

class EventReportUser(HttpUser):
    tasks = [EventReport]
    wait_time = between(1, 2)
    host = "http://app-fat.sandbox-shuangqiang.top"
