import subprocess as sp
import time
import datetime
import os

def logDiff(f, previous, current):
	f.write("@" + str(time.time()) + ':\n')
	#out
	tmp = list(previous.difference(current))
	for mac in tmp:
		f.write("< " + mac + "\n")
	#in
	tmp = list(current.difference(previous))
	for mac in tmp:
		f.write("> " + mac + "\n")
	f.flush()

def logFull(f, current):
	f.write("@" + str(time.time()) + ':\n')
	for mac in current:
		f.write(mac + '\n')
	f.flush()

def logDevs(f, previous, devices):
	for key in devices:
		if not (key in previous):
			f.write(key + ' ' + devices[key] + '\n')
	f.flush()

def getDevs(command):
	print "Nmap -> " + str(datetime.datetime.now()).split('.')[0]
	res = sp.check_output(command).split('\n')[2:-4]
	tmp = dict()
	for dev in res:
		if "MAC Address:" in dev:
			tmp[dev.split()[2]] = dev[dev.index('(') + 1:-1]
	print "OK"
	return tmp

if os.getuid() != 0:
	print "Error: You must run this script as root"
	exit()

command = ["nmap", "-sP", "192.168.1.0/24"]
timestamp = str(datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
fname = "log" + timestamp + ".txt"
fdevs = "devices" + timestamp + ".txt"
logfile = open(fname, 'w')
devfile = open(fdevs, 'w')
logger = logFull
print "Started logging on: " + fname
macs = dict()
timestep = 60

try:
	while True:
		start = int(time.time())
		news = getDevs(command)
		#logDiff(logfile, macs, news)
		logger(logfile, news)
		logDevs(devfile, macs, news)
		macs.update(news)
		elapsed = int(time.time()) - start
		if (elapsed < timestep):
			print "Sleeping for " + str(timestep - elapsed) + "s ..."
			time.sleep(timestep - elapsed)
except KeyboardInterrupt:
	print "Process stopped"
	logfile.close()
	devfile.close()
