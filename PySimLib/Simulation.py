class Simulation:
	#Static variables
	__simCounter = 0
	
	#Constructor
	def __init__(this, mdl):
		#Private members
		this.__mdl = mdl;
		this.__simNumber = Simulation.__simCounter;
		
		Simulation.__simCounter += 1;
		
		#Public members
		this.startTime = 0;
		this.stopTime = 1;
		this.solver = None;
		this.vars = {};
		
	#Magic methods
	def __str__(this):
		result = "Simulation(";
		result += "startTime: " + this.startTime + ", ";
		result += "stopTime: " + this.stopTime + ", ";
		result += "solver: " + str(this.solver) + ", ";
		result += "vars: {";
		for var in this.vars:
			result += "(" + str(var) + ", " + str(this.vars[var]) + ")";
		result += "})";
		
		return result;
		
	#Public methods
	def GetModel(this):
		return this.__mdl;
		
	def GetSimNumber(this):
		return this.__simNumber;
