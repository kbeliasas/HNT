#!/usr/bin/env python

import easysnmp

ip = '192.168.50.100' # Testuojamas irenginys
com = 'public'



def get_ip_add(ip):
    session = easysnmp.Session(hostname=ip, version=2, community=com)
    res = session.walk('.1.0.8802.1.1.2.1.4.2.1.3')
    ans = []
    temp1 = []
    for item in res:
        temp1.append(item.oid)
    c = 0
    for item in temp1:
        a = 0
        b = 0
        while a < 4:
            if (item[len(item)-b] == '.'):
                ans[c].append(item[len(item)-b])
                a = a + 1
                b = b + 1
            else:
                ans[c].append(item[len(item)-b])
                b = b + 1
        c = c + 1
    return ans

ip_add = get_ip_add(ip)
print ip_add