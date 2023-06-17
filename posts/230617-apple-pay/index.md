---
title: "Apple Pay 绑卡失败可能原因"
description: "Apple Pay 绑卡失败的原因分析与疑难解答"
date: "2023-06-17 15:00:00+0800"
image: "img/err-invalid.jpg"
categories:
  - Guide
  - Troubleshoot
tags:
  - Bank
  - Cards
  - Guide
  - Troubleshoot
  - Apple
  - Apple Pay
---

# Apple Pay 绑卡失败可能原因

先上目前绑卡截图镇楼

![](img/apple-wallet.jpg)

## 常见错误

### 您的发卡机构尚未提供对该卡的支持

> Your issuer does not yet offer support for this card

![](img/err-not-support.jpg)

* 中国大陆发行的非银联卡

### 卡的设备限制

> Card device limit

![](img/err-limit.jpg)

* 如果确认已解绑多余设备， [可尝试等待3天](https://discussionschinese.apple.com/thread/253116288?answerId=255886195322#255886195322)

### 卡片无效

> Invalid card

![](img/err-invalid.jpg)

* 该卡号今日已失败5次，明日再试

### 无法添加卡

> Could not add card
> Card not added

![](img/err-could-not-add.jpg)

![](img/err-not-added.jpg)

* 原因不明，建议跟客服对线

## 客服聊天记录

建议：先找银联问错误代码，再找对应银行；

银联首选云闪付线上客服，银行首选电话客服。

### 银联

> 碰到绑不上的问题可以先向银联咨询错误代码

![](img/chat-up-agent.jpg)

### 中国银行

> 中行电话客服才有足够权限，在线客服只能问到通用信息

![](img/chat-boc-bot.jpg)

![](img/chat-boc-agent.jpg)

* 每人无论单个或多个设备，最多绑定 **3次** 借记卡
* 绑卡超出上限 (新版 iOS [据说移除了](https://t.me/DocOfCard/2019) 这个上限)

## 参考资料

* [中国银行绑定 Apple Pay 失败的解决方法](https://www.jimmytian.com/archives/solve-apple-pay-cant-add-boc-card.html)
* [钱包解绑银行卡后无法再重新绑定，提示设备限制](https://discussionschinese.apple.com/thread/253116288?answerId=255886195322#255886195322)
