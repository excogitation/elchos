#!/bin/sh

( sleep 10 && opkg update && opkg install /pkgs/*) &
