#Global
from enum import Enum;
import subprocess;

class Platform(Enum):
	Windows = 1,
	Linux = 2,

#Interface functions
def Execute(args):
	import shlex;
	from PySimLib import Log;
	
	#escape args	
	if(GetPlatform() == Platform.Linux):
		for arg in args:
			arg = shlex.quote(arg);
			
		exitCode = subprocess.call(args, shell = False, stdout=Log.GetTarget(), stderr=Log.GetTarget());
	else:
		raise NotImplementedError("TODO: other platforms");
		
	#call program
	#fullCmdLine = ' '.join(args);
	#ret = subprocess.call(fullCmdLine, shell = False, stdout=Log_GetTarget(), stderr=Log_GetTarget());
	
	return exitCode;
	
def GetExeFileExtension():
	if(GetPlatform() == Platform.Linux):
		return "";
	
	raise NotImplementedError("TODO: other platforms");

	
def GetPlatform():
	import platform;
	
	ident = platform.system();
	if(ident == "Linux"):
		return Platform.Linux;
		
	raise NotImplementedError("TODO: other platforms");
	
def GetUserDirectory():	
	if(GetPlatform() == Platform.Linux):
		from os.path import expanduser;
		
		return expanduser("~");
		
	raise NotImplementedError("TODO: other platforms");
