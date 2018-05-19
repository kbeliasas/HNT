#!/usr/bin/env python

import sys
import logging
from ncclient import manager

log = logging.getLogger(__name__)

host = "192.168.50.6"
user = "admin"
password = "cisco"


ADD_MAC_ADDRESS = """
<config>
        <cli-config-data>
            <cmd>mac address-table static %s vlan %s interface %s</cmd>
        </cli-config-data>
</config>
"""

REMOVE_MAC_ADDRESS = """
<config>
        <cli-config-data>
            <cmd>no mac address-table static %s vlan %s interface %s</cmd>
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

def add_mac(host, user, password, mac, vlan, interface):
    with manager.connect(host=host, port=22, username=user, password=password, hostkey_verify=False, allow_agent=False, look_for_keys=False) as m:
        try:
            confstr = ADD_MAC_ADDRESS % (mac, vlan, interface)
            rpc_obj = m.edit_config(target='running', config=confstr)
            _check_response(rpc_obj, 'ADD_MAC_ADDRESS')
        except Exception:
            log.exception("Exception in adding %s mac %s vlan interface %s" % (mac, vlan, interface))

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    add_mac(host,user,password, "1111.1111.1111", "500", "gigabitEthernet0/27")

