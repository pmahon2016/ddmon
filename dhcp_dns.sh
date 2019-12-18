#!/bin/bash

/bin/sleep 20
/sbin/ifconfig wlan0 down 
/etc/init.d/isc-dhcp-server start
/bin/systemctl restart bind9

/bin/mkdir /root/yes
