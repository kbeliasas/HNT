#!/usr/bin/env python

import easysnmp

# ip = '192.168.226.152' # Pirmas irenginys
ip = '192.168.50.100'
com = 'public'

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
        ans.append('')
        return ans

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