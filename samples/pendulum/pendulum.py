from PySimLib import *;

Log.SetTarget(open("sim.log", "w"));

mdl = Model("pendulum", "pendulum.mo");
mdl.outputDir += "/result";
mdl.parameters["L"] = 2;

tool = mdl.GetCompatibleTools()[0];
tool.Compile(mdl);

sim = tool.CreateSimulation(mdl);
tool.Simulate(sim);

result = tool.ReadResult(sim);


p = Plot();
p.Add(result["time"], result["derPhi"], "r");
p.Show();
