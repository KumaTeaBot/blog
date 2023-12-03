# 制作 RHEL LXC 容器镜像

## 前言

虽然玩 Linux 很多年了，但一直以来都只是用
Debian 系的发行版，对其他的没有涉猎。
最近发现了 LXC 的美妙之处，于是试了试一直没体验过的 RHEL。

---

鲁迅先生说过，中国人的性情是总喜欢调和折中的。

作为硬件级的虚拟，VM 太过笨重，对内存的利用效率太低；
而作为应用级的虚拟，Docker 又太过轻量，systemd 也不能用，
只能用来部署单一程序。相比之下，作为系统级虚拟的 LXC
就是日常调试的最佳选择。

## 踩坑

我首先尝试的是官方 docker 镜像
[ubi (Universal Base Image)](https://catalog.redhat.com/software/containers/ubi9/ubi/615bcf606feffc5384e8452e),
通过 `docker save` 导出后直接导入到 PVE 中。
虽然可以启动，但是缺少太多组件，出现大量恶性问题，如无法联网等，不具备可用性。

然后尝试了去年试过的 [转生大法](https://blog.kmtea.eu/p/220710-pi-rhel/),
不过 `convert2rhel` 至今不支持 RHEL 9, 因此作罢。

---

然而，ubi 的文件结构是我们的重要参考，
后续我们打包的 rootfs 要力求与之一致。

![rootfs](img/00-ubi.jpg)

## 准备

打开 ISO [下载官网](https://developers.redhat.com/products/rhel/download),
**拉到下面**，选择 **Boot iso** 下载。~~当然你财力雄厚也可以选择十几G的 DVD iso~~

## 提取

这一步要从 RHEL 完整虚拟机中提取 rootfs。

![install](img/01-inst-01.jpg)

进入右上角，安装盘选择

![destination](img/01-inst-02.jpg)

下面选择自定义 Custom，否则它要给你创建 LVM 了

点击一次 Done 后，出来如下界面

![custom](img/01-inst-03.jpg)

选择标准分区 Standard Partition，然后点击上方蓝字
Click here to create them automatically

![partition](img/01-inst-04.jpg)

这里直接 Done 就行，但保险起见我把文件系统设为了 ext4

---

中间需要登录

登录后下方选择安装内容

![software](img/01-inst-05.jpg)

左边选择 Minimal Install，右边什么都不选

左下设置 root 密码就可以开始安装了

---

安装完成后，重启进入系统。
建议 ssh, vnc 没法复制粘贴，属于灾难级的体验。
然后执行

```shell
yum install -y tar

cd /tmp
mkdir afs boot dev home lost+found media mnt opt proc root run srv sys tmp
chmod -R 777 tmp
chown -R nobody:nobody proc sys
cp -a /bin /etc /lib /lib64 /sbin /usr /var .
rm -rf var/log/* var/cache/* var/tmp/*

tar cvJf rootfs.tar.xz ./*
```

生成 `rootfs.tar.xz` 后，任选方式传到 PVE 上。

我喜欢用 `python3 -m http.server 8080`，
但是要记得先关防火墙 `systemctl stop firewalld`。

![uploaded](img/01-inst-06.jpg)

## 精简

LXC 运行环境下，固件、内核均由宿主机提供，
我们可以将其卸载，节省空间。

由 `rootfs.tar.xz` 创建 lxc，启动后进入 shell

```shell
# dnf list --installed | grep firmware
# dnf list --installed | grep kernel
dnf remove -y iwl100-firmware.noarch iwl1000-firmware.noarch iwl105-firmware.noarch iwl135-firmware.noarch iwl2000-firmware.noarch iwl2030-firmware.noarch iwl3160-firmware.noarch iwl5000-firmware.noarch iwl5150-firmware.noarch iwl6000g2a-firmware.noarch iwl6050-firmware.noarch iwl7260-firmware.noarch linux-firmware.noarch linux-firmware-whence.noarch
dnf remove -y kernel.x86_64 kernel-core.x86_64 kernel-modules.x86_64 kernel-modules-core.x86_64 kernel-tools.x86_64 kernel-tools-libs.x86_64
dnf remove -y microcode_ctl
dnf clean all
```

一举节省高达一半空间

![uninstall](img/02-slim-01.jpg)

接下来是清除不必要的语言包，100M左右

```shell
cd /usr/share/locale
mkdir /tmp/locale
mv en* locale.alias /tmp/locale/
rm -rf ./*
mv /tmp/locale/* .
rmdir /tmp/locale
```

可以考虑关闭在容器中无法运行的服务

```shell
dnf remove -y audit
systemctl disable chronyd.service
```

最终体积来到 500M 左右，与官方 templates 同一水平。

![df](img/02-slim-02.jpg)

最后和上一步一样打包即可。

```shell
cd /tmp
mkdir afs boot dev home lost+found media mnt opt proc root run srv sys tmp
chmod -R 777 tmp
chown -R nobody:nobody proc sys
cp -a /bin /etc /lib /lib64 /sbin /usr /var .
rm -rf var/log/* var/cache/* var/tmp/*

tar cvJf rhel-9-minimal_9.3_amd64.tar.xz ./*
```

## 后记

![info](img/03-info-01.jpg)

有几点提醒：

1. 如果导入后启动，内存占用极低，终端黑屏无显示，可能是误删了 /etc 下账户文件 
   可通过 `lxc-start -n <ctid> -F -l DEBUG` 接入调试。
2. 非常不建议分享你制作的镜像！
   首先 `subscription-manager unregister` 不能保证账户信息完全被抹除，
   其次 `/etc` 下 `fstab` `hosts` `hostname` `resolv.conf` `shadow` 等大量文件均可能包含敏感信息。
