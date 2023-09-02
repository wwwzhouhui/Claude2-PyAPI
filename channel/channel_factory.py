"""
channel factory
"""

from channel.wechat.wechat_channel import WechatChannel
from channel.wechatcom.wechatenterprise_channel import WechatEnterpriseChannel
from channel.qqchat.qqchat_channel import QqchaChannel
from channel.dingtalk.dingtalk_channel import DingTalkChannel
from channel.feiShu.feishu_channel import FeiShuChannel

def create_channel(channel_type):
    """
    create a channel instance
    :param channel_type: channel type code
    :return: channel instance
    """
    if channel_type == 'wx':
        return WechatChannel()
    if channel_type == 'wxcom':
        return WechatEnterpriseChannel()
    if channel_type == 'qq':
        return QqchaChannel()
    if channel_type == 'dd':
        return DingTalkChannel()
    if channel_type == 'feishu':
        return FeiShuChannel()
    raise RuntimeError