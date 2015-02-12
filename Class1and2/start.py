#!/usr/bin/env python
import pickle
from snmp_helper import snmp_get_oid_v3, snmp_get_oid, snmp_extract

#OID's##############
SYS_DESCR = '1.3.6.1.2.1.1.1.0'
SYS_NAME = '1.3.6.1.2.1.1.5.0'
# Uptime when running config last changed    
ccmHistoryRunningLastChanged = '1.3.6.1.4.1.9.9.43.1.1.1.0'   
# Uptime when running config last saved (note any 'write' constitutes a save)    
ccmHistoryRunningLastSaved = '1.3.6.1.4.1.9.9.43.1.1.2.0'   
# Uptime when startup config last saved   
ccmHistoryStartupLastChanged = '1.3.6.1.4.1.9.9.43.1.1.3.0'
# sysUptime timestamp 
ccmHistorySYS_Uptime = '1.3.6.1.2.1.1.3.0'
#Router Info
ip_addr = '50.242.94.227'
router1 = (ip_addr, 7961)
router2 = (ip_addr, 8061)

# SNMPv3 Connection Parameters
a_user = 'pysnmp'
auth_key = 'galileo1'
encrypt_key = 'galileo1'
snmp_user = (a_user, auth_key, encrypt_key)

LAST_RUN_CHANGE = int(snmp_extract(snmp_get_oid_v3(router2, snmp_user, ccmHistoryRunningLastChanged)))
print LAST_RUN_CHANGE
pickle.dump( LAST_RUN_CHANGE, open( "rout2.p", "wb" ) )
print "last run saved"
quit()