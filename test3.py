#!/usr/bin/env python

from ncclient import manager

host = 192.168.50.5

with manager.connect(host=host, port=830, username=user, hostkey_verify=False) as m:
    c = m.get_config(source='running').data_xml
    with open("%s.xml" % host, 'w') as f:
        f.write(c)