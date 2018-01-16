#!/usr/bin/env python

import easysnmp
import networkx as nx
import matplotlib.pyplot as plt

# ip = '192.168.226.152' # Pirmas irenginys
ip = '192.168.50.100'
com = 'public'
failed = []
new_failed = []

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

def draw_topology(graph, labels=None, graph_layout='shell',
               node_size=1600, node_color='blue', node_alpha=0.3,
               node_text_size=12,
               edge_color='blue', edge_alpha=0.3, edge_tickness=1,
               edge_text_pos=0.3,
               text_font='sans-serif'):
    G=nx.Graph()

    for edge in graph:
        G.add_edge(edge[0], edge[1])

    if graph_layout == 'spring':
        graph_pos=nx.spring_layout(G)
    elif graph_layout == 'spectral':
        graph_pos=nx.spectral_layout(G)
    elif graph_layout == 'random':
        graph_pos=nx.random_layout(G)
    else:
        graph_pos=nx.shell_layout(G)


    nx.draw_networkx_nodes(G, graph_pos, node_size=node_size, alpha=node_alpha, node_color=node_color)
    nx.draw_networkx_edges(G, graph_pos, width=edge_tickness, alpha=edge_alpha, edge_color=edge_color)
    nx.draw_networkx_labels(G, graph_pos, font_size=node_text_size, font_family=text_font)

    if labels is None:
        labels = range(len(graph))

    edge_labels = dict(zip(graph, labels))
    nx.draw_networkx_edge_labels(G, graph_pos, edge_labels=edge_labels, label_pos=edge_text_pos)

    plt.show()


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

realations = []

del tested[0]

print tested


for x in range(0, len(tested)):
    for y in range(0, len(device_nei[x])):
        temp = (tested[x], device_nei[x][y])
        realations.append(temp)



draw_topology(realations,all_ports_topology)

ip = tested[0]
new_tested = ['']

ip_add = get_ip_add(ip)
port_list = get_id_port(ip)
device_list = []
all_ports_topology = []
port_list1 = []
for x in range(0, len(ip_add)):
    device_list.append(ip_add[x])
    all_ports_topology.append(port_list[x])
    port_list1.append(port_list[x])
new_device_nei = [device_list]
new_device_nei_ports = [port_list1]
new_tested.append(ip)


a = 1
while(a > 0):
    x = 0
    y = 0
    z = 0
    while (x > -1):
        while (y > -1):
            while (z > -1):
                if (new_device_nei[x][y] == new_tested[z]):
                    if (len(new_device_nei[x]) > y + 1): # Jei dar liko kaimynu, tai patikrink ji.
                        y = y + 1
                    elif (len(new_device_nei[x]) <= y + 1): # Jei nebeliko kaimynu, tai ...
                        if (len(new_device_nei) > x + 1): # Jei yra kitu irenginiu, tai tikrink juos.
                            x = x + 1
                            y = 0
                            z = 0
                        elif (len(new_device_nei) <= x + 1): # Jei nebeliko irenginiu, tai uzbaik.
                            x = -2
                            y = -2
                            z = -2
                            break
                elif (new_device_nei[x][y] != new_tested[z]): # Jei dar netestuotas, tai ...
                    if (len(new_tested) > z + 1): # Jei dar liko pratestuotu sarase irenginiu, tai perziurek juos.
                        z = z + 1
                    elif (len(new_tested) <= z + 1): # Jei nebeliko pratestuotu sarase irenginiu, tai ieskok nauju kaimynu.
                        ip = new_device_nei[x][y]
                        ip_add = get_ip_add(ip)
                        if (ip_add != ['failed']):
                            port_list = get_id_port(ip)
                            device_list = []
                            port_list1 = []
                            for a in range(0, len(ip_add)):
                                device_list.append(ip_add[a])
                                all_ports_topology.append(port_list[a])
                                port_list1.append(port_list[x])
                            new_device_nei.append(device_list)
                            new_device_nei_ports.append(port_list1)
                            new_tested.append(ip)
                        else:
                            new_tested.append(ip)
                            new_failed.append(ip)
                        if (len(new_device_nei[x]) > y + 1): # Jei dar liko kaimynu, tai patikrink ji.
                            y = y + 1
                        elif (len(new_device_nei[x]) <= y + 1): # Jei nebeliko kaimynu, tai ...
                            if (len(new_device_nei) > x + 1): # Jei yra kitu irenginiu, tai tikrink juos.
                                x = x + 1
                                y = 0
                                z = 0
                            elif (len(new_device_nei) <= x + 1): # Jei nebeliko irenginiu, tai uzbaik.
                                x = -2
                                y = -2
                                z = -2
                                break
    x = 0
    y = 0
    while (x > -1):
        while (y > -1):
            if (new_tested[x] == new_failed[y]):
                del new_tested[x]
                if (len(new_tested) <= x):
                    x = -2
                    y = -2
                    break
                elif (len(new_tested) > x):
                    y = 0
            elif (new_tested[x] != new_failed[y]):
                if (len(new_failed) <= y + 1):
                    if (len(new_tested) <= x + 1):
                        y = -2
                        x = -2
                        break
                    elif (len(new_tested) > x + 1):
                        y = 0
                        x = x + 1
                elif (len(new_failed) > y + 1):
                    y = y + 1

    del new_tested[0]


    if (len(tested) > len(new_tested)):
        x = 0
        while (x > -1):
            if (tested[x] == new_tested[x]):
                if (len(tested) > x + 1):
                    if (len(new_tested) > x + 1):
                        x = x + 1
                    else:
                        print 'IP = ' + str(tested[x]) + ' dingo.'
                        tested = new_tested
                        failed = new_failed
                        device_nei = new_device_nei
                        device_nei_ports = new_device_nei_ports
                        x = -2
                        break
                elif (len(tested) <= x + 1):
                    x = -2
                    break
            elif (tested[x] != new_tested[x]):
                print 'IP = ' + str(tested[x]) + ' dingo.'
                tested = new_tested
                failed = new_failed
                device_nei = new_device_nei
                device_nei_ports = new_device_nei_ports
                x = -2
                break

    elif (len(tested) < len(new_tested)):
        x = 0
        while (x > -1):
            if (tested[x] == new_tested[x]):
                if (len(new_tested) > x + 1):
                    if (len(tested) > x + 1):
                        x = x + 1
                    else:
                        print 'IP = ' + str(new_tested[x+1]) + ' atsirado.'
                        tested = new_tested
                        failed = new_failed
                        device_nei = new_device_nei
                        device_nei_ports = new_device_nei_ports
                        x = -2
                        break
                elif (len(new_tested) <= x + 1):
                    x = -2
                    break
            elif (tested[x] != new_tested[x]):
                print 'IP = ' + str(new_tested[x]) + ' atsirado.'
                tested = new_tested
                failed = new_failed
                device_nei = new_device_nei
                device_nei_ports = new_device_nei_ports
                x = -2
                break
    new_failed = []




    

print failed

print "end"