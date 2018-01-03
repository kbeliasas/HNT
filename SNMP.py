#!/usr/bin/env python

import netsnmp

ip = '192.168.226.152'


def get_ip_add(ip):
    oid = netsnmp.VarList(netsnmp.Varbind('.1.3.6.1.4.1.9.9.23.1.2.1.1.4'))
    res = netsnmp.snmpwalk(oid, Version = 2, DestHost=ip, Community='public')
    return res


ip_add = get_ip_add(ip)

device_list = []

for x in range(0, len(ip_add)):
    device_list.append(ip_add[x])

all_list = [device_list]

tested = []
tested.append(ip)

print tested


x = 0
while (x < 100):
    for a in range(0, len(all_list[x])):
        for b in range(0, len(tested)):
            if (all_list[x][a] == tested[b]):
                break
        ip = all_list[x][a]
        ip_add = get_ip_add(ip)

        




print device_list 