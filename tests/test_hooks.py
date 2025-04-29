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