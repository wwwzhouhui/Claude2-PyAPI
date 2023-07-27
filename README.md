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

## 列出所有的对话

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

### 版本:

- version 0.0.1: 基础功能包括创建会话、聊天、获取历史会话，清理历史记录等功能

## 🎉 致谢

感谢 @KoushikNavuluri  对本项目的支持。

## 问题反馈

如有问题，请在GitHub Issue中提交，在提交问题之前，请先查阅以往的issue是否能解决你的问题。
