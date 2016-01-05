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
			
	def _FileExists(this, fileName):
		return os.path.isfile(fileName);
			
	def _RenameFile(this, fromName, toName):
		if(not (os.path.abspath(fromName) == os.path.abspath(toName))):
			this._DeleteFile(toName);
			os.rename(fromName, toName);
		
	#Abstract
	def Accepts(this, mdl):
		raise NotImplementedError("The method Tool::Accepts is abstract.");
	
	def GetCompatibleSolvers(this):
		raise NotImplementedError("The method Tool::GetCompatibleSolvers is abstract.");
		
	def GetDefaultSolver(this):
		raise NotImplementedError("The method Tool::GetDefaultSolver is abstract.");
		
	def GetName(this):
		raise NotImplementedError("The method Tool::GetName is abstract.");
		
	def Compile(this, mdl):
		raise NotImplementedError("The method Tool::Compile is abstract.");
		
	def Simulate(this, sim):
		raise NotImplementedError("The method Tool::Simulate is abstract.");
