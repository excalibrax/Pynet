#!/usr/bin/env python
'''
Using the onepk_helper library establish a onePK connection to one of the two lab routers.  From this lab router obtain the product_id and SerialNo:

>>> rtr1_obj.net_element.properties.product_id
'CISCO881-SEC-K9'
>>> rtr1_obj.net_element.properties.SerialNo
'FTX1000008X'
'''

from onepk_helper import NetworkDevice

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
      
    rtr1_obj = NetworkDevice(**pynet_rtr1)
    rtr1_obj.establish_session()
    print "\nConnection established to: {}".format(rtr1_obj.net_element.properties.sys_name)
    print "Router 1 product ID:" + rtr1_obj.net_element.properties.product_id
    print "Router 1 serial no:" + rtr1_obj.net_element.properties.SerialNo
    rtr1_obj.disconnect()
    
    rtr2_obj = NetworkDevice(**pynet_rtr2)
    rtr2_obj.establish_session()
    print "\nConnection established to: {}".format(rtr2_obj.net_element.properties.sys_name)
    print "Router 2 product ID:" + rtr2_obj.net_element.properties.product_id
    print "Router 2 serial no:" + rtr2_obj.net_element.properties.SerialNo
    rtr2_obj.disconnect()

if __name__ == "__main__":
    main()