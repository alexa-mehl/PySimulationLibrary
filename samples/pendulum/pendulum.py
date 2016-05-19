from PySimLib import *;

Log.SetTarget(open("sim.log", "w"));

mdl = Model("pendulum", "pendulum.mo");
mdl.outputDir += "/output";
mdl.resultDir += "/result";

tool = mdl.GetCompatibleTools()[0];
tool.Compile(mdl);
tool.ReadInit(mdl);

sim = Simulation(mdl);
sim.stopTime = 10;
tool.Simulate(sim);
result = tool.ReadResult(sim);


p = Plot();
p.Add(result["time"], result["derPhi"], "r");
p.Show();


tool.Close();
