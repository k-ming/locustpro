import time
from locust import User, task, between, events
from pymysql import connect


class MySQLClient:
    def __init__(self):
        self.cursor = None
        try:
            self.conn = connect(
                host="122.8.184.129",
                port=3306,
                user="mx-cust-fat",
                password="F#46cbJTb89ks",
                database="mx-cust-fat"
            )
            print(self.conn)
        except Exception as e:
            raise e


    def query(self):
        self.cursor = self.conn.cursor()
        # result = self.conn.query(' SELECT * FROM cust_account_info where mobile_no=8100000006 ')
        self.cursor.execute(' SELECT * FROM cust_account_info where mobile_no=8100000006 ')
        result = self.cursor.fetchall()
        self.cursor.close()
        return result
        # print(result)

class DatabaseUser(User):
    wait_time = between(0.5, 2)  # 模拟用户思考时间
    db_client = None

    def on_start(self):
        if not self.db_client:
            self.db_client = MySQLClient()

    @task
    def run_query(self):
        try:
            self.db_client.query()
        except Exception as e:
            raise e



