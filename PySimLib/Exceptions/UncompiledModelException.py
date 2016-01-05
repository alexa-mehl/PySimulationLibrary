class UncompiledModelException(Exception):
	#Constructor
	def __init__(this, mdl, tool):
		Exception.__init__(this);
		
		#Private members
		this.__mdl = mdl;
		this.__tool = tool;
		
	#Magic methods
	def __str__(this):
		return 'Model "' + str(this.__mdl) + '" is being used with tool "' + str(this.__tool) + '" but is not compiled.';
