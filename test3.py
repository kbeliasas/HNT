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
            <cmd>username %s privilege 15 secret %s</cmd>
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

def create_access_vlan(host, user, password, username, password1):
    with manager.connect(host=host, port=22, username=user, password=password, hostkey_verify=False, allow_agent=False, look_for_keys=False) as m:
        try:
            confstr = ACCESS_VLAN % (username, password1)
            rpc_obj = m.edit_config(target='running', config=confstr)
            _check_response(rpc_obj, 'ACCESS_VLAN')
        except Exception:
            log.exception("Exception in creating access port in %s for %s vlan" % (username, password1))

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    create_access_vlan(host,user,password, "test", 'test')

