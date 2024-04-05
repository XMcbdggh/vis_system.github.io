import numpy as np
import requests

#需要改用户代理 user_agent
# #GET请求
# res=requests.get('http://127.0.0.1:5000/user2/?name=echo',json={'name':'echo','age':15,'sex':'男'},
#                  headers={'Content-Type':'application/json',
#                           'Cookie':'key=echo123564654'})
# res=requests.get('http://127.0.0.1:8081/giveBarData/')
# print(res.text)

# # POST请求
# res=requests.post('http://127.0.0.1:8081/giveBarData/',json={'currentProvince': 'Nordland'})
# print(res.text)

# url = 'http://127.0.0.1:8081/giveBarData'  # Flask API的URL
# data = {'currentProvince': 'Nord-Trøndelag'}  # 替换为你想查询的省份名称
#
# response = requests.post(url, json=data)
#
# if response.status_code == 200:
#     print("Success:")
#     print(response.json())  # 打印返回的数据
# else:
#     print("Error:")
#     print(response.text)  # 错误时打印错误信息
