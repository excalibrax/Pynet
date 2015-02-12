#!/usr/bin/env python
import pickle
from snmp_helper import snmp_get_oid_v3, snmp_extract

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
ip_addr = '*************'
router1 = (ip_addr, 7961)
router2 = (ip_addr, 8061)

	
def send_mail(subject, message):
	'''
	Simple function to help simplify sending SMTP email
	Assumes a mailserver is available on localhost
	'''
	sender = '*************'
	recipient = '*************'
	import smtplib
	from email.mime.text import MIMEText


	message = MIMEText(message)
	message['Subject'] = subject
	message['From'] = sender
	message['To'] = recipient

	# Create SMTP connection object to localhost
	smtp_conn = smtplib.SMTP('localhost')

	# Send the email
	smtp_conn.sendmail(sender, recipient, message.as_string())

	# Close SMTP connection
	smtp_conn.quit()


	return True

def main():
	
	# SNMPv3 Connection Parameters
	a_user = '*************'
	auth_key = '*************'
	encrypt_key = '*************'
	snmp_user = (a_user, auth_key, encrypt_key)

	if (pickle.load( open( "rout2.p", "rb" ) )):
		LAST_RUN_CHANGE = pickle.load( open( "rout2.p", "rb" ) )

	else:
		LAST_RUN_CHANGE = int(snmp_extract(snmp_get_oid_v3(router2, snmp_user, ccmHistoryRunningLastChanged)))
		pickle.dump( LAST_RUN_CHANGE, open( "rout2.p", "wb" ) )
		print "last run saved"
		quit()

	NEW_RUN_CHANGE = snmp_extract(snmp_get_oid_v3(router2, snmp_user, ccmHistoryRunningLastChanged))
		
	if NEW_RUN_CHANGE > LAST_RUN_CHANGE:
		print "Running config changed"
		subject = 'Test message'
		message = '''

		The running config has changed.
		Regards,

		Sean
		'''

		send_mail(subject, message)
	
	
if __name__ == '__main__':

	main()

