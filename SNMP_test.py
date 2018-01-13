#!/usr/bin/env python

from pysnmp.hlapi import *

ip = '192.168.50.100'
com = 'public'

from pysnmp.hlapi import *

errorIndication, errorStatus, errorIndex, varBinds = next(
    nextCmd(SnmpEngine(),
           CommunityData('public'),
           UdpTransportTarget(('demo.snmplabs.com', 161)),
           ContextData(),
           ObjectType(ObjectIdentity('1.0.8802.1.1.2.1.4.1.1.5')))
)

if errorIndication:
    print(errorIndication)
elif errorStatus:
    print('%s at %s' % (errorStatus.prettyPrint(),
                        errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
else:
    for varBind in varBinds:
        print(' = '.join([x.prettyPrint() for x in varBind]))