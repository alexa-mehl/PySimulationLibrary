import os;

class Model:
	#Constructor
	def __init__(this, name, files):
		#Private members
		this.__name = name;
		
		#Public members
		this.outputName = name;
		this.outputDir = None;
		this.simDir = None;
		
		if(len(files) == 1):
			this.outputDir = os.path.abspath(os.path.dirname(files[0]));
			this.simDir = this.outputDir;
			
	#Public methods
	def GetCompatibleTools(this):
		from . import GetTools;
		
		tools = GetTools();
		result = [];
		
		for tool in tools:
			if(tool.Accepts(this)):
				result.append(tool);
		
		return result;
		
	def GetName(this):
		return this.__name;
