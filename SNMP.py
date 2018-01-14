#!/usr/bin/env python

import easysnmp
import networkx as nx
import matplotlib.pyplot as plt

# ip = '192.168.226.152' # Pirmas irenginys
ip = '192.168.50.100'
com = 'public'
failed = []

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
        failed.append(ip)
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

def draw_topology(graph, labels=None, graph_layout='spectral',
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


tested = []
tested_names = []


ip_add = get_ip_add(ip)
port_list = get_id_port(ip)
device_list = []
all_ports = []
for x in range(0, len(ip_add)):
    device_list.append(ip_add[x])
    all_ports.append(port_list[x])
all_list = [device_list]
tested.append(ip)
tested_names



x = 0
y = 0
z = 0

while (x > -1):
    while (y > -1):
        while (z > -1):
            #print "x = " + str(x)
            #print "y = " + str(y)
            #print "z = " + str(z)
            if (all_list[x][y] == tested[z]): # Jei jau testuotas, tai ...
                if (len(all_list[x]) > y + 1): # Jei dar liko kaimynu, tai patikrink ji.
                    y = y + 1
                elif (len(all_list[x]) <= y + 1): # Jei nebeliko kaimynu, tai ...
                    if (len(all_list) > x + 1): # Jei yra kitu irenginiu, tai tikrink juos.
                        x = x + 1
                        y = 0
                        z = 0
                    elif (len(all_list) <= x + 1): # Jei nebeliko irenginiu, tai uzbaik.
                        x = -2
                        y = -2
                        z = -2
                        break
            elif (all_list[x][y] != tested[z]): # Jei dar netestuotas, tai ...
                if (len(tested) > z + 1): # Jei dar liko pratestuotu sarase irenginiu, tai perziurek juos.
                    z = z + 1
                elif (len(tested) <= z + 1): # Jei nebeliko pratestuotu sarase irenginiu, tai ieskok nauju kaimynu.
                    ip = all_list[x][y]
                    ip_add = get_ip_add(ip)
                    if (ip_add != ['failed']):
                        port_list = get_id_port(ip)
                        device_list = []
                        for a in range(0, len(ip_add)):
                            device_list.append(ip_add[a])
                            all_ports.append(port_list[a])
                        all_list.append(device_list)
                        tested.append(ip)
                    if (len(all_list[x]) > y + 1): # Jei dar liko kaimynu, tai patikrink ji.
                        y = y + 1
                    elif (len(all_list[x]) <= y + 1): # Jei nebeliko kaimynu, tai ...
                        if (len(all_list) > x + 1): # Jei yra kitu irenginiu, tai tikrink juos.
                            x = x + 1
                            y = 0
                            z = 0
                        elif (len(all_list) <= x + 1): # Jei nebeliko irenginiu, tai uzbaik.
                            x = -2
                            y = -2
                            z = -2
                            break

realations = []


for x in range(0, len(tested)):
    for y in range(0, len(all_list[x])):
        temp = (tested[x], all_list[x][y])
        realations.append(temp)

draw_topology(realations,all_ports)

print failed

print "end"