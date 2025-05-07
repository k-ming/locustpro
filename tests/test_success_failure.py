import os

from locust import  HttpUser, task, between

class Users(HttpUser):
    wait_time = between(1, 2)
    host = "https://"
    @task
    def test_baidu(self):
        with self.client.get("www.baidu.com", catch_response=True) as response:
            # if response.url != self.host:
            #     response.failure("域名错误！")
            if response.status_code == 200:
                response.success()

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    os.system("locust -f test_success_failure.py -u 1 -t 10s --headless ")