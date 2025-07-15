from locust import FastHttpUser, SequentialTaskSet, task, between
import logging as log
from queue import Queue

phone_queue = Queue()
for phone in range(2000000000, 2000010000):
    """
    使用线程取手机号，避免重复
    """
    phone_queue.put(phone)

class RegisterAndCredit(SequentialTaskSet):
    def on_start(self):
        """
        :return: 每次启动前先生成一个手机号
        """
        if phone_queue.empty():
            log.error("手机号用尽！")
            self.environment.runner.quit()
        else:
            self.mobile = phone_queue.get()
            log.info(f"分配手机号：{self.mobile}")

    @task
    def check_mobile(self):
        if self.mobile > 2000000020:
            log.error(f"手机号已注册: {self.mobile}")
            self.interrupt()
        else:
            log.info(f"手机号未注册: {self.mobile}")

    @task
    def register(self):
        if self.mobile > 2000000015:
            log.error(f"❌登录失败！: {self.mobile}")
            self.interrupt()
        else:
            log.info(f"✅登录成功!: {self.mobile}")

    @task
    def submit_user_info(self):
        if self.mobile > 2000000008:
            log.error(f"❌用户信息提交失败: {self.mobile}")
            self.interrupt()
        else:
            log.info(f"用户信息提交成功: {self.mobile}")

    @task
    def get_credit_limit(self):
        if self.mobile > 2000000004:
            log.error(f"❌获取用户额度失败: {self.mobile}")
            self.interrupt()
        else:
            log.info(f"获取用户额度成功: {self.mobile}")
            self.interrupt()


class VirtualUser(FastHttpUser):
    wait_time = between(1, 3)
    tasks = [RegisterAndCredit]
    host = "http://127.0.0.1"