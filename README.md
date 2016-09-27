- high availablity hub:
  * https://github.com/krebscode/minikrebs/tree/master/traits/special_purpose/keepalive-hub
  * https://github.com/makefu/openwrt-custom-builder
- platform elchos:
  goflex net:
    * https://wiki.openwrt.org/toh/seagate/goflexnet
    * http://www.ebay.de/itm/Seagate-FreeAgent-GoFlex-Net-Device-server-0-2-STAK200-/181799012053?hash=item2a5410c6d5:g:4g0AAOSwgQ9VoLeU
    * https://www.amazon.de/Seagate-FreeAgent-GoFlex-Net-Media-Sharing-Lösung/dp/B003R02R2O
- dcpp:
  * https://github.com/makefu/eiskaltdcpp-daemon-openwrt

wget with ssl
opkg update
opkg install wget
opkg install ca-certificates


#auto mounting hdd
remove the /etc/config/fstab symlink to /tmp/fstab

```
opkg install block-mount
block detect > /etc/config/fstab
/etc/init.d/fstab enable
#set option enabled 1 in fstab
```

#file system
```
opkg install e2fsprogs
```


TODO:
* set unique hostname to /etc/uci-defaults/01-set-hostname.sh
* say hello when booted up (local ip + name)
* password for eiskaltdcpp client?


quickfind players
dchubs
M: e4:95:6e:40:20:1b 10.42.22.159
S: e4:95:6e:40:20:1d 10.42.20.118 

goflexnet
1: 00:10:75:26:73:16 10.42.22.163
2: 00:10:75:26:71:DA 10.42.21.220
3: 00:10:75:26:73:3B 



hdd benchmarks:
write
time dd if=/dev/zero of=/mnt/sda1/1GB bs=1M count=1000
ext2	real	0m 17.37s
ext3	real	0m 19.48s
ext4	real	0m 13.77s

read
time dd if=/mnt/sda1/1GB of=/dev/null bs=1M count=1000
ext2	real	0m 8.83s
ext3	real	0m 8.82s
ext4	real	0m 11.87s


