import uuid
import json
import urllib3
from curl_cffi import requests




# 注意 impersonate 这个参数
url = requests.get("https://claude.ai/api/organizations", impersonate="chrome110")

#  cookie   请修改你直接的cookie
headers = {
    'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://claude.ai/chats',
    'Content-Type': 'application/json',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Connection': 'keep-alive',
    'Cookie': f''
}
# 支持使用代理
proxies = {"https": "socks://127.0.0.1:10808"}
#response = requests("GET",url,headers=headers,proxies=proxies)
response = requests.get("https://claude.ai/api/organizations", impersonate="chrome110",headers=headers,proxies=proxies,timeout=500)
if response.status_code == 200:
    res = json.loads(response.text)
    uuid = res[0]['uuid']
    print(f"uuid: {uuid} ")
else:
    print(f"Error: {response.status_code} - {response.text}")