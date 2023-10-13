# SaaS 平台 Python 应用部署实战

如果你还不知道，
现在各大云服务巨头都提供了
**永久免费** 的 Serverless 服务，
适合托管一些很小的应用。

想把去年写的一个 Telegram 超轻量 bot
部署到 Azure Functions 上，
结果被微软念经一样的文档气得不轻，
遂决定写一篇 walkthrough 记录下。

本教程所使用的代码放在
[KumaTea/KumaLiteBot](https://github.com/KumaTea/KumaLiteBot)
这个 repo 里。

目前示例 bot [Kuma 发癫 Bot](https://t.me/KumaLiteBot)
托管在 Azure 上面。

## Google Cloud Functions

谷歌的配置过程是最直观、方便、省心的，
其实这个bot之前就托管在谷歌云上，
但是因为有隐形收费就关掉了。
只能说贵有贵的道理。

### 创建 Functions

先进入 Functions 界面

![](img/GCP-01-create-01.jpg)

点蓝色的创建

基础信息，喜欢的名字就好

![](img/GCP-01-create-02.jpg)

Region 这里，一般根据最多人访问的地区来选

因为我是 Telegram Bot,
选择 API 所在地荷兰阿姆斯特丹

![](img/GCP-01-create-03.jpg)

Trigger 这里 Auth 选择允许未认证调用

你也不想每次打开都要输密码吧

![](img/GCP-01-create-04.jpg)

下面配置按需求选，
我的 bot 用不到默认的 256 MB 就选了最小的

环境变量记得
[在 **SECURITY AND IMAGE REPO** 设置](#其他设置)

![](img/GCP-01-create-05.jpg)

如果弹出启用 API 允许即可

### 录入代码

选择语言和版本

![](img/GCP-02-code-01.jpg)

右边编辑器可以粘贴自己的代码了。

![](img/GCP-02-code-02.jpg)

注意，
**Entry point** 这里要写的是你程序的入口，
一般是 `main`

主函数示例：

```python
@functions_framework.http
def main(request):
    res = ''
    try:
        if not request.method == "POST":
            return 'I am working!'
        update = Update.de_json(request.get_json(force=True), bot)
        if update.inline_query:
            res = inline(request)
        elif update.message:
            msg = update.message
            if msg.chat.id > 0:
                res = msg.reply_text(nonsense_reply())
        else:
            logger.info('Unknown type. Ignoring...')
    except Exception as e:
        logger.debug(str(request.get_json(force=True)))
        logger.error(str(e))
    return res if type(res) is str else ''
```

`request` 就是一个标准的 `flask.request` 对象，
非常友好，与楼下高下立判

然后点击左侧 `requirements.txt`

![](img/GCP-02-code-03.jpg)

把依赖贴进去，就可以点下面的 **Deploy** 了

### 其他设置

可以看到这里我失败了，因为忘了设置环境变量

![](img/GCP-03-settings-01.jpg)

我需要的变量是认证的 `BOT_TOKEN`,
`**安全地** 设置这个变量会很麻烦，介绍如下

点击上方 Edit

![](img/GCP-03-settings-02.jpg)

进入 SECURITY AND IMAGE REPO

点击 ADD A SECRET REFERENCE

![](img/GCP-03-settings-03.jpg)

这个时候会发现创建是灰的

就需要先启用这个什么 Secret API

点击左边 ENTER SECRET MANUALLY 就会弹出带你去的窗口

![](img/GCP-03-settings-04.jpg)

启用后回来刷新重新进入修改，就能看到可以创建了，右边会弹出窗口

![](img/GCP-03-settings-05.jpg)

Name 随便写，下面的 value 填你的 token

然后 CREATE SECRET

![](img/GCP-03-settings-06.jpg)

Reference method 选中暴露为环境变量

下面环境变量输入你需要的，比如 `BOT_TOKEN`

至于上面提示没有权限，实测没有影响

---

这是安全的方法，那么有没有不安全的呢？

当然有

~~首先 Cloud Functions v1 就没有这么多幺蛾子~~

![](img/GCP-03-settings-07.jpg)

只要在创建或者修改里面
**RUNTIME** 下面 environment variables 里面填就好了

当然你也可以直接写进代码里

### 完成

OK, 这就完了

GCP 会自动开始 build 并部署

![](img/GCP-04-done-01.jpg)

可以看见已经成功运行

![](img/GCP-04-done-02.jpg)

#### 小提示

Cloud Functions 有免费额度，
**但 Storage 没有**。

![](img/GCP-04-done-03.jpg)

部署完成后可以直接删掉避免扣钱，
完全不影响 bot 运行


## AWS Lambda

AWS Lambda 比 GCP Cloud Functions
多一步手动上传依赖的步骤

### 创建 Lambda

在开始之前，记得先在右上角选择你想要的地区

![](img/AWS-01-create-01.jpg)

AWS 和别人不一样，它是先选地区，在这里创建的所有资源都会在这里

![](img/AWS-01-create-02.jpg)

右上角黄色按钮创建

![](img/AWS-01-create-03.jpg)

名字，语言和版本，架构

![](img/AWS-01-create-04.jpg)

下方高级设置，要勾上 Enable Function URL,
这样才能从 URL 访问；

Auth type 选 None

![](img/AWS-01-create-05.jpg)

### 填入代码

向下拉，把代码粘贴进编辑器，保存即可

![](img/AWS-02-code-01.jpg)


主函数示例：

```python
def lambda_handler(event, context):
    res = {
        'statusCode': 200,
        'body': ''
    }
    method = event['requestContext']['http']['method']
    try:
        if not method == "POST":
            res['body'] = 'I am working!'
            return res
        update = Update.de_json(json.loads(event['body']), bot)
        if update.inline_query:
            res['body'] = str(inline(update))
        elif update.message:
            msg = update.message
            if msg.chat.id > 0:
                res['body'] = str(msg.reply_text(nonsense_reply()))
        else:
            logger.info('Unknown type. Ignoring...')
    except Exception as e:
        logger.error(str(event))
        logger.error(str(e))
    return res
```

`event` 示例

<span style="font-size: 0.5em">

> * GET: `{'version': '2.0', 'routeKey': '$default', 'rawPath': '/', 'rawQueryString': 'key=value', 'headers': {'sec-fetch-mode': 'navigate', 'x-amzn-tls-version': 'TLSv1.2', 'sec-fetch-site': 'none', 'accept-language': 'en-US,en;q=0.9', 'x-forwarded-proto': 'https', 'x-forwarded-port': '443', 'x-forwarded-for': '103.172.80.149', 'sec-fetch-user': '?1', 'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7', 'x-amzn-tls-cipher-suite': 'ECDHE-RSA-AES128-GCM-SHA256', 'sec-ch-ua': '"Google Chrome";v="117", "Not;A=Brand";v="8", "Chromium";v="117"', 'sec-ch-ua-mobile': '?0', 'x-amzn-trace-id': 'Root=1-65284b56-7a462eea204cb5a45d3c0668', 'sec-ch-ua-platform': '"Windows"', 'host': '7o22cfijy5jiujzbih6aov5yvy0hasni.lambda-url.eu-central-1.on.aws', 'upgrade-insecure-requests': '1', 'accept-encoding': 'gzip, deflate, br', 'sec-fetch-dest': 'document', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'}, 'queryStringParameters': {'key': 'value'}, 'requestContext': {'accountId': 'anonymous', 'apiId': '7o22cfijy5jiujzbih6aov5yvy0hasni', 'domainName': '7o22cfijy5jiujzbih6aov5yvy0hasni.lambda-url.eu-central-1.on.aws', 'domainPrefix': '7o22cfijy5jiujzbih6aov5yvy0hasni', 'http': {'method': 'GET', 'path': '/', 'protocol': 'HTTP/1.1', 'sourceIp': '103.172.80.149', 'userAgent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'}, 'requestId': '90551f3b-4891-4b37-9aeb-71e2fae50ad1', 'routeKey': '$default', 'stage': '$default', 'time': '12/Oct/2023:19:39:02 +0000', 'timeEpoch': 1697139542555}, 'isBase64Encoded': False}`
> 
> * POST: `{'version': '2.0', 'routeKey': '$default', 'rawPath': '/', 'rawQueryString': '', 'headers': {'content-length': '372', 'x-amzn-tls-cipher-suite': 'ECDHE-RSA-AES128-GCM-SHA256', 'x-amzn-tls-version': 'TLSv1.2', 'x-amzn-trace-id': 'Root=1-65284b9f-3fff13e27bc794f95e3dbc98', 'x-forwarded-proto': 'https', 'host': '7o22cfijy5jiujzbih6aov5yvy0hasni.lambda-url.eu-central-1.on.aws', 'x-forwarded-port': '443', 'content-type': 'application/json', 'x-forwarded-for': '91.108.6.19', 'accept-encoding': 'gzip, deflate'}, 'requestContext': {'accountId': 'anonymous', 'apiId': '7o22cfijy5jiujzbih6aov5yvy0hasni', 'domainName': '7o22cfijy5jiujzbih6aov5yvy0hasni.lambda-url.eu-central-1.on.aws', 'domainPrefix': '7o22cfijy5jiujzbih6aov5yvy0hasni', 'http': {'method': 'POST', 'path': '/', 'protocol': 'HTTP/1.1', 'sourceIp': '91.108.6.19', 'userAgent': None}, 'requestId': '9fc841ed-6d28-461e-a657-565813752326', 'routeKey': '$default', 'stage': '$default', 'time': '12/Oct/2023:19:40:15 +0000', 'timeEpoch': 1697139615123}, 'body': '{"update_id":11992905,\n"message":{"message_id":20,"from":{"id":5273618487,"is_bot":false,"first_name":"Kuma","last_name":"Tea","username":"realKumaTea","language_code":"en"},"chat":{"id":5273618487,"first_name":"Kuma","last_name":"Tea","username":"realKumaTea","type":"private"},"date":1697139614,"text":"/start","entities":[{"offset":0,"length":6,"type":"bot_command"}]}}', 'isBase64Encoded': False}`

</span>

Lambda 回传的 `response['body']` 必须是 str 类型，
否则会报 `[ERROR] Runtime.MarshalError: Unable to marshal response`

### 上传依赖

这个时候如果直接部署会报错：找不到依赖

![](img/AWS-03-deps-01.jpg)

AWS Lambda 奇葩的设计导致我们不能上传
`requirements.txt` 让它自己安装，
必须自己手动下载依赖并上传。

首先需要找一台 Linux 机器，运行 docker

```shell
docker run -it --rm --name test python:3.11-slim /bin/bash
```

![](img/AWS-03-deps-02.jpg)

然后安装所需依赖

```shell
apt update -qq && apt install zip -y -qq

cd /tmp
mkdir python
pip install "python-telegram-bot<20" -t python -q
zip -r python.zip python
```

![](img/AWS-03-deps-03.jpg)

再把生成的 `python.zip` 复制出来

记得新开个 shell 别傻乎乎把 docker 退了

```shell
docker cp test:/tmp/python.zip .
```

Docker 容器这个时候可以关了

继续下拉，在 Layers 这里点击 **Add a layer**

![](img/AWS-03-deps-04.jpg)

点 `AWS layers` 上面那行小字 `create a new layer`

![](img/AWS-03-deps-05.jpg)

随便写，上传，提交

![](img/AWS-03-deps-06.jpg)

重新回到 Lambda dashboard，拉到下面，
点开熟悉的 Add a layer，
选择 Custom layers，选刚刚创建的，右下角 Add

![](img/AWS-03-deps-07.jpg)

最后点 Code Source 旁边的 Deploy

### 其他设置

环境变量在下方 Configuration - Environment variables 里面，
设置简单不再赘述。

![](img/AWS-04-settings-01.jpg)

### 完成

已成功运行

![](img/AWS-05-done-01.jpg)

## Azure Functions

Azure 更是重量级，Web 端功能复杂甚至缺失，
必须使用 VS Code 才能完整部署

### 准备

你需要安装一个 [VS Code](https://code.visualstudio.com/)

然后安装 [Azure Functions 插件](https://marketplace.visualstudio.com/items?itemName=ms-azuretools.vscode-azurefunctions)

![](img/Azure-00-prep-01.jpg)

安装好之后，会在左边栏看到一个 A 图标

点击并登录，直到看到你使用的产品都列出了

![](img/Azure-00-prep-02.jpg)

### 创建 Functions

左下角 Workspace，鼠标移上去会有一个 Functions 图标出现

![](img/Azure-01-create-01.jpg)

点击第二个 Create New Project

回到上方，选择一个空文件夹

语言根据需要选，模型默认 V2, Python 环境可以选择有的也可以跳过

Template 选择 HTTP Trigger

![](img/Azure-01-create-02.jpg)

Trigger 名称是你的 API 路径，这里我改成了 `bot`

![](img/Azure-01-create-03.jpg)

然后认证选择 Anonymous

![](img/Azure-01-create-04.jpg)

就可以打开生成的代码文件编辑了

### 填入代码

首先这个 Create New Function 是没有用的

![](img/Azure-02-code-01.jpg)

它不过是在你的代码里加一个入口，可以自己写

把代码贴进去就好了，不赘叙

主函数示例：

```python
@app.route(route="bot", auth_level=func.AuthLevel.ANONYMOUS)
def main(req):
    res = ''
    try:
        if not req.method == "POST":
            return 'I am working!'
        update = Update.de_json(req.get_json(), bot)
        if update.inline_query:
            res = inline(update)
        elif update.message:
            msg = update.message
            if msg.chat.id > 0:
                res = msg.reply_text(nonsense_reply())
        else:
            logger.info('Unknown type. Ignoring...')
    except Exception as e:
        logger.debug(str(req.get_json()))
        logger.error(str(e))
    return res if type(res) is str else ''
```

这里要特别注意的是，
入口参数 **必须是 `req`**，
如果不一致，部署后会找不到 HTTP Trigger!!!

![](img/Azure-02-code-02.jpg)

微软没有任何文档提到这一点！我是怎么发现的呢？

原先一直用的是 `request` 当入口，
因为一直部署失败，乱翻文档，在 [HTTP Trigger](https://learn.microsoft.com/en-us/azure/azure-functions/functions-bindings-http-webhook-trigger#decorators) 看到这么一句

> `trigger_arg_name`	Argument name for HttpRequest, defaults to 'req'.

没事限制参数干嘛？我就改成 `req` 居然就成功了

### 部署和设置

工作区 Azure 图标 - Create Function App in Azure

![](img/Azure-03-deploy-01.jpg)

会需要你填写一个唯一的不重复的名字，因为这个到时候会写到 API 的 URL 里面

我这里用的是 `kmlt`

然后选择环境和地区，完成和等待创建即可

![](img/Azure-03-deploy-02.jpg)

![](img/Azure-03-deploy-03.jpg)

随后上方可见刚刚创建的 Function App

![](img/Azure-03-deploy-04.jpg)

---

创建好，部署之前，
如果你有环境变量需要设置，
点开
Azure -
Resources -
Function App -
kmlt,
在 **`Application Settings`** 上右键，
在弹出窗口中分别填入环境变量的名字和值

![](img/Azure-03-deploy-05.jpg)

---

完成后，点击 Functions 图标，选择
**Deploy to Function App...**

上方选择刚创建的，
弹出警告点 Deploy

右下角会开始输出部署 log

![](img/Azure-03-deploy-06.jpg)

### 完成

完成后 log 会显示你的 Trigger URL

![](img/Azure-04-done-01.jpg)

可以打开 URL 测试

![](img/Azure-04-done-02.jpg)

## 总结

平心而论，
Azure 的部署过程其实是很方便的，
尤其是对于那些用惯了 VS Code 的人来说。

然而由于微软的文档过于语焉不详才让我吃了那么多苦头，
没有这件事就没有这篇发奋而作的 blog，
笑死。
