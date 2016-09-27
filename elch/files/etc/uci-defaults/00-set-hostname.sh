#!/bin/sh
uci set system.@system[0].hostname=elch_$(hostid | md5sum | cut -c1-3 )
uci commit
