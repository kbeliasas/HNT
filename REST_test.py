#!/usr/bin/env python

import httplib2
import json

h = httplib2.Http(".cache")
h.add_credentials('admin', 'admin')
resp, content = h.request('http://192.168.50.254:8181/restconf/config/opendaylight-inventory:nodes', "GET")

print "resp"
print resp
print "content"
print content