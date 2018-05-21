#!/usr/bin/env python

import easysnmp
#import networkx as nx
#import matplotlib.pyplot as plt
import httplib2
import json
import sys
import logging
from ncclient import manager

log = logging.getLogger(__name__)

ip = '192.168.50.100'
com = 'public'
man_vlan = '500'
prod_vlan = "50"
user = "admin"
password = "cisco"
added_macs = []

ADD_MAC_ADDRESS = """
<config>
        <cli-config-data>
            <cmd>mac address-table static %s vlan %s drop</cmd>
        </cli-config-data>
</config>
"""

REMOVE_MAC_ADDRESS = """
<config>
        <cli-config-data>
            <cmd>no mac address-table static %s vlan %s drop</cmd>
        </cli-config-data>
</config>
"""

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
        if res1 == None:
            for item in res:
                if item.value == "34":
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

def _check_response(rpc_obj, snippet_name):
    log.debug("RPCReply for %s is %s" % (snippet_name, rpc_obj.xml))
    xml_str = rpc_obj.xml
    if "<ok />" in xml_str:
        log.info("%s successful" % snippet_name)
    else:
        log.error("Cannot successfully execute: %s" % snippet_name)

def add_mac_second(host, user, password, mac, vlan):
    with manager.connect(host=host, port=22, username=user, password=password, hostkey_verify=False, allow_agent=False, look_for_keys=False) as m:
        try:
            confstr = ADD_MAC_ADDRESS % (mac, vlan, interface)
            rpc_obj = m.edit_config(target='running', config=confstr)
            _check_response(rpc_obj, 'ADD_MAC_ADDRESS')
        except Exception:
            log.exception("Exception in adding %s mac %s vlan" % (mac, vlan))

def remove_mac_second(host, user, password, mac, vlan):
    with manager.connect(host=host, port=22, username=user, password=password, hostkey_verify=False, allow_agent=False, look_for_keys=False) as m:
        try:
            confstr = ADD_MAC_ADDRESS % (mac, vlan, interface)
            rpc_obj = m.edit_config(target='running', config=confstr)
            _check_response(rpc_obj, 'REMOVE_MAC_ADDRESS')
        except Exception:
            log.exception("Exception in removing %s mac %s vlan" % (mac, vlan))

def add_mac(host,user,password,mac,vlan):
    if __name__ == '__main__':
        logging.basicConfig(level=logging.INFO)
        add_mac_second(host,user,password, mac, vlan)

def remove_mac(host,user,password,mac,vlan):
    if __name__ == '__main__':
        logging.basicConfig(level=logging.INFO)
        remove_mac_second(host,user,password, mac, vlan)

h = httplib2.Http(".cache")
h.add_credentials('admin', 'admin')
resp, content = h.request('http://192.168.50.254:8181/restconf/operational/opendaylight-inventory:nodes', "GET")


OF_swi = []
all_OF_node_ports = []
all_OF_node_macs = []

allOFnodes = json.loads(content)

for node in allOFnodes['nodes']['node']:
    OF_node_macs = []
    for node_connector in node['node-connector']:
        OF_node_macs.append(node_connector['flow-node-inventory:hardware-address'])
    all_OF_node_macs.append(OF_node_macs)

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
        print "1"
        temp_list.append(item)
        tested.append(item)
    elif get_man_ip_add(item) == None:
        print "2"
        print str(item) + " Don't have man VLAN"
        temp_list.append(item)
        tested.append(item)
    else:
        temp_list.append(get_man_ip_add(item))
all_list.append(temp_list)


x = 0
y = 0
z = 0
while (x > -1):
    while (y > -1):
        while (z > -1):
            #time.sleep(5)
            if (all_list[x][y] == tested[z]):
                if (len(all_list[x]) > y + 1):
                    y = y + 1
                    z = 0
                elif (len(all_list[x]) <= y + 1):
                    if (len(all_list) > x + 1):
                        x = x + 1
                        y = 0
                        z = 0
                    elif (len(all_list) <= x + 1):
                        x = -2
                        y = -2
                        z = -2
                        break
            elif (all_list[x][y] != tested[z]):
                if (len(tested) > z + 1):
                    z = z + 1
                elif (len(tested) <= z + 1):
                    ip = all_list[x][y]
                    if ip != get_man_ip_add(ip):
                        b = 0
                        while (b > -1):
                            print 'b = ' + str(b)
                            print "manage = " + str(manage[b])
                            print "get_man_ip_add(ip) = " + str(get_man_ip_add(ip))
                            if manage[b] == get_man_ip_add(ip):
                                tested.append(ip)
                                b = -2
                                break
                            elif manage[b] != get_man_ip_add(ip):
                                if (len(manage) > b + 1 ):
                                    b = b + 1
                                elif (len(manage) <= b + 1):
                                    tested.append(ip)
                                    tested.append(get_man_ip_add(ip))
                                    manage.append(get_man_ip_add(ip))
                                    temp_list = []
                                    for item in get_ip_add(ip):
                                        if get_man_ip_add(item) == 'failed':
                                            temp_list.append(item)
                                            tested.append(item)
                                        elif get_man_ip_add(item) == None:
                                            temp_list.append(item)
                                            tested.append(item)
                                            print str(item) + "Don't have man VLAN"
                                        else:
                                            temp_list.append(get_man_ip_add(item))
                                    all_list.append(temp_list)
                                    b = -2
                                    break
                    elif ip == get_man_ip_add(ip):
                        tested.append(ip)
                        manage.append(ip)
                        temp_list = []
                        for item in get_ip_add(ip):
                            if get_man_ip_add(item) == 'failed':
                                temp_list.append(item)
                                tested.append(item)
                            elif get_man_ip_add(item) == None:
                                temp_list.append(item)
                                tested.append(item)
                                print str(item) + "Don't have man VLAN"
                            else:
                                temp_list.append(get_man_ip_add(item))
                        all_list.append(temp_list)
                    if (len(all_list[x]) > y + 1):
                        y = y + 1
                        z = 0
                    elif (len(all_list[x]) <= y + 1):
                        if (len(all_list) > x + 1):
                            x = x + 1
                            y = 0
                            z = 0
                        elif (len(all_list) <= x + 1):
                            x = -2
                            y = -2
                            z = -2
                            break


for x in range(0, len(all_OF_node_macs)):
    for y in range(0, len(manage)):
        try:
            macs = get_port_macs(manage[y])
            for mac in macs:
                mac = mac_corr(mac)
                if (mac == all_OF_node_macs[x][0]):
                    OF_swi.append(manage[y])
                    break
        except Exception as e:
            print "miss"


for list1 in added_macs:
    try:
        remove_mac(list1[0],user,password,list1[1],prod_vlan)
    except Exception:
        print "Nothing to remove"

dest_mac = []
node1 = []

for node in allOFnodes['nodes']['node']:
    for OF in OF_swi:
        try:
            macs = get_port_macs(OF)
            for mac in macs:
                mac = mac_corr(mac)
                for node_connector in node['node-connector']:
                    if mac == node_connector['flow-node-inventory:hardware-address']:
                        node1 = OF
                    break
        except Exception:
            print "miss"
    for node_table in node['flow-node-inventory:table']:
        if node_table["id"] == 0:
            try:
                for node_table_flow in node_table["flow"]:
                    try:
                        dest_mac = node_table_flow["match"]["ethernet-match"]["ethernet-destination"]["address"]
                        for x in range(0, len(manage)):
                            if node1 == manage[x]:
                                for swi in all_list[x]:
                                    try:
                                        add_mac(swi,user,password,dest_mac,prod_vlan)
                                        added_macs_temp = [swi,dest_mac]
                                        added_macs.append(added_macs_temp)
                                    except Exception:
                                        print "Device %s can't use netconf" % swi
                    except Exception:
                        err = 0
            except Exception:
                print "No flow entries in %s" % node["id"]



print 'OpenFlow = ' + str(OF_swi)


print 'Manage = ' + str(manage)
print 'all_list = ' + str(all_list)
print 'tested = ' + str(tested)


