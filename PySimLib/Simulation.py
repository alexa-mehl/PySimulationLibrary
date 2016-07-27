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

class Simulation:
	#Static variables
	__simCounter = 0
	
	#Constructor
	def __init__(this, mdl, simNumber = None):
		import copy;
		
		if(simNumber is None):
			simNumber = Simulation.__simCounter;
			
			Simulation.__simCounter += 1;
		
		#Private members
		this.__mdl = mdl;
		this.__simNumber = simNumber;
		
		#Public members
		this.startTime = mdl.startTime;
		this.stopTime = mdl.stopTime;
		this.solver = copy.deepcopy(mdl.solver);
		this.variables = copy.deepcopy(mdl.variables);
		
	#Magic methods
	def __str__(this):
		result = "Simulation(";
		result += "startTime: " + str(this.startTime) + ", ";
		result += "stopTime: " + str(this.stopTime) + ", ";
		result += "solver: " + str(this.solver) + ", ";
		result += "vars: {";
		for var in this.variables:
			result += "(" + str(var) + ", " + str(this.variables[var]) + ")";
		result += "})";
		
		return result;
		
	#Public methods
	def GetModel(this):
		return this.__mdl;
		
	def GetSimNumber(this):
		return this.__simNumber;
