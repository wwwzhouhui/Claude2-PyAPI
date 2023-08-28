from aiocqhttp import CQHttp, Event, MessageSegment

from channel.channel import Channel
from common.log import logger
from config import conf
from bridge.bridge import Bridge
bot = CQHttp()


@bot.on_message('private')
async def _(event: Event):
    context = dict()
    logger.info(event.message)
    await bot.send(event, QqchaChannel.build_reply_content(event.message,event.message, context))
    return {'reply': event.message}

@bot.on_startup
async def startup():
    logger.info("启动完毕，接收消息中……")



class QqchaChannel(Channel):
    def __init__(self):
        self.host = conf().get('reverse_ws_host')
        self.port = conf().get('reverse_ws_port')

    def startup(self):
        # startup()
        # bot.on_startup(startup)
        # logger.info("startup启动完毕，接收消息中……")
        bot.run(host=self.host, port=self.port)

    def handle(self, msg):
        logger.info("handle"+msg)

    def send(self, msg, receiver):
        logger.info('[QQ] sendMsg={}, receiver={}'.format(msg, receiver))
        bot.send(receiver, msg)

    def build_reply_content(self, query, context=None):
        return Bridge().fetch_reply_content(query, context)

