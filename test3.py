#!/usr/bin/env python

from ncclient import manager

host = "192.168.50.6"
user = "admin"
password = "cisco"


with manager.connect(host=host, port=22, username=user, password=password, hostkey_verify=False, allow_agent=False, look_for_keys=False) as m:
    c = m.get_config(source='running').data_xml
    with open("%s.xml" % host, 'w') as f:
        f.write(c)