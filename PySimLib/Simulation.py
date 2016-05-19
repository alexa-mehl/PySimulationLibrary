class Simulation:
	#Static variables
	__simCounter = 0
	
	#Constructor
	def __init__(this, mdl):
		import copy;
		
		#Private members
		this.__mdl = mdl;
		this.__simNumber = Simulation.__simCounter;
		
		Simulation.__simCounter += 1;
		
		#Public members
		this.startTime = mdl.startTime;
		this.stopTime = mdl.stopTime;
		this.solver = copy.deepcopy(mdl.solver);
		this.variables = copy.deepcopy(mdl.variables);
		
	#Magic methods
	def __str__(this):
		result = "Simulation(";
		result += "startTime: " + str(this.startTime) + ", ";
		result += "stopTime: " + str(this.stopTime) + ", ";
		result += "solver: " + str(this.solver) + ", ";
		result += "vars: {";
		for var in this.variables:
			result += "(" + str(var) + ", " + str(this.variables[var]) + ")";
		result += "})";
		
		return result;
		
	#Public methods
	def GetModel(this):
		return this.__mdl;
		
	def GetSimNumber(this):
		return this.__simNumber;
