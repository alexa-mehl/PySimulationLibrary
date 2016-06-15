from PySimLib.Solver import Solver;

class LSODAR(Solver):
	#Constructor
	def __init__(this):
		Solver.__init__(this);
		
	#Public methods
	def GetName(this):
		return "LSodar";
	
	def GetDetailedName(this):
		return "Livermore Solver for Ordinary Differential equations, with Automatic method switching for stiff and nonstiff problems, and with Root-finding";
		
	def Matches(this, pattern):
		pattern = pattern.lower();
		names = {
			"lsodar" #dymola name
		};
		
		return pattern in names;
