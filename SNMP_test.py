#!/usr/bin/env python

import easysnmp

# ip = '192.168.226.152' # Pirmas irenginys
ip = '192.168.50.100' # Testuojamas irenginys
com = 'public'



def get_ip_add(ip):
    session = easysnmp.Session(hostname=ip, version=2, community=com)
    res = session.get('.1.0.8802.1.1.2.1.3.8.1.2')
    return res.value

ip_add = get_ip_add(ip)
print ip_add
