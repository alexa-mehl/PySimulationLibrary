import os;

from PySimLib.Model import Model;

class ModelicaModel(Model):
	#Constructor
	def __init__(this, name, files):
		Model.__init__(this, name, files);
		
		#Private members
		this.__files = files;
		
		#Public members
		this.parameters = {};
		
	#Magic methods
	def __str__(this):
		return "Modelica class " + '"' + this.GetModelicaClassString() + '"';
		
	#Public methods
	def GetFiles(this):
		return this.__files;

	def GetModelicaClassString(this):
		cmd = this.GetName();
		
		if(this.parameters):
			cmd = cmd + "(";
			for key in this.parameters:
				cmd = cmd + key + "=" + str(this.parameters[key]) + ",";
			cmd = cmd[:-1]; #remove last comma
			cmd = cmd + ")";
			
		return cmd;
		
	#Class functions
	def Matches(name, files):
		return True;
