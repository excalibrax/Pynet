#!/usr/bin/env python
'''
Applied Python Course, Class1, Exercise 3
Note, you will need to update the IP and COMMUNITY_STRING to use this script.
'''

from snmp_helper import snmp_get_oid, snmp_extract

#OID's##############
SYS_DESCR = '1.3.6.1.2.1.1.1.0'
SYS_NAME = '1.3.6.1.2.1.1.5.0'
# Uptime when running config last changed    
ccmHistoryRunningLastChanged = '1.3.6.1.4.1.9.9.43.1.1.1.0'   
# Uptime when running config last saved (note any 'write' constitutes a save)    
ccmHistoryRunningLastSaved = '1.3.6.1.4.1.9.9.43.1.1.2.0'   
# Uptime when startup config last saved   
ccmHistoryStartupLastChanged = '1.3.6.1.4.1.9.9.43.1.1.3.0'

def determine_run_start_sync_state(run_change_sysuptime, start_save_sysuptime):
	# No 'wr mem' since last reload
	if start_save_sysuptime == 0:
		return False
		
	elif start_save_sysuptime >= run_change_sysuptime:
		return True
		
	return False
	
def convert_uptime_hours(sys_uptime):
	'''
	sys_uptime is in hundredths of seconds
	returns a float
	'''
	return int(sys_uptime) / 100.0 / 3600.0
	
def main():
	from snmp_helper import snmp_get_oid, snmp_extract
	COMMUNITY_STRING = '*************'
	ip_addr = '*************'

	# Router Info
	devices = {
	"pynet_rtr1": (ip_addr, COMMUNITY_STRING, 7961),
	"pynet_rtr2": (ip_addr, COMMUNITY_STRING, 8061),
	}

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
	'''
	Part 2
	for a_device in (pynet_rtr1, pynet_rtr2):
		print "****************"
		for the_oid in (SYS_NAME, SYS_DESCR):
			snmp_data = snmp_helper.snmp_get_oid(a_device, oid=the_oid)
			output = snmp_helper.snmp_extract(snmp_data)
		print output
	print 	"*********************"
	print
	'''
	#Part 3a
	 # Gather data from device
	for device_name, snmp_device in devices.items():
		# Gather data from device
		snmp_data = snmp_get_oid(snmp_device, oid=ccmHistorySYS_Uptime)
		sys_uptime = snmp_extract(snmp_data)
		
		uptime_hours = convert_uptime_hours(sys_uptime)
		 
		snmp_data = snmp_get_oid(snmp_device, oid=ccmHistoryRunningLastChanged)
		last_run_change = int(snmp_extract(snmp_data))

		snmp_data = snmp_get_oid(snmp_device, oid=ccmHistoryStartupLastChanged)
		last_start_save = int(snmp_extract(snmp_data))
		
		# Determine whether run-start are in sync
		run_save_status = determine_run_start_sync_state(last_run_change, last_start_save)
		
		# Display output
		print "\nDevice = %s" % device_name
		print "Current Uptime = %.1f hours" % uptime_hours
		# Check for a reboot and no save
		if not last_start_save:
			print 'This device has never been saved since the last reboot'
		else:
			if run_save_status:
				print 'Running config has been saved'
			else:
				print 'Running config not saved'
		print


if __name__ == '__main__':

	main()