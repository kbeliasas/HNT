#!/usr/bin/env python

import easysnmp

ip = '192.168.50.100'
com = 'public'
man_vlan = '500'

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
        for item in res:
            if item.value == man_vlan:
                return item.oid_index
                break
    except Exception as e:
        print 'Something wrong on ip = ' + ip
        print(e)
        ans = 'failed'
        return ans

tested = []
tested.append(ip)
manage = []
if ip != get_man_ip_add(ip):
    ip = get_man_ip_add(ip)
    tested.append(ip)
    manage.append(get_man_ip_add(ip))
all_list = []
temp_list = []
for item in get_ip_add(ip):
    if get_man_ip_add(item) != 'failed':
        temp_list.append(get_man_ip_add(item))
        print "1"
    elif get_man_ip_add(item) != None:
        temp_list.append(get_man_ip_add(item))
        print "2"
    elif get_man_ip_add(item) == None:
        print str(item) + "Don't have man VLAN"
all_list.append(temp_list)


print 'Manage = ' + str(manage)
print 'all_list = ' + str(all_list)
print 'tested = ' + str(tested)