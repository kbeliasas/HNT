#!/usr/bin/env python

import easysnmp

ip = '192.168.50.4'
com = 'public'
man_vlan = '500'


def get_man_ip_add(ip): #Management IP
    try:
        session = easysnmp.Session(hostname=ip, version=2, community=com)
        res = session.walk('.1.3.6.1.2.1.4.20.1.2')
        res1 = None
        for item in res:
            if item.value == man_vlan:
                res1 = item.oid_index
                break
        if res1 == None:
            for item in res:
                if item.value == str(int(float(man_vlan)) + 329):
                    res1 = item.oid_index
                    break
        return res1
    except Exception as e:
        print 'Something wrong on ip = ' + ip
        print(e)
        ans = 'failed'
        return ans



if get_man_ip_add(ip) == None:
    print "HIT"
print get_man_ip_add(ip)