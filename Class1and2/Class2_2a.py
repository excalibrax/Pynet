#!/usr/bin/env python
#CLass 2 exercise 2

import pygal
import time
from snmp_helper import snmp_get_oid_v3, snmp_extract

#Router Info
pynet_rtr1 = ('*******', 7961)

# SNMPv3 Connection Parameters
a_user = '*******'
auth_key = '*******'
encrypt_key = '*******'
snmp_user = (a_user, auth_key, encrypt_key)

snmp_oids = {
	'sysName':'1.3.6.1.2.1.1.5.0',
	'sysUptime':'1.3.6.1.2.1.1.3.0',
	'ifDescr_fa4':'1.3.6.1.2.1.2.2.1.2.5',
	'ifInOctets_fa4':'1.3.6.1.2.1.2.2.1.10.5',
	'ifInUcastPkts_fa4':'1.3.6.1.2.1.2.2.1.11.5',
	'ifOutOctets_fa4':'1.3.6.1.2.1.2.2.1.16.5',
	'ifOutUcastPkts_fa4':'1.3.6.1.2.1.2.2.1.17.5',
	}

#retrieve OID data
def oid_data(device, oid):
	snmp_data = snmp_get_oid_v3(pynet_rtr1, snmp_user, oid)
	return int(snmp_extract(snmp_data))

def makeChart(dictOfListsToGraph, timeIncrement, title, fileName):
	'''
	Given a dictionary of lists with graph values, the time increment over which the values
	were gathered, the title of the graph and the fileName, generate a line graph of the values using
	the dictionary keys as Titles for each line.
	'''
	line_chart = pygal.Line()
	line_chart.title = title
	longest = 0
	for anItem in dictOfListsToGraph:
		if len(dictOfListsToGraph[anItem]) > longest:
			longest = len(dictOfListsToGraph[anItem])
	longest *= timeIncrement
	longest += 5
	labelRange = range(int(timeIncrement), longest, int(timeIncrement))
	labelRange = map(str, labelRange)
	line_chart.x_labels = labelRange
	for anItem in dictOfListsToGraph:
		line_chart.add(anItem, dictOfListsToGraph[anItem])
	line_chart.render_to_file(fileName)
	
	
def main():
	graph_stats = {
	"in_octets": [],
	"out_octets": [],
	"in_ucast_pkts": [],
	"out_ucast_pkts": [],
	}
	#Byte dictionary
	bytesDict = dict()
	pktsDict = dict()
	bytesDict["Bytes In"] = list()
	bytesDict["Bytes Out"] = list()
	pktsDict["Packets In"] = list()
	pktsDict["Packets Out"] = list()

		
	# Enter a loop gathering SNMP data every 5 minutes for an hour.
	for time_track in range(0, 65, 5):
		time_track = 60
		print "\n%20s %-60s" % ("time", time_track)

		bytesDict["Bytes In"].append(oid_data(pynet_rtr1, oid=snmp_oids['ifInOctets_fa4']))
		bytesDict["Bytes Out"].append(oid_data(pynet_rtr1, oid=snmp_oids['ifInOctets_fa4']))
		pktsDict["Packets In"].append(oid_data(pynet_rtr1, oid=snmp_oids['ifInOctets_fa4']))
		pktsDict["Packets Out"].append(oid_data(pynet_rtr1, oid=snmp_oids['ifInOctets_fa4']))

		time.sleep(300)
	
if __name__ == '__main__':

	main()
	makeChart(bytesDict, 300, "Input/Output Bytes", "bytes.svg")
	makeChart(pktsDict, 300, "Input/Output Packets", "pkts.svg")

