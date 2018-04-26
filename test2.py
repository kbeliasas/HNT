#!/usr/bin/env python

import easysnmp

ip = '192.168.50.100'
com = 'public'

def get_man_ip_add(ip): #Management IP
    session = easysnmp.Session(hostname=ip, version=2, community=com)
    res = session.walk('.1.3.6.1.2.1.4.20.1.2')
    return res

print get_man_ip_add(ip)