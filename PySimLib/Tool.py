import os;

class Tool:
	#Constructor
	def __init__(this):
		pass
		
	#Magic methods
	def __str__(this):
		return this.GetName();
		
	#Protected methods
	def _DeleteFile(this, fileName):
		if(os.path.isfile(fileName)):
			os.remove(fileName);
			
	def _DirExists(this, dirPath):
		return os.path.isdir(dirPath);
		
	def _EnsureOutputFolderExists(this, mdl):
		if(not this._DirExists(mdl.outputDir)):
			os.makedirs(mdl.outputDir);
			
	def _EnsureResultFolderExists(this, mdl):
		if(not this._DirExists(mdl.resultDir)):
			os.makedirs(mdl.resultDir);
			
	def _FileExists(this, fileName):
		return os.path.isfile(fileName);
			
	def _RenameFile(this, fromName, toName):
		if(not (os.path.abspath(fromName) == os.path.abspath(toName))):
			this._DeleteFile(toName);
			os.rename(fromName, toName);
			
	def _SetDerivedValuesFromSimulationResults(this, sim, resultDict):
		mdl = sim.GetModel();
		
		#set final values
		for key in resultDict:
			if(key in sim.variables):
				f = resultDict[key][-1];
				sim.variables[key].final = f;
				mdl.variables[key].final = f;
		
	#Abstract
	def Accepts(this, mdl):
		raise NotImplementedError("The method Tool::Accepts is abstract.");
		
	def Close(this):
		raise NotImplementedError("The method Tool::Close is abstract.");
		
	def Compile(this, mdl):
		raise NotImplementedError("The method Tool::Compile is abstract.");
	
	def GetCompatibleSolvers(this):
		raise NotImplementedError("The method Tool::GetCompatibleSolvers is abstract.");
		
	def GetDefaultSolver(this):
		raise NotImplementedError("The method Tool::GetDefaultSolver is abstract.");
		
	def GetName(this):
		raise NotImplementedError("The method Tool::GetName is abstract.");
		
	def ReadInit(this, mdl):
		raise NotImplementedError("The method Tool::ReadInit is abstract.");
		
	def Simulate(this, sim):
		raise NotImplementedError("The method Tool::Simulate is abstract.");
		
	#Abstract Functions
	def IsAvailable():
		raise NotImplementedError("The function Tool::IsAvailable is abstract.");
