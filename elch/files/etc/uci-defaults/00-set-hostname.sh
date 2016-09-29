#!/bin/sh

# hostname already set:
test -e /etc/hostid && exit 0

dd if=/dev/urandom count=50 bs=1 | md5sum  | cut -d\  -f 1  > /etc/hostid
hn=elch_$(hostid | cut -c1-3 )
uci set system.@system[0].hostname=$hn
uci commit
# add the hostname to /etc/hosts for proftpd to stop whining
sed -i "s/^127\.0\.0\.1/& $hn/" /etc/hosts
