#!/usr/bin/env python

import netsnmp

# ip = '192.168.226.152' # Pirmas irenginys
ip = '192.168.50.100'

def get_ip_add(ip): # Pasiima kaimynus is irenginio.
    oid = netsnmp.VarList(netsnmp.Varbind('.1.3.6.1.4.1.9.9.23.1.2.1.1.4'))
    res = netsnmp.snmpwalk(oid, Version = 2, DestHost=ip, Community='public')
    return res

tested = []


ip_add = get_ip_add(ip)
device_list = []
for x in range(0, len(ip_add)):
    device_list.append(ip_add[x])
all_list = [device_list]
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
                    device_list = []
                    for a in range(0, len(ip_add)):
                        device_list.append(ip_add[a])
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



print tested
print device_list

print "end"