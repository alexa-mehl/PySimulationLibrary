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

#Import what user might need
from PySimLib import Log;
from PySimLib.Plot import Plot;
from PySimLib.Simulation import Simulation;

#Internal
__g_tools = [];
__g_modelClasses = [];
__g_solvers = {}; #we need to store instances and its classes

def __RegisterTool(toolClass):
	if(toolClass.IsAvailable()):
		global __g_tools;
		
		__g_tools.append(toolClass());

def __RegisterTools():
	#Dymola
	from PySimLib.Tools.Dymola import Dymola;
	__RegisterTool(Dymola);
	
	#OpenModelica
	from PySimLib.Tools.OpenModelica import OpenModelica;
	__RegisterTool(OpenModelica);
	
	#Simulink
	from PySimLib.Tools.Simulink import Simulink;
	__RegisterTool(Simulink);
	
def __RegisterModelRepresentationClasses():
	global __g_modelClasses;
	
	#Modelica
	from PySimLib.Models.ModelicaModel import ModelicaModel;
	__g_modelClasses.append(ModelicaModel);
	
	#Simulink
	from PySimLib.Models.SimulinkModel import SimulinkModel;
	__g_modelClasses.append(SimulinkModel);
	
def __RegisterSolvers():
	global __g_solvers;
	
	#DEABM
	from PySimLib.Solvers.DEABM import DEABM;
	__g_solvers[DEABM()] = DEABM;
	
	#DASSL
	from PySimLib.Solvers.DASSL import DASSL;
	__g_solvers[DASSL()] = DASSL;
	
	#Euler #TODO: REENABLE ME!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
	#from PySimLib.Solvers.Euler import Euler;
	#__g_solvers[Euler()] = Euler;
	
	#LSODAR
	from PySimLib.Solvers.LSODAR import LSODAR;
	__g_solvers[LSODAR()] = LSODAR;
	
Model = None;

__RegisterTools();
__RegisterSolvers();
__RegisterModelRepresentationClasses();


#Interface
def Model(name, files):
	global __g_modelClasses;
	
	if(not (type(files) == list)):
		files = [files];
	if(not(files)): #if files is empty
		return None;
		
	for mdlClass in __g_modelClasses:
		if(mdlClass.Matches(name, files)):
			return mdlClass(name, files);


def FindSolver(pattern):
	from PySimLib.Tool import Tool;
	
	solvers = GetSolvers();
	for solver in solvers:
		if(solver.Matches(pattern)):
			return solver;
				
	return None;
	
def FindTool(pattern):
	tools = GetTools();
	
	pattern = pattern.lower();
	for tool in tools:
		if(tool.GetName().lower() == pattern):
			return tool;
			
	return None;


def GetSolvers():
	global __g_solvers;
	
	result = [];
	
	for solver in __g_solvers:
		result.append(__g_solvers[solver]());
		
	return result;

		
def GetTools():
	global __g_tools;
	
	return __g_tools;	
