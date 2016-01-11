from PySimLib import *;

Log.SetTarget(open("sim.log", "w"));

mdl = Model("struc_param", "struc_param.mo");
mdl.outputDir += "/result";
mdl.parameters["N"] = 2;

tool = mdl.GetCompatibleTools()[0];
tool.Compile(mdl);

sim = tool.CreateSimulation(mdl);
sim.stopTime = 10;
tool.Simulate(sim);

result = tool.ReadResult(sim);


p = Plot();
p.Add(result["time"], result["v[1]"], "r");
p.Add(result["time"], result["v[2]"], "b");
p.Show();
