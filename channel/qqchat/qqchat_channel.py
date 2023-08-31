from aiocqhttp import CQHttp, Event, MessageSegment

from channel.channel import Channel
from common.log import logger
from config import conf
from bridge.bridge import Bridge
from concurrent.futures import ThreadPoolExecutor
bot = CQHttp()
thread_pool = ThreadPoolExecutor(max_workers=8)


@bot.on_message('private')
async def _(event: Event):
    # context = dict()
    # logger.info(event.message)
    # await bot.send(event, QqchaChannel.build_reply_content(event.message,event.message, context))
    # return {'reply': event.message}
    logger.info("event: {}", event)
    QqchaChannel().handle(event)

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
        thread_pool.submit(self._do_handle, msg)
    def _do_handle(self, msg):
        context = dict()
        #logger.info("msg:", msg.message)
        #context['from_user_id'] = msg.user_id
        reply_text = self.build_reply_content(msg.message, context)
        bot.sync.send_private_msg(user_id=msg.user_id, message=reply_text)

    def send(self, msg, receiver):
        logger.info('[QQ] sendMsg={}, receiver={}'.format(msg, receiver))
        bot.send(receiver, msg)

    def build_reply_content(self, query, context=None):
        return Bridge().fetch_reply_content(query, context)

