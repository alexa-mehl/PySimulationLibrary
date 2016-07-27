import os;

from PySimLib.Model import Model;

class SimulinkModel(Model):
	#Constructor
	def __init__(this, name, files):
		Model.__init__(this, name, files);
		
		#Private members		
		this.__file = files[0];
		
	#Public methods
	def GetFile(this):
		return this.__file;
		
	#Class functions
	def Matches(name, files):
		extension = os.path.splitext(files[0])[1];
		
		return extension == ".mdl";
