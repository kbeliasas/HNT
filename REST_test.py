#!/usr/bin/env python

import httplib2
import json

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
    all_OF_node_ports.append(OF_node_names)
    all_OF_node_macs.append(OF_node_macs)


print all_OF_node_ports
print
print all_OF_node_macs