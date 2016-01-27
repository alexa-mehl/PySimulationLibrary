import sys;
from PySimLib import *;

tool = FindTool(sys.argv[1]);

print("Name: ", tool.GetName());

print("Compatible Solvers:");
for solver in tool.GetCompatibleSolvers():
	print('    ', solver.GetName());
	
print("Default Solver: ", tool.GetDefaultSolver().GetName());