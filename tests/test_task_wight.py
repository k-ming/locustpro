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