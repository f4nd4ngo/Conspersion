"""Vincent Boucher 2015-01-07- Python  
Script to connect to multiple switches, add a specific command and logout."""
import os
import sys
import pexpect
import subprocess

#Switch username
switch_un = "admin"
#Switch password
switch_pw = "password"
	
#Function that will be called to send commands to the switch
def http_secure_server(ip):
	try:
		child = pexpect.spawn('ssh -o StrictHostKeyChecking=no %s@%s' % (switch_un, ip))
		child.logfile = sys.stdout
		child.timeout = 60
		i = child.expect(['Password:',pexpect.TIMEOUT,pexpect.EOF,'Connection refused','Connection timed out','Connection refused by server'],timeout=120)
		if i == 0:
			child.sendline(switch_pw)
			child.expect('#')
			#child.sendline('conf t')
			#child.expect('\(config\)#')
			#child.sendline('ip http secure-server')
			#child.expect('#')
			child.sendline('end')
			child.expect('#')
			#child.sendline('wr mem')
			#child.expect('[OK]')
			#child.expect('#')
			child.sendline('quit')
			sys.exit
		elif i == 1:
			print ('Timeout')
			sys.exit
		elif i == 2:
			print ('Reached EOF')
			sys.exit         		
		elif i == 3:
			print ('Connection refused')
			sys.exit
		elif i == 4:
			print ('Connection timed out')
			sys.exit
		elif i == 5:
			print ('Connection refused by server')
			sys.exit
	except:
		raise
		
#For loop that will loop through switches in a specific range with the function http_secure_server	
with open(os.devnull, "wb") as limbo:
        for n in xrange(7, 15):
                ip="10.23.30.{0}".format(n)
                result=subprocess.Popen(["ping", "-c", "1", "-n", "-W", "2", ip],
                        stdout=limbo, stderr=limbo).wait()
                if result:
                        print ip, "inactive"
                else:
                        http_secure_server(ip)
		
