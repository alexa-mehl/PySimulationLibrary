class VariableDescriptor:
	#Constructor
	def __init__(this):
		#Public members
		this.start = None;
		this.final = None;
		
	#Magic methods
	def __str__(this):
		result = "start: " + str(this.start) + ", ";
		result += "final: " + str(this.final);
		
		return result;
