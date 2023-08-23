# Claude2 -pyAPI 
   主要功能，实现Claude2 创建会话、聊天、发送附件、获取历史会话，清理历史记录等功能




## 先决条件

　　要使用这个API,您需要有以下:
　　
　　Python安装在您的系统上

​           python =">=3.7"

 　　请求库安装

```bash
  pip install requests
  pip install python-dotenv

```

## 使用


在您的Python脚本导入claude_api模块:

    from claude_api import Client

* 接下来,你需要创建一个客户端类的实例通过提供你的Claude AI cookie:
* 你可以通过浏览器访问https://claude.ai/ 确保你能通过网页调用Claude2 访问。然后通过F12浏览器抓取cookies 值
* ![image-20230727113153074](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20230727113153074.png)



      cookie = os.environ.get('cookie')
      claude_api = Client(cookie)

##    使用2

   使用docker 方式启动

​       docker 编译打包镜像

```
docker build -t=wwwzhouhui/claude2-pyapi:0.0.2 .
```

​      docker 启动

```
docker run -d -p 5000:5000 -e "cookie=aaa" -e "uploads=/home/claude/uploads" -v /home/claude/uploads:/home/claude/uploads wwwzhouhui/claude2-pyapi:0.0.2
```

​    -p  启动容器内部端口5000，对外访问端口5000

​    -e  容器启动参数通过cookie 传递参数。

​    -v  读取文件附件临时文件，通过docker 挂卷方式。

​      启动后

![image-20230801135355477](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20230801135355477.png)

​      cmd 命令行查看容器启动

​      ![image-20230801135526791](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20230801135526791.png)

​    容器内部启动日志

![image-20230801135703958](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20230801135703958.png)

##  使用 replit 部署

<a href="https://replit.com/@wwwzhouhui/Claude2-PyAPI#replit.nix">
  <img alt="Run on Repl.it" src="https://repl.it/badge/github/valetzx/nodeunblockreplit" style="height: 40px; width: 190px;" />
</a>

https://replit.com/@wwwzhouhui/Claude2-PyAPI#replit.nix

##  列出所有的对话

列出所有会话Id与Claude ,你可以使用list_all_conversations方法:

    conversations = claude_api.list_all_conversations()
    for conversation in conversations:
        conversation_id = conversation['uuid']
        print(conversation_id)

## 发送消息

发送消息给 Claude, 您可以使用send_message方法。您需要提供提示和对话ID:



    prompt = "Hello, Claude!"
    conversation_id = "<conversation_id>" or claude_api.create_new_chat()['uuid']
    response = claude_api.send_message(prompt, conversation_id)
    print(response)

## 发送消息带附件

你可以发送任何类型的附件claude 得到响应中使用附件参数send_message ()

注意:claude 目前只支持某些文件类型

    prompt = "Hey,Summarize me this document.!"
    conversation_id = "<conversation_id>" or claude_api.create_new_chat()['uuid']
    response = claude_api.send_message(prompt, conversation_id,attachment="path/to/file.pdf")
    print(response)


## 删除对话

删除一个对话,你可以使用delete_conversation方法:


    conversation_id = "<conversation_id>"
    deleted = claude_api.delete_conversation(conversation_id)
    if deleted:
        print("Conversation deleted successfully")
    else:
        print("Failed to delete conversation")

## 聊天对话的历史

聊天对话记录,您可以使用chat_conversation_history方法:

    conversation_id = "<conversation_id>"
    history = claude_api.chat_conversation_history(conversation_id)
    print(history)

## 创建新的聊天

创建一个新的聊天对话(id),您可以使用create_new_chat方法:


    new_chat = claude_api.create_new_chat()
    conversation_id = new_chat['uuid']
    print(conversation_id)

## 重置所有对话

重置所有对话,您可以使用reset_all方法:


    reset = claude_api.reset_all()
    if reset:
        print("All conversations reset successfully")
    else:
        print("Failed to reset conversations")   

## 重命名聊天

   重命名一个聊天对话,你可以使用rename_chat方法:

    conversation_id = "<conversation_id>"
    title = "New Chat Title"
    renamed = claude_api.rename_chat(title, conversation_id)
    if renamed:
        print("Chat conversation renamed successfully")
    else:
        print("Failed to rename chat conversation")

​                                                                                          测试

​     启动claude_flask.py

1. 获取历史会话
   1. ![image-20230727113933463](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20230727113933463.png)

   postman 导入测试的请求接口json

  get 请求，获取当前会话历史记录 http://127.0.0.1:5000/chat/0c24bd45-ac55-4a24-8393-1582369f5abd

 其中0c24bd45-ac55-4a24-8393-1582369f5abd 是对话ID 

  请求参数 无:

  ![image-20230727114240619](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20230727114240619.png)


​    

​       点击 send postman 接口会调用 启动的flask 程序，调用成功后postman 接口会返回当天聊天会话历史记录

​      ![image-20230727114435649](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20230727114435649.png)

​      程序控制台会返回请求 GET /chat/0c24bd45-ac55-4a24-8393-1582369f5abd   返回200 

​     ![image-20230727114534664](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20230727114534664.png)

2. 创建新会话

   请求 方式 POST  请求url   http://127.0.0.1:5000/chat

   headhers 设置  Content-Type=  application/json

    ![image-20230727114755516](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20230727114755516.png)

​    body  请求参数， prompt 是固定值， 后面是您需要问的问题。

​     {

​       "prompt": "亚洲金融危机爆发时间是什么时候？请告诉我为什么会出现金融危机?" 

​    }

​    ![image-20230727114914418](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20230727114914418.png)

​    请求返回

   ![image-20230727115103581](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20230727115103581.png)

   我们刷新一下网页端，查看当前浏览器

  ![image-20230727115222342](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20230727115222342.png)

3 当前会话中发送消息

   请求 方式 POST  请求url   http://127.0.0.1:5000/send

   headhers 设置  Content-Type=  application/json

![image-20230727115403219](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20230727115403219.png)

​    body  请求参数， prompt 是固定值， 后面是您需要问的问题。conversation_id 当前聊天会话ID

​     {

​         "conversation_id": "0c24bd45-ac55-4a24-8393-1582369f5abd", 

​         "prompt": "中国和美国的科技有哪些差距？估计多少年才能缩小差距？!" 

​     }

​      请求返回

​      ![image-20230727115712187](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20230727115712187.png)

​     

​     我们刷新一下网页端，查看当前浏览器

​    ![image-20230727115852900](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20230727115852900.png)

4 文件上传功能

​    请求 方式 POST  请求url   http://127.0.0.1:5000/upload

   headhers 设置  Content-Type=  multipart/form-data

   ![image-20230801094048526](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20230801094048526.png)

 body  请求参数 使用form-data, form 表单1 参数file   类型选择 file   

![image-20230801094345113](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20230801094345113.png)

![image-20230801094413288](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20230801094413288.png)

 请求返回

![image-20230801094552650](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20230801094552650.png)



5  发送消息并附带附件

 请求 方式 POST  请求url   http://127.0.0.1:5000/sendattachment

   headhers 设置  Content-Type=  multipart/form-data

![image-20230801094751415](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20230801094751415.png)

 body  请求参数 使用form-data, form 表单三个参数 ，conversation_id，prompt，file 其中 前面2个 文件类型txt,最后一个文件类型选择file

![image-20230801094956606](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20230801094956606.png)

 请求返回

![image-20230801095053897](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20230801095053897.png)

刷新网页查看页面结果。

![image-20230801095236798](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20230801095236798.png)

 视频信息：https://foul-maxilla-075.notion.site/claude2-a81a9488e7e943f588f4fe80a0a2fce0



### 代理相关配置说明:

env 配置文件增加

```
HTTP_PROXY="http://127.0.0.1:10809"
HTTPS_PROXY="https://127.0.0.1:10809"
#SOCKS5_PROXY="socks5://127.0.0.1:10808"
ISPROXY=True
```

  如果启用代理模式访问，ISPROXY设置True.另外 配置HTTP_PROXY、HTTPS_PROXY 、SOCKS5_PROXY 代理。二者可选。如果不设置代理可以将ISPROXY 设置为空或者 ISPROXY=False  HTTP_PROXY、HTTPS_PROXY 、SOCKS5_PROXY 可以设置为空。

## *微信机器人功能:*

增加claude_wechatbot.py 实现微信机器人调用claude2创建聊天信息、发送聊天信息、获取历史聊天对话功能。

![Screenshot_20230813_213239_com.tencent.mm](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/Screenshot_20230813_213239_com.tencent.mm.jpg)

主要代码简单介绍

```
itchat.instance.receivingRetryCount = 600  # 修改断线超时时间
itchat.auto_login(enableCmdQR=2,hotReload=False,qrCallback=qrCallback)
user_id = itchat.instance.storageClass.userName
name = itchat.instance.storageClass.nickName
logger.info("Wechat login success, user_id: {}, nickname: {}".format(user_id, name))
#itchat.send('Hello, filehelper', toUserName='wwzhouhui')
# msg="天气预报"
# itchat.send('%s' % tuling(msg),toUserName='filehelper')
itchat.run()
```

 以上代码执行启动一个微信登陆监听画面，在系统控制台中会出现二维码。用微信扫描二维码，这样登陆访问的微信就具备机器人功能。

![image-20230813214437724](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20230813214437724.png)



```
# text_reply msg_files可以处理好友之间的聊天回复
@itchat.msg_register([TEXT,MAP,CARD,NOTE,SHARING])
def text_reply(msg):
    #itchat.send('%s' % get_chat_history(msg['Text']),msg['FromUserName'])
     itchat.send('%s' % send_message_judge(msg['Text']),msg['FromUserName'])
```

​     以上代码实现监听claude2 回复消息监听转发到微信中，通过微信机器人发送给问问题的人。

​    

```
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
```

​    调用claude2api接口实现消息的创建和消息的发送给claude2，输入提示词实现调用claude2获取回答问题消息。

###  *企业微信机器人功能:*

增加了ImApp.py 通过工厂方法构建IM 功能目前包含企业微信和微信功能目前测试通过了claude2创建聊天信息、发送聊天信息发生消息给企业微信。

![](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/%25E4%25BC%2581%25E4%25B8%259A%25E5%25BE%25AE%25E4%25BF%25A1%25E6%2588%25AA%25E5%259B%25BE_1692783572160.png)

   企业微信需要回调函数，所以程序运行需要有公网访问地址，最好需要固定IP

   ![image-20230823174713575](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20230823174713575.png)

详细测试可以看视频https://foul-maxilla-075.notion.site/claude2-3ed6c06da96249a1ad106d1ce987aa6c

###  版本:

- version 0.0.1: 基础功能包括创建会话、聊天、获取历史会话，清理历史记录等功能
- version 0.0.2:  修改文件读取功能，增加了文件上传功能和发送消息并附带附件功能；增加了项目演示视频信息。
- version 0.0.3：增加docker容器运行，运行cookie传参数使用，避免程序写死；增加replit 部署
- version 0.0.4：修改claude_api.py接口代码，考虑国内网络环境以及容器部署没办法访问claude，增加代理proxy访问方式
- version 0.0.5：修改claude_api.py接口代码对于send_message返回数据解析做了相应修改；增加微信创建聊天、发送聊天、获取历史聊天信息功能；
- version 0.0.6：修复We are unable to serve your request 问题，替换成curl_cffi 模拟浏览器模式，增加testcurl_cffi.py 测试代码
- version 0.0.7：新增加IM功能工厂代码，目前完成企业微信整合claude_api.py接口功能，后面重写微信功能


### 视频演示地址:

第一节 ：基础功能包括创建会话、聊天、获取历史会话

哔哩哔哩：https://www.bilibili.com/video/BV1Cz4y1x7BV/

YouTube：https://www.youtube.com/watch?v=e-ssvXw9Di8&t=49s

西瓜视频：https://www.ixigua.com/7260833345888584249?is_new_connect=0&is_new_user=0

第二节 ：文件上传功能和发送消息并附带附件功能，支持docker容器部署

哔哩哔哩：https://www.bilibili.com/video/BV1KN411h7Hm/

YouTube：https://www.youtube.com/watch?v=_uqHbZjoV14&t=40s

西瓜视频：https://www.ixigua.com/7262393347132621352

第三节 ：支持微信聊天功能，实现微信创建聊天、发送聊天、获取历史聊天信息功能

哔哩哔哩：https://www.bilibili.com/video/BV1f8411R7Aj

YouTube： https://www.youtube.com/watch?v=_l0yE2Kgm1g&t=40s

西瓜视频：https://www.ixigua.com/7266855523801268772

## 🎉 致谢

感谢以下项目对本项目提供的有力支持：

1. [Claude-API](https://github.com/KoushikNavuluri/Claude-API)

   提供claude2 网页端逆向接口

2. [chatgpt-on-wechat](https://github.com/zhayujie/chatgpt-on-wechat)

   提供微信、企业微信功能整合

## 问题反馈

如有问题，请在GitHub Issue中提交，在提交问题之前，请先查阅以往的issue是否能解决你的问题。

## 常见问题汇总

1. 请求无权限

   ![image-20230811130335065](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20230811130335065.png)

​     

此类问题是当前访问的地区和国家不能访问https://claude.ai 导致的。类似前端页面返回错误地址信息

可以检查自己IP 地址 使用这个网站https://ipleak.net/ 测试

![image-20230811132845703](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20230811132845703.png)

  

以上ip显示是荷兰不是英国和美国这样导致访问地址受限。

![image-20230811130718423](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20230811130718423.png)

![image-20230811131419471](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20230811131419471.png)

2. uuid 返回不了值

      代码claude_api.py get_organization_id 方法中出错

   ```
    response = self.send_request("GET",url,headers=headers)
           if response.status_code == 200:
               res = json.loads(response.text)
               uuid = res[0]['uuid']
               return uuid
           else:
               print(f"Error: {response.status_code} - {response.text}")
   ```

   ​    返回code 200  但是程序解析  uuid = res[0]['uuid']      返回报错。

      这是因为和问题1 类似权限问题导致网站重定向到错误页面 不能返回正确的 json 数字，代码在解析json代码不严谨返回解析报错。

      可以通过网页端访问https://claude.ai/api/organizations

      ![image-20230811131542303](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20230811131542303.png)

​      返回带有uuid的 json 返回值，说明网络情况是允许访问的。

3. 发任何消息回复： {"error": {"type": "permission_error", "message": "We are unable to serve your request"}} 

   在requirements.txt 增加urllib3和curl_cffi 2个依赖。修改了curl_cffi 模拟浏览器模式

   详细测试看这个视频https://foul-maxilla-075.notion.site/testcurl_cff-We-are-unable-to-serve-your-request-f5445d3f8dc040be8ee94a1a19ad923a
