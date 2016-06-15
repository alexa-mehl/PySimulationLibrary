from PySimLib import *;
from math import *;

Log.SetTarget(open("sim.log", "w"));

#setup models and tool and then compile
pendulum = Model("pendulum", "pendulum.mo");
ball = Model("ball", "ball.mo");

pendulum.outputDir += "/output";
pendulum.resultDir += "/result";
ball.outputDir += "/output";
ball.resultDir += "/result";

tool = pendulum.GetCompatibleTools()[0];
tool.Compile(pendulum);
tool.Compile(ball);
tool.ReadInit(pendulum);
tool.ReadInit(ball);

#simulate pendulum until we find a force less than zero
sim = Simulation(pendulum);
sim.stopTime = 1;

derPhi = 0;
index = None;

while index is None:
	derPhi += 1;
	
	sim.variables["derPhi"].start = derPhi;
	tool.Simulate(sim);
	result = tool.ReadResult(sim);
	
	for i in range(0, len(result["F"])):
		if(result["F"][i] < 0):
			index = i; #got it
			break;
			
print("derPhi: ", derPhi);


#calc x and y for pendulum
x = [];
y = [];
for i in range(0, index):
	v = result["phi"][i];
	x.append(sin(v) * pendulum.parameters["L"]);
	y.append(-cos(v) * pendulum.parameters["L"]);
			

#run ball sim
sim = Simulation(ball);

sim.stopTime = 0.6;
sim.variables["x"].start = sin(result["phi"][index]);
sim.variables["y"].start = -cos(result["phi"][index]);
sim.variables["vx"].start = cos(result["phi"][index]) * result["derPhi"][index] * pendulum.parameters["L"];
sim.variables["vy"].start = sin(result["phi"][index]) * result["derPhi"][index] * pendulum.parameters["L"];

tool.Simulate(sim);
result2 = tool.ReadResult(sim);


p = Plot();
p.Add(x, y, "r");
p.Add(result2["x"], result2["y"], "b");
p.Save(pendulum.outputDir + "/pendulumToBall.png");


tool.Close();
