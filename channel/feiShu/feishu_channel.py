# encoding:utf-8
import json
import hmac
import hashlib
import base64
import time
import requests
from urllib.parse import quote_plus
from common.log import logger
from flask import Flask, request, render_template, make_response
from config import conf
from bridge.bridge import Bridge
from channel.channel import Channel
from urllib import request as url_request
from concurrent.futures import ThreadPoolExecutor
class FeiShuChannel(Channel):
    def __init__(self):
        self.app_id = conf().get('feishu_app_id')
        self.app_secret = conf().get('feishu_app_secret')
        self.verification_token = conf().get('feishu_verification_token')
        self.host = conf().get('feishu_host')
        self.port = conf().get('feishu_port')
        logger.info("[feiShu] app_id={}, app_secret={} verification_token={} feishu_host={} feishu_port={} ".format(
            self.app_id, self.app_secret, self.verification_token,self.host, self.port))

    def startup(self):
        http_app.run(host=self.host, port=self.port)

    def get_tenant_access_token(self):
        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal/"
        headers = {
            "Content-Type": "application/json"
        }
        req_body = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }

        data = bytes(json.dumps(req_body), encoding='utf8')
        req = url_request.Request(url=url, data=data,
                                  headers=headers, method='POST')
        try:
            response = url_request.urlopen(req)
        except Exception as e:
            print(e.read().decode())
            return ""

        rsp_body = response.read().decode('utf-8')
        rsp_dict = json.loads(rsp_body)
        code = rsp_dict.get("code", -1)
        if code != 0:
            print("get tenant_access_token error, code =", code)
            return ""
        return rsp_dict.get("tenant_access_token", "")

    def notify_feishu(self, token, receive_type, receive_id, at_id, answer):
        # logger.info("notify_feishu.receive_type = {} receive_id={}",
        #          receive_type, receive_id)

        url = "https://open.feishu.cn/open-apis/im/v1/messages"
        params = {"receive_id_type": receive_type}

        # text = at_id and "<at user_id=\"%s\">%s</at>" % (
        #     at_id, answer.lstrip()) or answer.lstrip()
        text = answer.lstrip()
        #logger.info("notify_feishu.text = {}", text)
        msgContent = {
            "text": text,
        }
        req = {
            "receive_id": receive_id,  # chat id
            "msg_type": "text",
            "content": json.dumps(msgContent),
        }
        payload = json.dumps(req)
        headers = {
            # your access token
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json",
        }
        response = requests.request(
            "POST", url, params=params, headers=headers, data=payload
        )
        #logger.info("notify_feishu.response.content = {}", response.content)

    def handle(self, message):
        event = message["event"]
        msg = event["message"]
        messageId = msg["message_id"]
        chat_type = msg["chat_type"]
        sender_id = event["sender"]["sender_id"]["open_id"]

        prompt = json.loads(msg["content"])["text"]
        prompt = prompt.replace("@_user_1", "")

        #重复


        # 非文本不处理
        message_type = msg["message_type"]
        if message_type != "text":
            return {'ret': 200}
        if chat_type == "group":
            mentions = msg["mentions"]
            # 日常群沟通要@才生效
            if not mentions:
                return {'ret': 200}
            receive_type = "chat_id"
            receive_id = msg.get("chat_id")
            at_id = sender_id
        elif chat_type == "p2p":
            receive_type = "open_id"
            receive_id = sender_id
            at_id = None

        # 调用发消息 API 之前，先要获取 API 调用凭证：tenant_access_token
        access_token = self.get_tenant_access_token()
        if access_token == "":
            logger.error("send message access_token is empty")
            return {'ret': 204}

        context = dict()

        context['from_user_id'] = str(sender_id)
        reply = self.build_reply_content(prompt, context)
        #logger.info("handle.reply :", reply)
        # 机器人 echo 收到的消息
        self.notify_feishu(access_token, receive_type,
                            receive_id, at_id, reply)
        return {'ret': 200}

    def handle_request_url_verify(self, post_obj):

        # 原样返回 challenge 字段内容
        challenge = post_obj.get("challenge", "")
        logger.info("[handle_request_url_verify] challenge={}".format(challenge))
        return {'challenge': challenge}

    def build_reply_content(self, query, context=None):
        return Bridge().fetch_reply_content(query, context)


#feishu = FeiShuChannel()
thread_pool = ThreadPoolExecutor(max_workers=8)
http_app = Flask(__name__)


@http_app.route("/", methods=['POST'])
def chat():
    feishu = FeiShuChannel()
    # log.info("[feiShu] chat_headers={}".format(str(request.headers)))
    logger.info("[feiShu] chat={}".format(str(request.data)))
    obj = json.loads(request.data)
    # logger.info("[feiShu] type={}".format(obj.get("type", "")))
    # logger.info("[feiShu] token={}".format(obj.get("token", "")))
    # logger.info("[feiShu] challenge={}".format(obj.get("challenge", "")))
    if not obj:
        return {'ret': 201}
    # 校验 verification token 是否匹配，token 不匹配说明该回调并非来自开发平台
    headers = obj.get("header")
    if not headers:
        return {'ret': 201}
    # token = headers.get("token", "")
    # # logger.info("[feiShu] token={}".format(token))
    # # if token != feishu.verification_token:
    # #     logger.error("verification token not match, token = {}", token)
    # #     return {'ret': 201}

    # 根据 type 处理不同类型事件
    t = obj.get("type", "")
    if "url_verification" == t:  # 验证请求 URL 是否有效
        return feishu.handle_request_url_verify(obj)
    elif headers.get("event_type", None) == "im.message.receive_v1":  # 事件回调
        return feishu.handle(obj)
    return {'ret': 202}