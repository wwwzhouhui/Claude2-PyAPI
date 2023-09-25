from curl_cffi import requests,Curl, CurlOpt
from io import BytesIO
import json
import re


def send_message():
    url = "https://claude.ai/api/append_message"
    #print("send_message,attachment"+attachment)
    # Upload attachment if provided
    attachments = []
    # 提示词你的问题
    prompt="中美之间的冲突有哪些？"
    # 对应增加的organization_id 可以通过testcurl_cffi.py运行后获取
    organization_id="28912dc3-bcd3-43c5-944c-a943a02d19fc"
    #  当前对话输出对话ID https://claude.ai/chat/59a35107-753a-489b-98c6-e289604f9d97 对应这段url 后面一串代码
    conversation_id="59a35107-753a-489b-98c6-e289604f9d97"
    #  cookie 对应claude2 网页端抓取的F12获得的 cookie
    cookie="请换成你的cookies"
    #  代理地址（主要是方便本地测试 我用的是v2rayN代理访问的，测试的时候使用socks 代理，你也可以换成https代理
    proxies = "socks://127.0.0.1:10808"
    payload = json.dumps({
        "completion": {
            "prompt": f"{prompt}",
            "timezone": "Asia/Kolkata",
            "model": "claude-2"
        },
        "organization_uuid": f"{organization_id}",
        "conversation_uuid": f"{conversation_id}",
        "text": f"{prompt}",
        "attachments": attachments
    })

    headers = [b'User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0',
               b'Accept: text/event-stream, text/event-stream',
               b'Accept-Language: en-US,en;q=0.5',
               b'Referer: https://claude.ai/chats',
               b'Content-Type: application/json',
               b'Origin: https://claude.ai',
               b'DNT: 1',
               b'Connection: keep-alive',
               b'Cookie: %b'%cookie.encode('utf-8'),
               b'Sec-Fetch-Dest: empty',
               b'Sec-Fetch-Mode: cors',
               b'Sec-Fetch-Site: same-origin',
               b'TE: trailers']



    buffer = BytesIO()
    c = Curl()
    def stream_callback(data):
        json_str = data.decode('utf-8')

        decoded_data = re.sub('\n+', '\n', json_str).strip()
        data_strings = decoded_data.split('\n')
        for data_string in data_strings:
            json_str = data_string[6:].strip()
            _data = json.loads(json_str)
            if 'completion' in _data:
                buffer.write(str(_data['completion']).encode('utf-8'))
                print(_data['completion'], end="")

    c.setopt(CurlOpt.URL, b'https://claude.ai/api/append_message')
    c.setopt(CurlOpt.WRITEFUNCTION, stream_callback)
    c.setopt(CurlOpt.HTTPHEADER, headers)
    c.setopt(CurlOpt.POSTFIELDS, payload)
    c.setopt(CurlOpt.PROXY, proxies.encode())
    c.impersonate("chrome110")

    c.perform()
    c.close()
    body = buffer.getvalue()
    print(body.decode())

send_message()