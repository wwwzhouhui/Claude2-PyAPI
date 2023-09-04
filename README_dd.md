# Claude2 -pyAPI -dingding
   主要介绍Claude2api整合钉钉相关配置和说明

## 钉钉相关设置-创建应用

1. 登陆钉钉开放平台

   https://open-dev.dingtalk.com/

2. 应用开发-机器人

   选择应用开发-点击机器人创建一个机器人

   ![image-20230904144420569](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20230904144420569.png)

​     点击创建应用，在弹出的创建应用对话框输入 H5微应用

​     ![image-20230904144635034](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20230904144635034.png)

​      创建完成后 机器人如下：

   ![image-20230904144706442](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20230904144706442.png)

​    点击应用会出现详细页面，这里面我们需要记住应用凭证（AgentId、AppKey、AppSecret）

​    ![image-20230904144811915](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20230904144811915.png)

## 钉钉相关设置-开发管理

这里我们需要设置钉钉调用发布程序的公网网络。设置服务器出口IP  应用地址

![image-20230904145103533](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20230904145103533.png)



 如图配置好公网访问IP 、应用点击保存按钮

##      钉钉相关设置-程序应用发布

点击版本管理与发布，完成程序应用上架。

![image-20230904145349514](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20230904145349514.png)

##            钉钉相关设置-添加机器人

企业成员使用路径：进入要使用机器人的群 >【群设置】>【智能群助手】>【添加机器人】，在企业机器人列表中即可找到

![image-20230904153240807](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20230904153240807.png)

![image-20230904153308489](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20230904153308489.png)

![image-20230904153331847](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20230904153331847.png)

![image-20230904153450694](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20230904153450694.png)

![image-20230904153539852](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20230904153539852.png)

​    创建完成后记录下access_token   值 

https://oapi.dingtalk.com/robot/send?access_token=xxxx

##  程序相关配置

 1config.json  配置文件修改

   ![image-20230904153932166](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20230904153932166.png)

程序中config.json 对应的dingtalk_key、dingtalk_secret、dingtalk_token、dingtalk_post_token、dingtalk_host、dingtalk_port 按照上面创建钉钉应用配置修改相应的值。

## 程序测试

1.修改ImApp.py

```python
import config
from common.log import logger
from channel import channel_factory
def run():
    try:
        # load config
        config.load_config()

        # create channel
        channel = channel_factory.create_channel("dd")

        # startup channel
        channel.startup()
    except Exception as e:
        logger.error("App startup failed!")
        logger.exception(e)


if __name__ == "__main__":
    run()
```

 channel = channel_factory.create_channel("dd")  修改成dd  创建钉钉频道

2.启动程序

```
nohup python3 ImApp.py & tail -f nohup.out
```

​    ![image-20230904154303807](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20230904154303807.png)

​    服务器启动程序

3. IM聊天测试

   找到 钉小蜜机器人（机器人名字你根据自己习惯起），输入聊天消息

   ![image-20230904154842354](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20230904154842354.png)

   服务器控制台返回的信息

   ![image-20230904154944497](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20230904154944497.png)
