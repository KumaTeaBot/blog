# 诺基亚贝尔光猫宽带密码破解提取

## 前言

本教程适用于诺基亚贝尔光猫，型号 `HGW` 或 `G-140W-**`

![设备信息](img/02-info.jpg)

---

此型号的光猫不可开启 `telnet`:

* `http://192.168.1.1/getpage.gch?pid=1002&nextpage=tele_sec_tserver_t.gch`
* `http://192.168.1.1/cgi-bin/telnetenable.cgi?telnetenable=1`

以上地址均无效。

---

F12 大法无效：

![](img/03-net-config.jpg)

`密码` 文本框一经选中内容就会消失；

![](img/04-net-inspect.jpg)

使用 `F12` 审查元素，会发现该处明文为 `!!!@@@`
，不是合法的宽带拨号密码。

## 教程

### 1. 登录

```
username: CMCCAdmin
password: aDm8H%MdA
```

![](img/01-login.jpg)

### 2. 打开如下地址

`http://192.168.1.1/dumpdatamodel.cgi`

![](img/05-dump.jpg)

搜索宽带账号
(如 `139.gd`)
在下方找到密码字段。

### 3. 提取密码

Ref:
[thedroidgeek / nokia-router-cfg-tool.py](https://gist.github.com/thedroidgeek/80c379aa43b71015d71da130f85a435a)

首先安装依赖

```bash
conda install pycryptodome || pip install pycryptodome
```

随后运行：

```python
import base64

class RouterCrypto:
    def __init__(self):
        from Crypto.Cipher import AES
        # key and IV for AES
        key = '3D A3 73 D7 DC 82 2E 2A 47 0D EC 37 89 6E 80 D7 2C 49 B3 16 29 DD C9 97 35 4B 84 03 91 77 9E A4'
        iv  = 'D0 E6 DC CD A7 4A 00 DF 76 0F C0 85 11 CB 05 EA'
        # create AES-128-CBC cipher
        self.cipher = AES.new(bytes(bytearray.fromhex(key)), AES.MODE_CBC, bytes(bytearray.fromhex(iv)))

    def decrypt(self, data):
        output = self.cipher.decrypt(data)
        # remove PKCS#7 padding
        return output[:-ord(output[-1:])]


encrypted = input('请输入密码字串：')
print('解密密码为：', RouterCrypto().decrypt(base64.b64decode(encrypted)).decode('UTF-8'))
```

![](img/06-decrypt.jpg)
