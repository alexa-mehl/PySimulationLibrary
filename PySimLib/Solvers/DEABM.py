from PySimLib.Solver import Solver;

class DEABM(Solver):
	#Constructor
	def __init__(this):
		Solver.__init__(this);
		
	#Public methods
	def GetName(this):
		return "DEABM";
	
	def GetDetailedName(this):
		return "DEABM"; #nobody seems to know what it means... the last three letters could mean Adams-Bashforth-Moulton or Adams-Bashforth-Method
		
	def Matches(this, pattern):
		pattern = pattern.lower();
		names = {
			"deabm" #dymola name
		};
		
		return pattern in names;
