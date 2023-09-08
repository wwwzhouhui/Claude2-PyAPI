from config import conf
import config

config.load_config()
bot_token=conf().get('telegram').get('bot_token')
print(bot_token)
