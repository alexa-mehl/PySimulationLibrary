"""
  Copyright (C) 2014-2016  Alexandra Mehlhase <a.mehlhase@tu-berlin.de>, All Rights Reserved
  
  Implemented by Alexandra Mehlhase, Amir Czwink
  
  This file is part of the AMSUN project
  (https://gitlab.tubit.tu-berlin.de/groups/amsun)

  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.
   
  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

#Global
from enum import Enum;
import os;
import subprocess;

class Platform(Enum):
	Windows = 1,
	Linux = 2,

#Interface functions
def Execute(args, blocking = True, workingDirectory = None):
	import shlex;
	from PySimLib import Log;
	
	#escape args
	for arg in args:
		arg = shlex.quote(arg);
		
	#execute
	childProcess = subprocess.Popen(args, shell = False, stdout=Log.GetTarget(), stderr=Log.GetTarget(), cwd = workingDirectory);
	if(blocking):
		childProcess.wait();
		exitCode = childProcess.returncode;
	else:
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
