#coding=utf8
import requests
import json
import threading
import io
from lib import itchat
from lib.itchat.content import *
from common.log import logger
from common.utils import *
from claude_api import Client
# tuling plugin can be get here:
# https://github.com/littlecodersh/EasierLife/tree/master/Plugins/Tuling
#from tuling import get_response
# 调用图灵机器人的api，采用爬虫的原理，根据聊天消息返回回复内容
apiurl="http://127.0.0.1:5000"



#  获取cluade2 聊天消息
def get_chat(conversation_id):
    url = apiurl+"/chat/"+conversation_id
    payload = ""
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    print(response.text)
    data = json.loads(response.text)
    answer = data['text']
    return answer

#  发送消息给cluade2
def sendMessage(conversation_id,msg):
    url = apiurl+"/send"
    payload = json.dumps({
        "conversation_id": conversation_id,
        "prompt": msg
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    data = json.loads(response.text)
    answer = data['text']
    return answer
#  创建会话并实现消息发送
def createMessage(msg):
    url = apiurl+"/chat"
    payload = json.dumps({
        "prompt": msg
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    data = json.loads(response.text)
    answer = data['text']
    return answer

#  发送消息给cluade2并带有附件信息
def sendattachment(msg):
    url = apiurl+"/sendattachment"
    payload={}
    files=[
        ('file',('多模态.txt',open('/D:/工作临时/2023/2023-8/2023年8月3日/多模态.txt','rb'),'text/plain'))
    ]
    headers = {
        'Content-Type': 'multipart/form-data'
    }
    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    print(response.text)
    data = json.loads(response.text)
    answer = data['text']
    return answer

#   获取历史聊天信息
def get_chat_history(msg):
    cookie = get_cookie()
    isproxy= get_proxy()
    client = Client(cookie,isproxy)
    conversation_id="d7dbfdc0-7109-4495-88ec-d4802ae3870b"
    data = client.chat_conversation_history(conversation_id)
    logger.info("get_chat_history {} data"+str(data))
    answer = data['chat_messages']
    texts = []
    for message in answer:
        texts.append(message['text'])
    logger.info("get_chat_history {} answer".format(texts))
    return texts

# 创建新的对话聊天信息
def create_chat(msg):
    data = {'prompt': msg}
    prompt = data['prompt']

    cookie = get_cookie()
    isproxy= get_proxy()
    client = Client(cookie,isproxy)
    conversation = client.create_new_chat()
    conversation_id = conversation['uuid']
    response = client.send_message(prompt, conversation_id)
    logger.info("create_chat {} "+str(response))
    answer = response
    logger.info("create_chat {} answer".format(answer))
    resultdata = {'uuid': conversation_id,'answer':answer}
    return resultdata
# 发送消息
def send_message(msg,conversation_id):
    data = {'prompt': msg}
    prompt = data['prompt']
    cookie = get_cookie()
    isproxy= get_proxy()
    client = Client(cookie,isproxy)
    response = client.send_message(prompt, conversation_id)
    logger.info("send_message {} "+str(response))
    answer = response
    logger.info("send_message {} answer".format(answer))
    return answer


Conversation_id = ""
# 发送消息判断 如果是有Conversation_id 有值说明已经创建过群聊，直接发送消息，如果没有消息创建消息
def send_message_judge(msg):
    global Conversation_id
    if Conversation_id != "":
        return send_message(msg,Conversation_id)
    else:
        result= create_chat(msg)
        Conversation_id = result['uuid']
        return result['answer']

# 获取群聊信息
def get_group_info():
    cookie = get_cookie()
# 对于群聊信息，定义获取想要针对某个群进行机器人回复的群ID函数
def group_id(name):
    df = itchat.search_chatrooms(name=name)
    return df[0]['UserName']

# 注册文本消息，绑定到text_reply处理函数
# text_reply msg_files可以处理好友之间的聊天回复
@itchat.msg_register([TEXT,MAP,CARD,NOTE,SHARING])
def text_reply(msg):
    #itchat.send('%s' % get_chat_history(msg['Text']),msg['FromUserName'])
     itchat.send('%s' % send_message_judge(msg['Text']),msg['FromUserName'])

@itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
def download_files(msg):
    msg['Text'](msg['FileName'])
    return '@%s@%s' % ({'Picture': 'img', 'Video': 'vid'}.get(msg['Type'], 'fil'), msg['FileName'])

# 现在微信加了好多群，并不想对所有的群都进行设置微信机器人，只针对想要设置的群进行微信机器人，可进行如下设置
@itchat.msg_register(TEXT, isGroupChat=True)
def group_text_reply(msg):
    # 当然如果只想针对@你的人才回复，可以设置if msg['isAt']:
    item = group_id(u'想要设置的群的名称')  # 根据自己的需求设置
    if msg['ToUserName'] == item:
        itchat.send(u'%s' % send_message_judge(msg['Text']), item)

# 可用的二维码生成接口
# https://api.qrserver.com/v1/create-qr-code/?size=400×400&data=https://www.abc.com
# https://api.isoyu.com/qr/?m=1&e=L&p=20&url=https://www.abc.com
def qrCallback(uuid, status, qrcode):
    # logger.debug("qrCallback: {} {}".format(uuid,status))
    if status == "0":
        try:
            from PIL import Image

            img = Image.open(io.BytesIO(qrcode))
            _thread = threading.Thread(target=img.show, args=("QRCode",))
            _thread.setDaemon(True)
            _thread.start()
        except Exception as e:
            pass

        import qrcode

        url = f"https://login.weixin.qq.com/l/{uuid}"

        qr_api1 = "https://api.isoyu.com/qr/?m=1&e=L&p=20&url={}".format(url)
        qr_api2 = "https://api.qrserver.com/v1/create-qr-code/?size=400×400&data={}".format(url)
        qr_api3 = "https://api.pwmqr.com/qrcode/create/?url={}".format(url)
        qr_api4 = "https://my.tv.sohu.com/user/a/wvideo/getQRCode.do?text={}".format(url)
        print("You can also scan QRCode in any website below:")
        print(qr_api3)
        print(qr_api4)
        print(qr_api2)
        print(qr_api1)

        qr = qrcode.QRCode(border=1)
        qr.add_data(url)
        qr.make(fit=True)
        qr.print_ascii(invert=True)

itchat.instance.receivingRetryCount = 600  # 修改断线超时时间
itchat.auto_login(enableCmdQR=2,hotReload=False,qrCallback=qrCallback)
user_id = itchat.instance.storageClass.userName
name = itchat.instance.storageClass.nickName
logger.info("Wechat login success, user_id: {}, nickname: {}".format(user_id, name))
#itchat.send('Hello, filehelper', toUserName='wwzhouhui')
# msg="天气预报"
# itchat.send('%s' % tuling(msg),toUserName='filehelper')
itchat.run()