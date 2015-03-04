#!/usr/bin/env python
'''
Using Arista's eapilib, create a script that allows you to add a VLAN 
(both the VLAN ID and the VLAN name).  
Your script should first check that the VLAN ID is available and only add 
the VLAN if it doesn't already exist.  
Use VLAN IDs between 100 and 999.  You should be able to call the script from the command 
line as follows:
   python eapi_vlan.py --name blue 100     # add VLAN100, name blue

If you call the script with the --remove option, the VLAN will be removed.
   python eapi_vlan.py --remove 100          # remove VLAN100

Once again only remove the VLAN if it exists on the switch.  You will probably want to use Python's argparse to accomplish the argument processing.
'''

import eapilib
import jsonrpclib
import argparse
from pprint import pprint

login_dict = dict(

  )
eapi_conn = eapilib.create_connection(**login_dict)

def check_vlan(vlan_id):
    #check if Vlan exsists if not return name
    try:
        output= run_commands(['show vlan {}'.format(vlan_id)])
        output = output[0]['vlans']
        return output[vlan_id]['name']
    except:
        pass
    return False

def config_commands(commands):
     #run config commands from string
     eapi_conn.config(commands)

def run_commands(commands):
    #run commands from string
    output= eapi_conn.run_commands(commands)
    return output

def main():
    #gather data from parse    
    parser = argparse.ArgumentParser(description='add or remove Vlans from predefined switch')
    parser.add_argument("vlan_num", help="VLAN ID", type=int, action="store")
    parser.add_argument("--name", help="VLAN name", action="store", dest="vlan_name", type=str)
    parser.add_argument("--remove", help="Remove the given VLAn ID", action="store_true")

    values=parser.parse_args()
    vlan_id = str(values.vlan_num)
    remove = values.remove
    vlan_name = values.vlan_name

    #Check if Vlan exists if does return name
    vlan_exists=check_vlan(vlan_id)
    
    #Check if commmand remove was used, if so remove vlan if it exists
    if remove:
        if vlan_exists: 
            print "vlan " + vlan_id + " name: " + str(vlan_exists) + " exists, removing it."
            config_commands(['no vlan ' + vlan_id])
        else:
            print "VLAN " + vlan_id + " does not exist"
    else:
        if vlan_exists == vlan_name:
           print "Vlan " + vlan_id + ": " + vlan_name + " already exists, no action taken"
        elif vlan_exists and vlan_name:
           print "Vlan " + vlan_id + " exists, changing name to: " + vlan_name
           commands=['vlan ' + vlan_id]
           commands.append('name ' + vlan_name)
           config_commands(commands)
        elif vlan_name:
           print "Adding Vlan " + vlan_id + ": " + vlan_name + " to the device"
           commands=['vlan ' + vlan_id]
           commands.append('name ' + vlan_name)
           config_commands(commands)
        else:
           print "Adding Vlan " + vlan_id + " to the device"
           config_commands(['vlan ' + vlan_id])

    

if __name__ == "__main__":

   main()
