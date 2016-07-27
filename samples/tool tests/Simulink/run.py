from PySimLib import *;

Log.SetTarget(open("sim.log", "w"));

mdl = Model("pendel", "pendel.mdl");
mdl.outputDir += "/output";
mdl.resultDir += "/result";

tool = FindTool("Simulink");
if(tool is None):
	exit("Couldn't get Simulink instance. Check your config file.");
	
tool.Compile(mdl);
tool.ReadInit(mdl);

sim = Simulation(mdl);
tool.Simulate(sim);
result = tool.ReadResult(sim);

p = Plot();
p.Add(result["x"], result["y"], "r");
p.Show();


tool.Close();
