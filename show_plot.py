import sys
import os
import matplotlib.pyplot as plt
import matplotlib
import datetime

class Device:
	index = 0
	def __init__(self, name="unknown"):
		self.ID = Device.index
		Device.index += 1
		self.name = name

def plotAt(hour, devices, lst):
	for dev in lst:
		date = matplotlib.dates.date2num(datetime.datetime.fromtimestamp(hour))
		plt.plot_date(date, devices[dev].ID, 'ro')

devices = dict()
timelst = list()

if len(sys.argv) == 2 or len(sys.argv) == 3:
	filename = sys.argv[1]
	try:
		logfile = open(filename, 'r')
	except:
		print "file error"
		exit()
	if len(sys.argv) == 3:
		devfname = sys.argv[2]
	else:
		devfname = filename.replace("log", "devices")
else:
	print "wrong arguments"
	exit()


if os.path.isfile(devfname):
	devfile = open(devfname, 'r')
	for line in devfile:
		line = line.split(' ', 1)
		devices[line[0]] = Device(line[1])

tick = 0
tickdevs = list()
for line in logfile:
	if ('@' in line):
		if tick > 0:
			plotAt(timelst[tick - 1], devices, tickdevs)
		tickdevs = list()
		timelst.append(int(float(line[1:-2])))
		tick += 1
	else:
		line = line[:-1]
		if not(line in devices):
			print line
			devices[line] = Device(line)
		tickdevs.append(line)

order = range(len(devices))
for key in devices:
	dev = devices[key]
	order[dev.ID] = dev.name

plt.yticks(range(len(order)), order)
plt.show()
