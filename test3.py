#!/usr/bin/env python

from ncclient import manager

host = "192.168.50.6"
user = "admin"
password = "cisco"


with manager.connect(host=host, port=22, username=user, password=password, hostkey_verify=False, allow_agent=False, look_for_keys=False) as m:
    try:
        print "pavyko"
        a = m.get()
        a.close()
    except Exception as e:
        print e