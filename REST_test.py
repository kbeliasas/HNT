#!/usr/bin/env python

import httplib2
import json
import easysnmp

ip = '192.168.50.100'
com = 'public'
failed = []
new_failed = []
OF_swi = []

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

def get_id_port(ip): # Pasiima kaimynu sasaju numerius
    session = easysnmp.Session(hostname=ip, version=2, community=com)
    try:
        res = session.walk('.1.0.8802.1.1.2.1.4.1.1.7')
        ans = []
        for item in res:
            ans.append(item.value)
        return ans
    except Exception as e:
        ans = []
        ans.append('')
        return ans

def get_port_macs(ip):
    session = easysnmp.Session(hostname=ip, version=2, community=com, use_sprint_value=True)
    res = session.walk('.1.3.6.1.2.1.2.2.1.6')
    ans = []
    for item in res:
        ans.append(item.value)
    return ans

def mac_corr(string):
    a = 0
    x = 0
    while (x > -1):
        if (x < len(string)):
            if (string[x] != ':'):
                a = a + 1
            elif(string[x] == ':'):
                if (a < 2):
                    a = 0
                    string = string[:x-1] + '0' + string[x-1:]
                    x = x + 1
                elif (a >= 2):
                    a = 0
            x = x + 1
        else:
            if (a < 2):
                string = string[:x-1] + '0' + string[x-1:]
            x = -2
            break
    return string


h = httplib2.Http(".cache")
h.add_credentials('admin', 'admin')
resp, content = h.request('http://192.168.50.254:8181/restconf/operational/opendaylight-inventory:nodes/node/openflow:14193329701457472', "GET")


allOFnodes = json.loads(content)

print allOFnodes