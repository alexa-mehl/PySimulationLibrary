from PySimLib import *

space = "\t"

print("Name")
print("----")

for tool in GetTools():
    print(tool.GetName())
