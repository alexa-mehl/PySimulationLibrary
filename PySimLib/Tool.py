import os;

class Tool:
    #Constructor
    def __init__(this):
        pass
        
    #Magic methods
    def __str__(this):
    	return this.GetName();
    
    #Abstract
    def Accepts(this, mdl):
    	raise NotImplementedError("The method Tool::Accepts is abstract.");
    	
    def GetCompatibleSolvers(this):
    	raise NotImplementedError("The method Tool::GetCompatibleSolvers is abstract.");
    	
    def GetDefaultSolver(this):
    	raise NotImplementedError("The method Tool::GetDefaultSolver is abstract.");
    	
    def GetName(this):
        raise NotImplementedError("The method Tool::GetName is abstract.");
