#Interface
def CreateModel(name, files):
	global __g_modelClasses;
	
	if(not (type(files) == list)):
		files = [files];
		
	for mdlClass in __g_modelClasses:
		if(mdlClass.Matches(name, files)):
			return mdlClass(name, files);
			
			
def FindSolver(pattern):
	from PySimLib.Tool import Tool;
	
	solvers = GetSolvers();
	pattern = pattern.lower();
	for solver in solvers:
		if(not (solver.GetName().lower().find(pattern) == -1)):
			return solver;
				
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
	

#Internal
__g_tools = [];
__g_modelClasses = [];
__g_solvers = {}; #we need to store instances and its classes

def __RegisterTool(toolClass):
	if(toolClass.IsAvailable()):
		global __g_tools;
		
		__g_tools.append(toolClass());

def __RegisterTools():
	#OpenModelica
    from PySimLib.Tools.OpenModelica import OpenModelica;
    __RegisterTool(OpenModelica);
    
def __RegisterModelRepresentationClasses():
	global __g_modelClasses;
	
	#Modelica
	from PySimLib.Models.ModelicaModel import ModelicaModel;
	__g_modelClasses.append(ModelicaModel);
	
def __RegisterSolvers():
	global __g_solvers;
	
	#DASSL
	from PySimLib.Solvers.DASSL import DASSL;
	__g_solvers[DASSL()] = DASSL;
    
    
__RegisterTools();
__RegisterModelRepresentationClasses();
__RegisterSolvers();
