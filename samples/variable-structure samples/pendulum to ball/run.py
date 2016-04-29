from PySimLib import *;
from math import *;

Log.SetTarget(open("sim.log", "w"));

#setup models and tool and then compile
pendulum = Model("pendulum", "pendulum.mo");
ball = Model("ball", "ball.mo");			

tool = pendulum.GetCompatibleTools()[0];
tool.Compile(pendulum);
tool.Compile(ball);

#simulate pendulum until we find a force less than zero
sim = tool.CreateSimulation(pendulum);

derPhi = 0;
index = None;

while index is None:
	derPhi += 1;
	
	sim.vars["derPhi"].start = derPhi;
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
	x.append(sin(v));
	y.append(-cos(v));
			

#run ball sim
sim = tool.CreateSimulation(ball);

sim.vars["x"].start = sin(result["phi"][index]);
sim.vars["y"].start = -cos(result["phi"][index]);

tool.Simulate(sim);
result2 = tool.ReadResult(sim);


p = Plot();
p.Add(x, y, "r");
p.Add(result2["x"], result2["y"], "b");
p.Save("pendulumToBall.png");


tool.Close();
