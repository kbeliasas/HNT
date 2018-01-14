#!/usr/bin/env python

import time

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
            time.sleep(1)
            print "x = " + str(x)
            print "y = " + str(y)
            print "z = " + str(z)
            if (all_list[x][y] == tested[z]):
                print 0
                if (len(all_list[x]) > y + 1):
                    print 1
                    y = y + 1
                elif (len(all_list[x]) <= y + 1):
                    if (len(all_list) > x + 1):
                        print 2
                        x = x + 1
                        y = 0
                        z = 0
                    elif (len(all_list) <= x + 1):
                        print 3
                        x = -2
                        y = -2
                        z = -2
                        break
            elif (all_list[x][y] != tested[z]):
            	print 4
            	if (len(tested) > z + 1):
            	    print 5
            	    z = z + 1
            	elif (len(tested) <= z + 1):
            	    print 6
            	    ip = all_list[x][y]
            	    ip_add = get_ip_add(ip)
            	    device_list = []
            	    for a in range(0, len(ip_add)):
                        device_list.append(ip_add[a])
                    all_list.append(device_list)
                    tested.append(ip)
                    if (len(all_list[x]) > y + 1):
                        print "len of all_list[x]=" + str(len(all_list[x]))
                        print 7
                        y = y + 1
                    elif (len(all_list[x]) <= y + 1):
                        if (len(all_list) > x + 1):
                            print 8
                            x = x + 1
                            y = 0
                            z = 0
                        elif (len(all_list) <= x + 1):
                            print "len of all_list="+str(len(all_list))
                            print 9
                            x = -2
                            y = -2
                            z = -2
                            break

print tested
print all_list


    
	