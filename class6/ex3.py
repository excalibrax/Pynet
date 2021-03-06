#!/usr/bin/env python
'''
Using the onepk_helper library establish a onePK connection to one of the two lab routers.  From this lab router obtain the product_id and SerialNo:

>>> rtr1_obj.net_element.properties.product_id
'CISCO881-SEC-K9'
>>> rtr1_obj.net_element.properties.SerialNo
'FTX1000008X'
'''

from onepk_helper import NetworkDevice
from onep.interfaces import NetworkInterface, InterfaceFilter
from pprint import pprint
from onep.vty import VtyService

def main():
    pynet_rtr1 = dict(
        ip='50.242.94.227',
        username='pyclass',
        password='88newclass',
        pin_file='pynet-rtr1-pin.txt',
        port=15002
      )
    
    pynet_rtr2 = dict(
        ip='50.242.94.227',
        username='pyclass',
        password='88newclass',
        pin_file='pynet-rtr2-pin.txt',
        port=8002
      )
      

    for a_rtr in (pynet_rtr1, pynet_rtr2):
        rtr_obj = NetworkDevice(**a_rtr)
        rtr_obj.establish_session()
        
        vty_service = VtyService(rtr_obj.net_element)
        vty_service.open()
        
        router_name = rtr_name = rtr_obj.net_element.properties.sys_name
        
        cmd = "show version"
        cli = vty_service.write(cmd)

        print rtr_name
        print cli


        
        
        rtr_obj.disconnect()
    

if __name__ == "__main__":
    main()