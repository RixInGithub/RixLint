import time
from sys import argv as argsList
import sys
argsList = list(argsList)
argsList.pop(-1)

class RLRuntime():
	def __init__(self):
		self.start = time.time()

	def elapsed(self):
		timeFloat = time.time()
		return timeFloat - self.start

class Builtins():
	def __init__(self):
		self.runtime = RLRuntime()
		self.debug = "debug.log"
		self.warnCount = 0
		self.errCount = 0
		with open(self.debug, "r") as debugIO:
			self.lintFile = debugIO.read().split("\n")[0].split()[-1].replace("\"", "")
		with open(self.debug, "w") as debugIO:
			print("", end="")
		with open(self.debug, "a") as debugIO:
			debugIO.write("File = \"" + self.lintFile + "\"\nWarns = []\nErrors = []")
		self.lintFileStr = open(self.lintFile, "r").read()

	def warn(self, *msgTuple):
		with open(self.debug, "a") as debugIO:
			debugIO.write("\nWarns.append(\"" + " ".join(msgTuple) + "\")")
		self.warnCount += 1

	def correct(self, *msgTuple):
		with open(self.debug, "a") as debugIO:
			debugIO.write("\nErrors.append(\"" + " ".join(msgTuple) + "\")")
		self.errCount += 1

	def detectToken(self, token):
		return self.lintFileStr.find(token) != -1

	def tokenMentioned(self, token):
		return self.lintFileStr.count(token)

builtins = Builtins()
if builtins.detectToken("print "):
	if sys.version_info[0] > 2: # After Python 2
		count = 0
		while count != builtins.tokenMentioned("print "):
			builtins.correct("Parentheses needed in print function")
			count = count + 1
if builtins.detectToken("print(") and sys.version_info[0] < 3:
	count = 0
	while count != builtins.tokenMentioned("print("):
		builtins.correct("Seperate print function with space instead of parenthesis")
		count = count + 1
