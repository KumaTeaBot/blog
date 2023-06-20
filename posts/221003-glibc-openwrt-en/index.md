# Add glibc to OpenWrt

> [中文版](/p/221003-glibc-openwrt/)

I'm trying to replace `traceroute` with a tool called
[BestTrace](https://www.ipip.net/download.html),
but an error was raised during execution:

> Failed to execute process './besttrace'. Reason:
> 
> The file './besttrace' does not exist or could not be executed.

![Error](/p/221003-glibc-openwrt/img/01-error.jpg)

Check the executable with `file`:

> besttrace: ELF 64-bit LSB executable, x86-64, version 1 (SYSV), dynamically linked, **interpreter /lib64/ld-linux-x86-64.so.2**, Go BuildID=1c1dnBC1TKT-wnm6J_Ek/Csaj2Jrm0niZmmJ8paMZ/_hoguDO-XKYO0IWEnHWa/H2kGhpM-teit7NepUJE5, not stripped

Noticed that, `interpreter /lib64/ld-linux-x86-64.so.2`,
which means the arch `x86-64` is correct, but `glibc` runtime is missing.

Since 2015, [for consideration of the space and speed of embedded devices](https://news.ycombinator.com/item?id=9941076),
OpenWrt has swutched to [musl](https://musl.libc.org/) from uClibc as C library.

Whereas nowadays most software are using `glibc`, which cannot be run on OpenWrt.

## Solution

Just copy `ld-linux-x86-64.so.2` here!

### Docker

If Docker is installed:

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

This means you can always get the latest libs,
and switch to other distros you like.

### Directly

> Note: glibc v2.35, packed on 2022-10-03, could be outdated.

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

After these instructions the program can be run successfully.

![Done](/p/221003-glibc-openwrt/img/02-done.jpg)
