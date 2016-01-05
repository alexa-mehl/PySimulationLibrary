class CompilationFailedException(Exception):
	#Constructor
	def __init__(this, mdl, tool):
		Exception.__init__(this);
		
		#Private members
		this.__mdl = mdl;
		this.__tool = tool;
		
	#Magic methods
	def __str__(this):
		return 'Compilation of model "' + str(this.__mdl) + '" with tool "' + str(this.__tool) + '" failed.';
