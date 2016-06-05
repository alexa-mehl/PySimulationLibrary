#Global
import os;

#External
def GetTarget():
	global __target;
	
	return __target;
	
def Append(string):
	global __target;
	
	__target.write(string);
	
def Line(string):
	Append(string);
	Append("\r\n");
	
def SetTarget(target):
	global __target;
	
	__target = target;

#Internals
__target = open(os.devnull, 'w'); #default to not create a log
