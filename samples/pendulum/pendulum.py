from PySimLib import *;

mdl = CreateModel("pendel", "pendel.mo");
tool = mdl.GetCompatibleTools()[0];
solver = tool.GetDefaultSolver();

print(mdl);
print(tool);
print(solver);
print(tool.GetCompatibleSolvers());
