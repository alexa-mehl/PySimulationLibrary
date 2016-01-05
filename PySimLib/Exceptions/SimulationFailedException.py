class SimulationFailedException(Exception):
	#Constructor
	def __init__(this, sim, tool):
		Exception.__init__(this);
		
		#Private members
		this.__sim = sim;
		this.__tool = tool;
		
	#Magic methods
	def __str__(this):
		return 'Simulation of model "' + str(this.__sim.GetModel()) + '" with tool "' + str(this.__tool) + '" failed.';
