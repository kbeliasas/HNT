#!/usr/bin/env python

import netsnmp

def getnameofnei():
    oid = netsnmp.VarList(netsnmp.Varbind('.1.3.6.1.4.1.9.9.23.1.2.1.1.6'))
    res = netsnmp.snmpwalk(oid, Version = 2, DestHost='192.168.226.152', Community='public')
    return res

print getnameofnei()
