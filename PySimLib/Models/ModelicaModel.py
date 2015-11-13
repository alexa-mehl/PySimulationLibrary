import os;

from PySimLib.Model import Model;

class ModelicaModel(Model):
	#Constructor
	def __init__(this, name, files):
		Model.__init__(this, name);
		
		#Private members
		this.__files = files;
		this.__parameters = {};
		
	#Magic methods
	def __str__(this):
		return "Modelica class " + '"' + this.GetModelicaClassString() + '"';
		
	#Public methods
	def GetModelicaClassString(this):
		cmd = this.GetName();
		
		if(this.__parameters):
			cmd = cmd + "(";
			for key in this.__parameters:
				cmd = cmd + key + "=" + str(this.__parameters[key]) + ",";
			cmd = cmd[:-1]; #remove last comma
			cmd = cmd + ")";
			
		return cmd;
		
	#Class functions
	def Matches(name, files):
		return True;
