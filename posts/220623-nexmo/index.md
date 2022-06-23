---
title: "Nexmo 虚拟手机号浅探"
description: "全网最低成本注册 Google Voice"
date: "2022-06-23 18:00:00+0800"
image: "img/cover.jpg"
categories:
  - Guide
tags:
  - Guide
  - Telegram
  - Google
---

# Nexmo 虚拟手机号浅探

> 最低成本：6.5元

### 前情提要

5月，我的 Telegram 被误封了。众所周知，Telegram
和微信一样不存在客服，因此我只能重新注册一个账号。

想起来18年似乎注册过一个叫 [Nexmo](https://www.nexmo.com)
的虚拟号码平台，还充值了10欧元，
但当时因为需要编程才能使用，就放置了。

这次重新登录，发现已经可以不用写代码，于是欣然注册，分享如下。

### 0. 准备工作

注册及充值略（因为是四年前 😩

[sign up](https://dashboard.nexmo.com/sign-up)

* 支持 支付宝 / 微信 / 银联
* **Nexmo 最低充值金额为 10 欧元**，建议拼车

## 1. 选用号码

注册完毕并充值后，进入
[主页](https://dashboard.nexmo.com/)

<img alt="dashboard" src="img/001-dashboard.jpg" width="640"/>

点击左侧 **构建和管理** - **号码** - **[购买号码](https://dashboard.nexmo.com/buy-numbers)**

<img alt="number" src="img/002-number.jpg" width="640"/>

选择 `国家/地区` 为 **United States (+1)**，
`功能` 为 **SMS**，
类型为 **Any**

下方的 `Number` 如果有想要的数字可以填写，
临时号码留空即可

<img alt="select" src="img/003-select.jpg" width="640"/>

选择一个你喜欢的号码，点击 **购买**

<img alt="confirm" src="img/004-confirm.jpg" width="640"/>

你应该能在 **构建和管理** - **号码** - **[您的号码](https://dashboard.nexmo.com/your-numbers)**
看见刚刚购买的号码

<img alt="status" src="img/005-status.jpg" width="640"/>

## 2. 注册 Google Voice

打开 [Google Voice](https://voice.google.com) ，
进入 [设置](https://voice.google.com/u/0/settings) ，
点击 **New linked number** 按钮

<img alt="gv" src="img/006-gv.jpg" width="640"/>

填入刚才购买的号码，点击 **Send code**

回到 **日志** - **[短信日志](https://dashboard.nexmo.com/sms/logs)**

<img alt="log" src="img/007-log.jpg" width="640"/>

更改 `指示` 为 **入站**，点击 **搜索**

<img alt="query" src="img/008-query.jpg" width="640"/>

再把验证码填入 Google Voice，完成验证

---

### 后记

正如前文所述，
Nexmo 的正规用法是编程和使用 API，
因此如果有能力，可以搭建 Webhook，
甚至可以实现转发到 Telegram 的效果

<img alt="flask" src="img/009-flask.jpg" width="640"/>

<img alt="response" src="img/010-response.jpg" width="640"/>

### Discussion

* 「全网最低成本」指每个虚拟手机号每月租用成本为 0.9 欧元，约合人民币 6.5 元
* 作者申明没有收到任何资助，且无利益相关（废话）
