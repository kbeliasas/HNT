#!/usr/bin/env python

import sys
import logging
from ncclient import manager

log = logging.getLogger(__name__)

host = "192.168.50.6"
user = "admin"
password = "cisco"


ACCESS_VLAN = """
<config>
        <cli-config-data>
            <cmd>interface %s</cmd>
            <cmd>switchport mode access</cmd>
            <cmd>switchport access vlan %s</cmd>
        </cli-config-data>
</config>
"""

def _check_response(rpc_obj, snippet_name):
    log.debug("RPCReply for %s is %s" % (snippet_name, rpc_obj.xml))
    xml_str = rpc_obj.xml
    if "<ok />" in xml_str:
        log.info("%s successful" % snippet_name)
    else:
        log.error("Cannot successfully execute: %s" % snippet_name)

def create_access_vlan(host, user, password, interface, vlan):
    with manager.connect(host=host, port=22, username=user, password=password, hostkey_verify=False, allow_agent=False, look_for_keys=False) as m:
        try:
            confstr = ACCESS_VLAN % (interface, vlan)
            rpc_obj = m.edit_config(target='running', config=confstr)
            _check_response(rpc_obj, 'ACCESS_VLAN')
        except Exception:
            log.exception("Exception in creating access port in %s for %s vlan" % (interface, vlan))

create_access_vlan(host,user,password, "interface GigabitEthernet0/28", '500')

