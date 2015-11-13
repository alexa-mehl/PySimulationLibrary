from enum import Enum;

class Platform(Enum):
	Windows = 1,
	Linux = 2,
	
def GetPlatform():
	import platform;
	
	ident = platform.system();
	if(ident == "Linux"):
		return Platform.Linux;
		
	raise NotImplemented("TODO: other platforms");
	
def GetUserDirectory():
	from os.path import expanduser;
	
	return expanduser("~");
