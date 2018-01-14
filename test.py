#!/usr/bin/env python

import time
import networkx as nx
import matplotlib.pyplot as plt

def get_ip_add(ip):
    if ip == 'A':
        res = ['B', 'C']
    elif ip == 'B':
        res = ['A', 'C']
    elif ip == 'C':
        res = ['A', 'B', 'D']
    elif ip == 'D':
        res = ['C']
    return res

def draw_topology(realations, labels=None, graph_layout='shell',
               node_size=1600, node_color='blue', node_alpha=0.3,
               node_text_size=12,
               edge_color='blue', edge_alpha=0.3, edge_tickness=1,
               edge_text_pos=0.3,
               text_font='sans-serif'):
    G=nx.Graph()

    for edge in realations:
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


ip = 'A'

ip_add = get_ip_add(ip)

device_list = []

for x in range(0, len(ip_add)):
    device_list.append(ip_add[x])

all_list = [device_list]

tested = []
tested.append(ip)


x = 0
y = 0
z = 0
while (x > -1):
    while (y > -1):
        while (z > -1):
            print "x = " + str(x)
            print "y = " + str(y)
            print "z = " + str(z)
            if (all_list[x][y] == tested[z]):
                if (len(all_list[x]) > y + 1):
                    y = y + 1
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
                    ip_add = get_ip_add(ip)
                    device_list = []
                    for a in range(0, len(ip_add)):
                        device_list.append(ip_add[a])
                    all_list.append(device_list)
                    tested.append(ip)
                    if (len(all_list[x]) > y + 1):
                        print "len of all_list[x]=" + str(len(all_list[x]))
                        y = y + 1
                    elif (len(all_list[x]) <= y + 1):
                        if (len(all_list) > x + 1):
                            x = x + 1
                            y = 0
                            z = 0
                        elif (len(all_list) <= x + 1):
                            print "len of all_list="+str(len(all_list))
                            x = -2
                            y = -2
                            z = -2
                            break

realations = []

for x in range(0, len(tested)):
    for y in range(0, len(all_list[x])):
        temp = (tested[x], all_list[x][y])
        realations.append(temp)

print realations


print tested
print all_list