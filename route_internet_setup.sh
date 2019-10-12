#!/bin/bash

# use this scrip to enable routing on the Raspberry Pi. Routing would be used for testing the dhcp in an separate lan
# before connecting to your main wifi router


# enable forwarding on the PI
echo 1> /proc/sys/net/ipv4/ip_forward


IPT=/sbin/iptables
LOCAL_IFACE=eth0
INET_IFACE=wlan0
INET_ADDRESS=192.168.1.185


# Flush the tables
$IPT -F INPUT
$IPT -F OUTPUT
$IPT -F FORWARD

$IPT -t nat -P PREROUTING ACCEPT
$IPT -t nat -P POSTROUTING ACCEPT
$IPT -t nat -P OUTPUT ACCEPT

# Allow forwarding packets:
$IPT -A FORWARD -p ALL -i $LOCAL_IFACE -j ACCEPT
$IPT -A FORWARD -i $INET_IFACE -m state --state ESTABLISHED,RELATED -j ACCEPT

# Packet masquerading
$IPT -t nat -A POSTROUTING -o $INET_IFACE -j SNAT --to-source $INET_ADDRESS
