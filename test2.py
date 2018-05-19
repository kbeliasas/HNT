#!/usr/bin/env python

import easysnmp
#import networkx as nx
#import matplotlib.pyplot as plt
import httplib2
import json

ip = '192.168.50.100'
com = 'public'
man_vlan = '500'
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
        ans = failed
        return ans

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


tested = []
tested.append(ip)
manage = []
manage.append(get_man_ip_add(ip))
if ip != get_man_ip_add(ip):
    ip = get_man_ip_add(ip)
    tested.append(ip)
all_list = []
temp_list = []
for item in get_ip_add(ip):
    if get_man_ip_add(item) == 'failed':
        temp_list.append(item)
        tested.append(item)
    elif get_man_ip_add(item) == None:
        print str(item) + " Don't have man VLAN"
        temp_list.append(item)
        tested.append(item)
    else:
        temp_list.append(get_man_ip_add(item))
all_list.append(temp_list)

print "get_ip_add = %s" % get_ip_add(ip)
