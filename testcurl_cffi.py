import uuid
import json
from curl_cffi import requests




# 注意 impersonate 这个参数
url = requests.get("https://claude.ai/api/organizations", impersonate="chrome110")

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
    'Cookie': f'intercom-device-id-lupk8zyo=08a1e314-e71e-4000-a22c-65a021d19fa3; sessionKey=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; cf_clearance=.CbWh9M7ld0qg8APj4uAchCEETarQcFd3jXWy1uo5gA-1692235544-0-1-cfe27045.3372f732.98e32fa5-0.2.1692235544; intercom-session-lupk8zyo=aUMyS2ZkYjNsZ1F3N2NkYjIxSVRrVGlFRWxNelZTSnloc3U0eDY4eEJ3VWpLeWg0ekt2YlovNjVsVEJldUgvLy0tT3VCQ3M3SU81aDFTa1ZDNWZ5ZlEzZz09--290673ec821a3a75c4bd1f6c01aa980861a81cf0; __cf_bm=BLGC281SbIt0xBzCUmKdYl32e_TYCLcfemWcW92CSD8-1692237908-0-AYFC2rlCQC5DVRmIwcGup1ugEkNMJufLCGctPbPWtDU6oXN6U9X7jZf3L/cJeNsKo5cIIlGQFmNBy1eXjhRP2oI='
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