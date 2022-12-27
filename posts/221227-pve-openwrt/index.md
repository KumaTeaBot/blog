---
title: "PVE 更新 OpenWrt 教程"
description: "一种更新运行在 Proxmox VE 中的 OpenWrt 虚拟机的固件版本的方案"
date: "2022-12-27 17:00:00+0800"
image: "img/cover.jpg"
categories:
  - Guide
tags:
  - Guide
  - OpenWrt
  - Proxmox
  - VM
---

# PVE 更新 OpenWrt

## 准备工作

* OpenWrt 固件
  ![Firmware](img/01-firmware.jpg)
  * 建议编译时 **不要** 选中 `gzip` 压缩，否则容易出现各种奇妙的问题
  * 一般情况下不选用名称带有 `rootfs` 的固件

* USB 网卡 (可选)
  ![USB Ethernet](img/02-usb.jpg)
  * 如果你和我一样把全部网口都直通了，则需要在更新时使用其他的方式连接到 PVE
  * PVE 默认不会自动启用新插入的网卡，你可能需要
    `ifup enx00xxxxxxxxxx && ip link set dev enx00xxxxxxxxxx up`
    其中网卡名 `enx00xxxxxxxxxx` 可以在 `ifconfig` 查询
  ![ifup](img/03-ifup.jpg)


## 为什么不能用正常方式升级？

众所周知，OpenWrt 正常升级方式是在 `系统` - `备份升级` 中升级：

![Upgrade](img/04-upgrade.jpg)

但你会发现 x86 固件是不包含 `sysupgrade` 固件的：

![Checksum](img/05-checksum.jpg)

所以，对于运行在 Proxmox VE 中的 OpenWrt 虚拟机，我们只能通过手动方式升级

---

在开始之前，请确保你划分了一块虚拟硬盘作为 `overlay` 分区放置配置。

![overlay](img/06-overlay.jpg)

如果没有，我强烈建议你花十分钟搜下教程
(关键词 `extroot overlay`)
完成这件事， **功在当代利在千秋**

## 上传新固件

上传到 `local` - `ISO`

![Upload firmware](img/07-upload.jpg)

推荐检查 `sha256sum`

## 更换系统固件

1. 在以非目标 OpenWrt 内网的方式连接 PVE 的情况下，关闭虚拟机 <br>
  ![Shutdown](img/08-shutdown.jpg)
  可以用 PVE 的 `Shutdown` 按钮，也可以在 Console 输入 `poweroff` <br>
2. 选中系统盘 <br>
  ![Select](img/09-select.jpg)
  点击 `Detach` 并确认 <br>
  ![Detach](img/10-detach.jpg)
  再在下方找到 `Unused Disk 0` 并 `Remove` 删除 <br>
  ![Remove](img/11-remove.jpg)
3. 导入新固件 <br>
  来到 **PVE 的 Console** 输入： <br>
  `qm importdisk 101 /var/lib/vz/template/iso/openwrt-x86-64-generic-squashfs-combined-efi.img local-lvm` <br>
  其中 `101` 是你的 OpenWrt 虚拟机 ID
  ![Import](img/12-import.jpg)
  随后一个新的 `Unused Disk 0` 出现了
  ![Found new Unused](img/13-disk.jpg)
4. 启用新系统盘 <br>
  选中新的 `Unused Disk 0` 并点击 `Edit`，确认即可 <br>
  ![Attach Unused Disk 0](img/14-edit.jpg)
5. 启动虚拟机

## 恢复配置

1. 按一下回车激活 Console <br>
  ![Activate console](img/15-console.png)
2. 此时，原先的 `overlay` 会被自动挂在为 `/mnt/sda1` (有时是 `sdb1`) <br>
  我们可以发现，该目录下 `etc` 内含有一 `.extroot-uuid` 文件。 <br>
  ![Cleanup](img/16-cleanup.jpg)
  这一文件会误导系统读取正确的 UUID 并导致无法挂载！ <br>
  使用 `rm -rf /mnt/sda1/etc` 将之删除。 <br>
  `/etc/fstab` 也是没用的： `rm -f /etc/fstab`
3. 查看自动生成的 `/etc/config/fstab` <br>
  ![Old fstab](img/17-old-fstab.jpg)
  * 去掉用不到的 `boot` 挂载
  * 把 `sda1` 的 UUID 移动到 `overlay` 配置下
  ![New fstab](img/18-new-fstab.jpg)
  保存后重启
4. 把修改的 `/etc/config/fstab` 同步到配置分区 <br>
  `cp -a /etc/config/fstab /mnt/sda1/upper/etc/config/`
  ![Sync config](img/19-sync-fstab.jpg)

---

## 完成

1. 重启
2. 检查 `df -h`，可发现配置分区已成功挂载！
  ![Reboot](img/20-reboot.jpg)

## References

我被万恶的 `.extroot-uuid` 困扰了几个月之久，直到看到了
[这篇帖子](https://forum.openwrt.org/t/solved-extroot-not-working-on-18-06/16723/2)

![Solution](img/21-forum.jpg)

因此写这篇教程广而告之。
