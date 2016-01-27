#Global
from enum import Enum;
import os;
import subprocess;

class Platform(Enum):
	Windows = 1,
	Linux = 2,

#Interface functions
def Execute(args, blocking = True):
	import shlex;
	from PySimLib import Log;
	
	#escape args
	for arg in args:
		arg = shlex.quote(arg);
		
	#execute
	if(blocking):
		exitCode = subprocess.call(args, shell = False, stdout=Log.GetTarget(), stderr=Log.GetTarget());
	else:
		subprocess.Popen(args, shell = False, stdout=Log.GetTarget(), stderr=Log.GetTarget());
		exitCode = None;
		
	#call program
	#fullCmdLine = ' '.join(args);
	#ret = subprocess.call(fullCmdLine, shell = False, stdout=Log_GetTarget(), stderr=Log_GetTarget());
	
	return exitCode;
	
def GetConfigDirectory():
	if(GetPlatform() == Platform.Windows):
		return os.environ['LOCALAPPDATA'];
		
	if(GetPlatform() == Platform.Linux):
		return GetUserDirectory() + "/.config";
		
	raise NotImplementedError("TODO: other platforms");
	
def GetExeFileExtension():
	if(GetPlatform() == Platform.Windows):
		return ".exe";
		
	if(GetPlatform() == Platform.Linux):
		return "";
	
	raise NotImplementedError("TODO: other platforms");

	
def GetPlatform():
	import platform;
	
	ident = platform.system();
	if(ident == "Windows"):
		return Platform.Windows;
		
	if(ident == "Linux"):
		return Platform.Linux;
		
	raise NotImplementedError("PySimLib is not implemented on the currently running platform, which is '" + ident + "'. Contact us for help.");
	
def GetUserDirectory():	
	if(GetPlatform() == Platform.Linux):
		from os.path import expanduser;
		
		return expanduser("~");
		
	raise NotImplementedError("TODO: other platforms");