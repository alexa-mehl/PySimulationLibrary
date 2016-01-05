from PySimLib.Solver import Solver;

class DASSL(Solver):
	#Constructor
	def __init__(this):
		Solver.__init__(this);
		
	#Public methods
	def GetName(this):
		return "DASSL";
	
	def GetDetailedName(this):
		return "Differential Algebraic System Solver";
		
	def Matches(this, pattern):
		pattern = pattern.lower();
		names = {
			"dassl" #open modelica name
		};
		
		return pattern in names;
