#!/usr/bin/env python

import netsnmp

ip = '192.168.226.152'

def sys_name(ip):
    oid = netsnmp.VarList(netsnmp.Varbind('.1.3.6.1.2.1.1.5'))
    res = netsnmp.snmpwalk(oid, Version = 2, DestHost=ip, Community='public')
    return res[0]

def get_nei_name(ip):
    oid = netsnmp.VarList(netsnmp.Varbind('.1.3.6.1.4.1.9.9.23.1.2.1.1.6'))
    res = netsnmp.snmpwalk(oid, Version = 2, DestHost=ip, Community='public')
    return res

def get_ip_add(ip):
    oid = netsnmp.VarList(netsnmp.Varbind('.1.3.6.1.4.1.9.9.23.1.2.1.1.4'))
    res = netsnmp.snmpwalk(oid, Version = 2, DestHost=ip, Community='public')
    return res


device_list = { sys_name(ip) : ip }

nei_name = get_nei_name(ip)
ip_add = get_ip_add(ip)


for x in range(0, len(nei_name)):
    device_list[nei_name[x]] = ip_add[x]

tested = []
tested.append(ip)

print tested

print device_list 