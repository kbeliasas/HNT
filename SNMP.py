#!/usr/bin/env python

import netsnmp

ip_add = '192.168.226.152'

def get_nei_name(ip_add):
    oid = netsnmp.VarList(netsnmp.Varbind('.1.3.6.1.4.1.9.9.23.1.2.1.1.6'))
    res = netsnmp.snmpwalk(oid, Version = 2, DestHost=ip_add, Community='public')
    return res

def get_ip_add(ip_add):
    oid = netsnmp.VarList(netsnmp.Varbind('. 1.3.6.1.4.1.9.9.23.1.2.1.1.4'))
    res = netsnmp.snmpwalk(oid, Version = 2, DestHost=ip_add, Community='public')
    return res

print get_nei_name(ip_add)
