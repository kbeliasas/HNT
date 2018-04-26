#!/usr/bin/env python

import easysnmp

ip = '192.168.50.100'
com = 'public'
man_vlan = '500'

def get_man_ip_add(ip): #Management IP
    session = easysnmp.Session(hostname=ip, version=2, community=com)
    res = session.walk('.1.3.6.1.2.1.4.20.1.2')
    for item in res:
        if item.value == man_vlan:
            return item.oid_index
            break

def get_ip_add(ip): # Pasiima kaimyu adresus is irenginio.
    session = easysnmp.Session(hostname=ip, version=2, community=com)
    try:
        res = session.walk('.1.0.8802.1.1.2.1.4.2.1.3')
        ans = []
        temp1 = []
        for item in res:
            temp1.append(item.oid)
        c = 0
        for item in temp1:
            ans.append('')
            a = 0
            b = 1
            while a < 4:
                if (item[len(item)-b] == '.'):
                    ans[c] = item[len(item)-b] + ans[c]
                    a = a + 1
                    b = b + 1
                else:
                    ans[c] = item[len(item)-b] + ans[c]
                    b = b + 1
            ans[c] = ans[c].lstrip('.')
            c = c + 1
        return ans
    except Exception as e:
        print 'Something wrong on ip = ' + ip
        print(e)
        ans = []
        ans.append('failed')
        return ans

print get_man_ip_add(ip)