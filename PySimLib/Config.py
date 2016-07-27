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

from PySimLib.Platform import *;

#Public
def GetBoolConfigValue(section, key):
	global __g_sections;
	
	return __g_sections[section][key] == "true";
	
def GetConfigValue(section, key):
	global __g_sections;
	
	return __g_sections[section][key];
	
def HasConfigValue(section, key):
	global __g_sections;
	
	if(section in __g_sections):
		return key in __g_sections[section];
	
	return False;




#Internal
__g_sections = {};

def ReadConfigFromFile():
	import os;
	import os.path;
	import configparser;
	
	global __g_sections;
	
	path = GetConfigDirectory() + '/PySimLib.cfg';
	
	if(not os.path.isfile(path)):
		raise Exception("PySimLib is not configured. Please read the manual to do so.");
		
	parser = configparser.ConfigParser();
	parser.optionxform = str;	#disable lower caseing
	parser.read(path);
	
	for section in parser.sections():
		entries = {};
		for key in parser.options(section):
			entries[key] = parser[section][key];
			
		if(len(entries) > 0):
			__g_sections[section] = entries;

#read config
ReadConfigFromFile();
