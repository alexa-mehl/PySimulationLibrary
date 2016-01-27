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
