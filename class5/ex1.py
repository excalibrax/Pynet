#!/usr/bin/env python
'''
Use Arista's eAPI to obtain 'show interfaces' from the switch.  Parse the 'show interfaces' 
output to obtain the 'inOctets' and 'outOctets' fields for each of the interfaces on the switch.  
Accomplish this directly using jsonrpclib.
'''

import jsonrpclib
import eapilib


login_dict = dict(

  )
  
conn_url = 'https://{username}:{password}@{ip}:{port}/command-api'.format(**login_dict)
connection=jsonrpclib.Server(conn_url)
connection

interfaces = connection.runCmds(1, ["show interfaces"])


interfaces = interfaces[0]['interfaces']
keys = interfaces.keys()

for keys in interfaces:
    counters = interfaces[keys].get(u'interfaceCounters', '0')
    if hasattr(counters, 'get'): 
       print keys, "inOctets:", counters.get(u'inOctets', '0'), "outOctets:", counters.get(u'outOctets', '0')

