from locust import HttpUser, TaskSet, task, between

"""
风控特征获取接口压测
"""

class TestRiskFeature(TaskSet):
    headers = {
        "Content-Type": "application/json",
        "Connection": "keep-alive",
    }

    @task
    def request_feature(self):
        payload ={
            "async": True,
            "createTime": "",
            "disabledCache": False,
            "eventCode": "P1001",
            "eventFlag": True,
            "impressList": [
                "local_applist_loan_app_updated_720d_cnt",
                "local_applist_genreid_game_action_90d_cnt"
            ],
            "impressSet": [],
            "newData": True,
            "payload": {
                "cust_no": "800000007004"
            },
            "reqSeqNo": "111111",
            "riskSeqNo": "",
            "ruleId": 0,
            "ruleSet": "",
            "strategyId": 0,
            "userId": ""
        }
        with self.client.post("/console/api/data/loadByImpress",  headers=self.headers, json=payload, catch_response=True) as response:

            if response.status_code != 200 :
                # print(response)
                response.failure("请求失败！")
            else :
                json_data = response.json()["data"]
                if json_data["data"]["local_applist_genreid_game_action_90d_cnt"] and json_data["data"]["local_applist_loan_app_updated_720d_cnt"]:
                    print(json_data["data"]["local_applist_genreid_game_action_90d_cnt"] )
                    if json_data["data"]["local_applist_genreid_game_action_90d_cnt"]['val'] !=0 or json_data["data"]["local_applist_loan_app_updated_720d_cnt"]['val'] !=0:
                        response.failure("响应超时！")
                    response.success()
                else:
                    response.failure("没有响应！")

class RiskFeatureUser(HttpUser):
    wait_time = between(1, 2)
    tasks = [TestRiskFeature]
    host = "http://aiorisk-fat.sandbox-shuangqiang.top"