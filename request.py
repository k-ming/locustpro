# import urllib.request
# import urllib.parse
# url = 'http://app-fat.sandbox-shuangqiang.top/loanapp/api/intent/checkRegisterUser'
# data = {"phone":9100000000}
# data_encode = urllib.parse.urlencode(data).encode("utf-8")
# req = urllib.request.Request(url, data=data_encode)
# req.add_header('Content-Type', 'application/json')
# req.add_header("versionCode",2)
# req.add_header("secret",0)
# with urllib.request.urlopen(req) as res:
#     print(res.read())
import json

import requests
url = 'http://app-fat.sandbox-shuangqiang.top/loanapp/api/intent/checkRegisterUser'
data = {"phone":9100000000}
headers = {'content-type': 'application/json', "versionCode":"2", "secret":"0"}
json_data = json.dumps(data)
response = requests.post(url, data=json_data, headers=headers)
print(response.json())