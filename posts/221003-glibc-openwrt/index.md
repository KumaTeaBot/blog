# 向 OpenWrt 添加 glibc

> [English version](/p/221003-glibc-openwrt-en/)

今天试图在 OpenWrt 软路由上使用
[BestTrace](https://www.ipip.net/download.html) 替换 `traceroute`，
但下载完成后运行却出现了错误：

> Failed to execute process './besttrace'. Reason:
> 
> The file './besttrace' does not exist or could not be executed.

![Error](img/01-error.jpg)

使用 `file` 检查文件：

> besttrace: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, **interpreter /lib64/ld-linux-x86-64.so.2**, Go BuildID=1c1dnBC1TKT-wnm6J_Ek/Csaj2Jrm0niZmmJ8paMZ/_hoguDO-XKYO0IWEnHWa/H2kGhpM-teit7NepUJE5, not stripped

注意到 `interpreter /lib64/ld-linux-x86-64.so.2`，
说明架构 `x86-64` 无误，但缺少了 `glibc` 运行库。

自 2015 以后，[为了嵌入式设备的体积及运行速度考虑](https://news.ycombinator.com/item?id=9941076) ，
OpenWrt 使用 [musl](https://musl.libc.org/) 作为 C 运行库。

然而现在大部分软件都使用 `glibc`，在 OpenWrt 上就不能运行了。

## 解决方案

只要把 `ld-linux-x86-64.so.2` 复制进来就好了！

### Docker

如果安装了 Docker
可以使用如下脚本：

```shell
#!/usr/bin/env bash

set -ex

# working directory
# change to /opt, /usr/share or something else if you like
WK_DIR="/root/data"
mkdir -p $WK_DIR
cd $WK_DIR

# pull Ubuntu
docker pull ubuntu:jammy

# start a container
docker run -itd --name glibc ubuntu:jammy

# copy libs
docker cp -a glibc:/lib/x86_64-linux-gnu .

# link
ln -s "$WK_DIR/x86_64-linux-gnu"                      /lib/x86_64-linux-gnu     || echo "Link already exists."
ln -s "$WK_DIR/x86_64-linux-gnu/ld-linux-x86-64.so.2" /lib/ld-linux-x86-64.so.2 || echo "Link already exists."

# cleanup
docker stop glibc
docker rm   glibc
docker rmi  ubuntu:jammy
```

你也可以换用 Debian 或者任意你喜欢的发行版

### 直装

> 注：于 2022-10-03 打包的 glibc v2.35，可能过时

```shell
#!/usr/bin/env bash

set -ex

# working directory
# change to /opt, /usr/share or something else if you like
WK_DIR="/root/data"
mkdir -p $WK_DIR
cd $WK_DIR

# download
wget "https://github.com/KumaTea/blog/releases/download/221003/glibc.tar.gz"

# decompress
tar -xzf glibc.tar.gz

# link
ln -s "$WK_DIR/x86_64-linux-gnu"                      /lib/x86_64-linux-gnu     || echo "Link already exists."
ln -s "$WK_DIR/x86_64-linux-gnu/ld-linux-x86-64.so.2" /lib/ld-linux-x86-64.so.2 || echo "Link already exists."

# cleanup
rm -f glibc.tar.gz
```

---

操作完成后程序已可成功运行。

![Done](img/02-done.jpg)
