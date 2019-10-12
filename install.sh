#!/bin/bash


apt -y update && apt -y install

apt -y install bind9
apt -y install isc-dhcp-server


cp /root/ddmon/named* /etc/bind/

cp /root/ddmon/db.* /var/cache/bind/

cp /root/ddmon/dhcpcd.conf /etc/

cp /root/ddmon/dhcpd.conf /etc/dhcp/

cp /root/ddmon/isc-dhcp-server  /etc/default/

chmod u+x /root/ddmon/runpython.sh


