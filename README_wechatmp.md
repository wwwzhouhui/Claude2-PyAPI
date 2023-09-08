# Claude2 -pyAPI -dingding
   主要介绍Claude2api微信公众号相关配置和说明

## 微信公众号相关设置-创建应用

1. 登陆微信公众平台

   https://mp.weixin.qq.com/

2. 设置与开发-基础配置

   ![image-20230909004753199](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20230909004753199.png)

   点击服务器配置，设置URL 和 Token 和  EncodingAESKey 等相关配置
   
   因为公众号相当于开发的程序服务器在公网的服务器上面（和之前企业微信、飞书、钉钉都很类似）必须要有公网访问的IP服务。
   
   其中 url  填写：公网IP+wx   （因为微信默认是80和443端口启用）所以RUL  http://54.153.123.45/wx
   
   Token  可以根据自己需要填写
   
   EncodingAESKey 可以随机生成。
   
   ![image-20230909005315666](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20230909005315666.png)
   
   以上配置完按照上面点击完成。
   
   3 回调服务程序
   
      我们需要编写一段代码部署到服务器上，以便服务器回调这个接口从而确保微信公众号可以访问这个服务。具体代码如下
   
      testwx.py
   
    	
   
   ```python
   import hashlib
   import web
   from handle import Handle
   
   urls = (
       '/wx', 'Handle',
   )
   if __name__ == '__main__':
       app = web.application(urls, globals())
       app.run()
   ```
   
    handle.py
   
    
   
   ```python
   import hashlib
   import web
   
   class Handle(object):
       def GET(self):
           try:
               data = web.input()
               if len(data) == 0:
                   return "hello, this is handle view"
               signature = data.signature
               timestamp = data.timestamp
               nonce = data.nonce
               echostr = data.echostr
               token = "XXXX" #请按照公众平台官网\基本配置中信息填写
               list = [token, timestamp, nonce]
               list.sort()
               sha1 = hashlib.sha1()
               sha1.update(list[0].encode("utf-8"))
               sha1.update(list[1].encode("utf-8"))
               sha1.update(list[2].encode("utf-8"))
               hashcode = sha1.hexdigest() #获取加密串
               print ("handle/GET func: hashcode, signature: ", hashcode, signature)
               if hashcode == signature:
                   return echostr
               else:
                   return ""
           except Exception as Argument:
               return Argument
   ```
   
   4. 测试回调程序
   
      将以上2个PY 程序部署服务器上。
   
      启动程序 python3    testwx.py
   
      ```shell
      python3 testwx.py 80
      
      ```
   
      ![image-20230909005909154](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20230909005909154.png)

​    

​              测试程序启动完成。（这里需要注意服务器防火墙需要开启80端口访问）

​              ![image-20230909010013227](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20230909010013227.png)

​              点击提交

​               ![image-20230909010038177](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20230909010038177.png)

​    ![image-20230909010112654](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20230909010112654.png)

​       服务端返回200 验证成功。

5. 前启动ImApp.py

   ```shell
   python3 ImApp.py
   ```

    ![image-20230909010316404](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20230909010316404.png)

​         程序启动完成后，程序监听微信公众号了。

​    6   验证及测试

​          微信搜索到公众号，打开公众号聊天窗口

​           ![image-20230909010516032](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20230909010516032.png)

​           输入提示词“喜洋洋和灰太狼的故事“ 输入后，后端程序持续监听发送。因为微信公众号对返回要求较高 3秒钟没有相应会中断，所以我们设置超时重复机制+缓存模式。

​           ![image-20230909010759291](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20230909010759291.png)

​          程序微信超时3次，前段微信公众号返回”已开始处理，请稍等片刻后输入"继续"查看回复“   点击继续，这样微信公众号就会持续保持连接等待返回。

![image-20230909011003635](https://mypicture-1258720957.cos.ap-nanjing.myqcloud.com/Obsidian/image-20230909011003635.png)

