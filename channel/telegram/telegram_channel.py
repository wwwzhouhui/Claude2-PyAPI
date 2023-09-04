from concurrent.futures import ThreadPoolExecutor
import io
import requests
import telebot
from common.log import logger
from channel.channel import Channel
from config import conf
bot = telebot.TeleBot(token=conf().get('telegram').get('bot_token'))
thread_pool = ThreadPoolExecutor(max_workers=8)

@bot.message_handler(commands=['help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "<a>我是claude2机器人，开始和我聊天吧!</a>", parse_mode = "HTML")

# 处理文本类型消息
@bot.message_handler(content_types=['text'])
def send_welcome(msg):
    # telegram消息处理
    TelegramChannel().handle(msg)

class TelegramChannel(Channel):
    def __init__(self):
        pass

    def startup(self):
        logger.info("开始启动[telegram]机器人")
        bot.infinity_polling()

    def handle(self, msg):
        logger.debug("[Telegram] receive msg: " + msg.text)
        thread_pool.submit(self._dosend,msg.text,msg)

    def _dosend(self,query,msg):
        context= dict()
        context['from_user_id'] = str(msg.chat.id)
        reply_text = super().build_reply_content(query, context)
        logger.info('[Telegram] reply content: {}'.format(reply_text))
        bot.reply_to(msg,reply_text)


