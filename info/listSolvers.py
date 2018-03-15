from PySimLib import *

space = "\t"

print("Name", space, "Detailed name")
print("----")

for solver in GetSolvers():
    print(solver.GetName(), space, solver.GetDetailedName())
