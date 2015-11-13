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
