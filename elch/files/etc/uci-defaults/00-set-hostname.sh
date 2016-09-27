#!/bin/sh
hn=elch_$(hostid | md5sum | cut -c1-3 )
uci set system.@system[0].hostname=$hn
uci commit
# add the hostname to /etc/hosts for proftpd to stop whining
sed -i "s/^127\.0\.0\.1/& $hn/" /etc/hosts
