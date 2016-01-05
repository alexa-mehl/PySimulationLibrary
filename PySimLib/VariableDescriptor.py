class VariableDescriptor:
	#Constructor
	def __init__(this):
		#Public members
		this.start = None;
		
	#Magic methods
	def __str__(this):
		result = "start: " + str(this.start);
		
		return result;
