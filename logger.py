import subprocess as sp
import time
import datetime

def logDiff(f, previous, current):
	f.write(str(time.time()) + ':\n')
	#out
	tmp = list(previous.difference(current))
	for mac in tmp:
		f.write("< " + mac + "\n")
	#in
	tmp = list(current.difference(previous))
	for mac in tmp:
		f.write("> " + mac + "\n")
	f.flush()

def getList(command):
	res = sp.check_output(command).split('\n')[2:-4]
	return [x.split()[2] for x in res if "MAC Address:" in x]

command = ["nmap", "-sP", "192.168.1.0/24"]
logfile = open("log" + str(datetime.datetime.now()).split('.')[0] + ".txt", 'w')
macs = set(getList(command))
timestep = 30

try:
	while True:
		start = int(time.time())
		news = set(getList(command))
		logDiff(logfile, macs, news)
		macs = news
		elapsed = int(time.time()) - start
		if (elapsed < timestep):
			time.sleep(timestep - elapsed)
except KeyboardInterrupt:
	print "Process stopped"
	logfile.close()
