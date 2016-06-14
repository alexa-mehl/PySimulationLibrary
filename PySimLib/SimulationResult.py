"""
This class holds the values that a simulation generates.
The values in the object are stored in a dictionary that maps each variable to a vector of values of this variable.
The following should illustrate that:
values = 
{
	"x" : [t1(x), t2(x)....],
	"y" : [t1(y), t2(y)....],
	"time" : [t1(time), t2(time)...],
	...
}

Note: Also the simulation time should be present with the name "time" (CASE SENSITIVE).
"""
class SimulationResult:
	#Constructor
	#Args:
	# values - Simulation result values in a form as illustrated above
	def __init__(this, values):
		this.__values = values;
		
	#Magic methods
	def __getitem__(this, key):
		return this.__values[key];
		
	#Public methods
	#Returns a datapoint of a trace of a variable
	#
	#Args:
	# varName - variable trace to be read
	# nTimesBack - number of time steps to move backwards in time (defaults to 0 meaning last available value)
	def GetValue(this, varName, nTimestepsBack = 0):
		datapoints = this.__values[varName];
		
		return datapoints[len(datapoints) - 1 - nTimestepsBack];
		
	#Returns the result dictionary		
	def GetValues(this):
		return this.__values;
