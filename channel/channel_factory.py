"""
channel factory
"""

from channel.wechat.wechat_channel import WechatChannel
from channel.wechatcom.wechatenterprise_channel import WechatEnterpriseChannel

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
    raise RuntimeError