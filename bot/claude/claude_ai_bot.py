# encoding:utf-8

import requests
from bot.bot import Bot
from config import conf
from claude_api import Client
from common.log import logger
from bot.claude.idStore import idStore

class ClaudeAiBot(Bot):


    def reply(self, query, context=None):
        storage = idStore()
        Conversation_id=storage.get_id()
        if Conversation_id is not None:
            return self.send_message(query,Conversation_id)
        else:
            result= self.create_chat(query,Conversation_id)
            storage.set_id(result['uuid'])
            return result['answer']
        # 创建新的对话聊天信息
    def create_chat(self,msg,conversation_id):
        data = {'prompt': msg}
        prompt = data['prompt']
        self.cookie = conf().get('cookie')
        self.isproxy= conf().get('isproxy')
        #logger.info("create_chat: cookie: {}".format(self.cookie))
        #logger.info("create_chat: isproxy: {}".format(self.isproxy))
        client = Client(self.cookie,self.isproxy)
        conversation = client.create_new_chat()
        conversation_id = conversation['uuid']
        response = client.send_message(prompt, conversation_id)
        logger.info("create_chat {} "+str(response))
        answer = response
        logger.info("create_chat {} answer".format(answer))
        resultdata = {'uuid': conversation_id,'answer':answer}
        return resultdata
    # 发送消息
    def send_message(self,msg,conversation_id):
        data = {'prompt': msg}
        prompt = data['prompt']
        self.cookie = conf().get('cookie')
        self.isproxy= conf().get('isproxy')
        client = Client(self.cookie,self.isproxy)
        response = client.send_message(prompt, conversation_id)
        logger.info("send_message {} "+str(response))
        answer = response
        logger.info("send_message {} answer".format(answer))
        return answer

