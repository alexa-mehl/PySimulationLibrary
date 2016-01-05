class Solver:
	#Constructor
	def __init__(this):
		#Public members
		this.stepSize = 0;
		this.tolerance = 1e-6;
		
	#Magic methods
	def __str__(this):
		return this.GetName() + "(stepSize: " + str(this.stepSize) + ", tolerance: " + str(this.tolerance) + ")";
		
	#Abstract
	def GetName(this):
		raise NotImplementedError("The method Solver::GetName is abstract.");
		
	def GetDetailedName(this):
		raise NotImplementedError("The method Solver::GetDetailedName is abstract.");
		
	def Matches(this, pattern):
		raise NotImplementedError("The method Solver::Matches is abstract.");
