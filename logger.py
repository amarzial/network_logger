import subprocess as sp
import time
import datetime

logfile = open("log" + str(datetime.datetime.now()).split('.')[0] + ".txt", 'w')

try:
	while True:
		lst = sp.check_output(["arp-scan", "-l"])
		logfile.write("time: " + str(time.time()) + '\n')
		for line in lst.split('\n')[2:-4]:
			logfile.write(line + '\n')
		time.sleep(5)
except KeyboardInterrupt:
	print "Process stopped"
	logfile.close()
