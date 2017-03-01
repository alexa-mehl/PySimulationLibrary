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

#Lib
import os;
import os.path;
import re;

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

	def GetModelicaClassString(this, includeVariables = False, source = None):
		cmd = this.GetName();
		
		def numericSafe(x):
			if(type(x) == float and x.is_integer()):
				return int(x);
			return x;
		
		if(source is None):
			source = this;
		
		if(this.parameters or source.variables):
			cmd = cmd + "(";
			for key in this.parameters:
				cmd = cmd + key + "=" + str(this.parameters[key]) + ",";
			for key in source.variables:
				if(source.variables[key].start is None):
					continue;
				if(re.match("der(.+?)", key)): #skip derivatives
					continue;
					
				cmd += key + "(start=" + str(numericSafe(source.variables[key].start)) + "),";
			cmd = cmd[:-1]; #remove last comma
			cmd = cmd + ")";
			
		return cmd;
		
	#Class functions
	def Matches(name, files):
		extension = os.path.splitext(files[0])[1];
		
		return extension == ".mo";
