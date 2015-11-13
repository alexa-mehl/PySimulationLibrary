from PySimLib.Config import *;
from PySimLib.Tool import Tool;

class OpenModelica(Tool):
	#Public methods
	def Accepts(this, mdl):
		from PySimLib.Models.ModelicaModel import ModelicaModel;
		
		return isinstance(mdl, ModelicaModel);
		
	def GetCompatibleSolvers(this):
		from PySimLib import FindSolver;
		
		solvers = [];
		
		solvers.append(FindSolver("dassl"));
		
		return solvers;
		
	def GetDefaultSolver(this):
		from PySimLib import FindSolver;
		
		return FindSolver("dassl");
		
	def GetName(this):
		return "OpenModelica";
		
	#Class functions
	def IsAvailable():		
		return HasConfigValue("OpenModelica", "PathExe");
