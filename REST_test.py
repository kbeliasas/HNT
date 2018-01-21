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
resp, content = h.request('http://192.168.50.254:8181/restconf/operational/opendaylight-inventory:nodes', "GET")

all_OF_node_ports = []
all_OF_node_macs = []

allOFnodes = json.loads(content)

for x in range(0, len(allOFnodes['nodes']['node'])):
    OF_node_ports = []
    OF_node_macs = []
    for y in range(0, len(allOFnodes['nodes']['node'][x])-2):
        OF_node_ports.append(allOFnodes['nodes']['node'][x]['node-connector'][y]['flow-node-inventory:port-number'])
        OF_node_macs.append(allOFnodes['nodes']['node'][x]['node-connector'][y]['flow-node-inventory:hardware-address'])
    all_OF_node_ports.append(OF_node_ports)
    all_OF_node_macs.append(OF_node_macs)


tested = ['']
device_nei_ports = []


ip_add = get_ip_add(ip)
port_list = get_id_port(ip)
device_list = []
all_ports_topology = []
port_list1 = []
for x in range(0, len(ip_add)):
    device_list.append(ip_add[x])
    all_ports_topology.append(port_list[x])
    port_list1.append(port_list[x])
device_nei = [device_list]
device_nei_ports = [port_list1]
tested.append(ip)



x = 0
y = 0
z = 0

while (x > -1):
    while (y > -1):
        while (z > -1):
            #print "x = " + str(x)
            #print "y = " + str(y)
            #print "z = " + str(z)
            if (device_nei[x][y] == tested[z]): # Jei jau testuotas, tai ...
                if (len(device_nei[x]) > y + 1): # Jei dar liko kaimynu, tai patikrink ji.
                    y = y + 1
                elif (len(device_nei[x]) <= y + 1): # Jei nebeliko kaimynu, tai ...
                    if (len(device_nei) > x + 1): # Jei yra kitu irenginiu, tai tikrink juos.
                        x = x + 1
                        y = 0
                        z = 0
                    elif (len(device_nei) <= x + 1): # Jei nebeliko irenginiu, tai uzbaik.
                        x = -2
                        y = -2
                        z = -2
                        break
            elif (device_nei[x][y] != tested[z]): # Jei dar netestuotas, tai ...
                if (len(tested) > z + 1): # Jei dar liko pratestuotu sarase irenginiu, tai perziurek juos.
                    z = z + 1
                elif (len(tested) <= z + 1): # Jei nebeliko pratestuotu sarase irenginiu, tai ieskok nauju kaimynu.
                    ip = device_nei[x][y]
                    ip_add = get_ip_add(ip)
                    if (ip_add != ['failed']):
                        port_list = get_id_port(ip)
                        device_list = []
                        port_list1 = []
                        for a in range(0, len(ip_add)):
                            device_list.append(ip_add[a])
                            all_ports_topology.append(port_list[a])
                            port_list1.append(port_list[x])
                        device_nei.append(device_list)
                        device_nei_ports.append(port_list1)
                        tested.append(ip)
                    else:
                        tested.append(ip)
                        failed.append(ip)
                    if (len(device_nei[x]) > y + 1): # Jei dar liko kaimynu, tai patikrink ji.
                        y = y + 1
                    elif (len(device_nei[x]) <= y + 1): # Jei nebeliko kaimynu, tai ...
                        if (len(device_nei) > x + 1): # Jei yra kitu irenginiu, tai tikrink juos.
                            x = x + 1
                            y = 0
                            z = 0
                        elif (len(device_nei) <= x + 1): # Jei nebeliko irenginiu, tai uzbaik.
                            x = -2
                            y = -2
                            z = -2
                            break

x = 0
y = 0
while (x > -1):
    while (y > -1):
        if (tested[x] == failed[y]):
            del tested[x]
            if (len(tested) <= x):
                x = -2
                y = -2
                break
            elif (len(tested) > x):
                y = 0
        elif (tested[x] != failed[y]):
            if (len(failed) <= y + 1):
                if (len(tested) <= x + 1):
                    y = -2
                    x = -2
                    break
                elif (len(tested) > x + 1):
                    y = 0
                    x = x + 1
            elif (len(failed) > y + 1):
                y = y + 1

del tested[0]

for x in range(0, len(all_OF_node_macs)):
    for y in range(0, len(tested)):
        try:
            macs = get_port_macs(tested[y])
            for mac in macs:
                mac = mac_corr(mac)
                if (mac == all_OF_node_macs[x][0]):
                    OF_swi.append(tested[y])
                    break
        except Exception as e:
            print "miss"


print OF_swi
print
print tested