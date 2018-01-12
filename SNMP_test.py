#!/usr/bin/env python

import netsnmp

# ip = '192.168.226.152' # Pirmas irenginys
ip = '192.168.50.100' # Testuojamas irenginys

def get_ip_add(ip): # Pasiima kaimynus is irenginio.
    oid = netsnmp.VarList(netsnmp.Varbind('.1.3.6.1.4.1.9.9.23.1.2.1.1.4'))
    res = netsnmp.snmpwalk(oid, Version = 2, DestHost=ip, Community='public')
    return res

tested = []


ip_add = get_ip_add(ip)
device_list = []
for x in range(0, len(ip_add)):
    device_list.append(ip_add[x])
all_list = [device_list]
tested.append(ip)
