import subprocess
import os
from com.android.monkeyrunner import MonkeyRunner, MonkeyDevice

# helper: execute a raw command and selectively mute stdout and stderr
def _cmd(cmdlist, mute=1):
	if mute:
		fnull = open(os.devnull, "w")
		proc = subprocess.Popen(cmdlist, stdout = fnull, stderr = fnull)
		proc.communicate()
		fnull.close()
		return (proc.returncode, None)
	else:
		proc = subprocess.Popen(cmdlist, stdout = subprocess.PIPE, 
				stderr = subprocess.PIPE)
		(output, erroutput) = proc.communicate()
		return (proc.returncode, erroutput + output)
	
class MonkeyHelper:
	# call the aapt tool with arbitrary commands
	@staticmethod
	def aapt(cmdlist, mute = True):
		return _cmd(["aapt"] + cmdlist, mute)
	
	# retrieve the package name and main activity name of an apk
	@staticmethod
	def aapt_dump(apk):
		(ret, output) = MonkeyHelper.aapt(['dump','badging',apk], False)
		assert ret == 0, "Failed to retrieve the info of " + apk
		pkg = mainact = None
		for line in output.splitlines():
			if line.startswith('package:'):
				# get the package name
				(_, _, line) = line.partition("name='")
				pkg = line[:line.index("\'")]
			if line.startswith('launchable-activity:'):
				# get the main activity
				(_, _, line) = line.partition("name='")
				mainact = line[:line.index("\'")]
		assert pkg is not None, 'Abnormal pkg:'+apk+'\n'+output
		return (pkg, mainact)

# enhanced MonkeyDevice
class EMonkeyDevice:
	DOWN_AND_UP = MonkeyDevice.DOWN_AND_UP
	DOWN = MonkeyDevice.DOWN
	UP = MonkeyDevice.UP
	def __init__(self):
		self.dev = MonkeyRunner.waitForConnection()
		self.displayWidth = int(self.getProperty("display.width"))
		self.displayHeight = int(self.getProperty("display.height"))
		print "Device attached"
		print "displayWidth = ", self.displayWidth
		print "displayHeight = ", self.displayHeight
	def broadcastIntent(self, uri, action, data, mimetype, extras, component, flags):
		self.dev.broadcastIntent(uri, action, data, mimetype, extras, component, flags)
	def drag(self, start, end, duration, steps):
		self.dev.drag(start, end, duration, steps)
		return self
	def getProperty(self, key):
		return self.dev.getProperty(key)
	def getSystemProperty(self, key):
		return self.dev.getSystemProperty(key)
	def installPackage(self, path):
		self.dev.installPackage(path)
	def instrument(self, className, args):
		return self.dev.instrument(className, args)
	def press(self, name, t = DOWN_AND_UP):
		self.dev.press(name, t)
		return self
	def reboot(self, into = "None"):
		self.dev.reboot(into)
	def rebootBootloader(self):
		self.dev.reboot("bootloader")
	def rebootRecovery(self):
		self.dev.reboot("Recovery")
	def removePackage(self, package):
		self.dev.removePackage(package)
	def shell(self, cmd):
		return self.dev.shell(cmd)
	def startActivity(self, uri, action, data, mimetype, extras, component, flags):
		self.dev.startActivity(uri, action, data, mimetype, extras, component, flags)
	def takeSnapshot(self):
		return self.dev.takeSnapshot()
	def touch(self, x, y, t = DOWN_AND_UP):
		self.dev.touch(x, y, t)
		return self
	def type(self, message):
		self.dev.type(message)
		return self
	def wake(self):
		self.dev.wake()
		return self
	def slideLeft(self):
		h = self.displayHeight / 2
		w1 = self.displayWidth * 7 / 8
		w2 = self.displayHeight * 3 / 8
		self.dev.drag ((w1, h), (w2, h), 0.05, 100)
		return self
	def slideRight(self):
		h = self.displayHeight / 2
		w1 = self.displayWidth * 3 / 8
		w2 = self.displayHeight * 7 / 8
		self.dev.drag ((w1, h), (w2, h), 0.05, 100)
		return self
	def unlockScreen(self):
		h = self.displayHeight * 6 / 7
		self.dev.drag((self.displayWidth / 2, h), (self.displayWidth, h), 0.05, 100)
		return self
	def sleep(self, seconds):
		MonkeyRunner.sleep(seconds)
		return self
	def getInstalledPackage(self):
		raw = str(self.shell("pm list packages"))
		l = []
		for line in raw.split('\n'):
			if line.startswith("package:"):
				l.append(line[8:].rstrip())
		return l
	def killAllBgApps(self):
		self.shell("am kill-all")
	def pushFile(self, path):
		#return self.shell("push " + path)
		pass
	def pullFile(self, devicePath, localPath):
		# return self.shell("pull %s %s" % (devicePath, localPath))
		pass
	def getSystemInfo(self):
		d = {"android_version": self.getProperty("build.version.release")}
		return d
	