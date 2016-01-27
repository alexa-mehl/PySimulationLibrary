import sys;
from PySimLib.Mat.Mat import Mat;
from PySimLib.Mat.TextMatrix import TextMatrix;

space = "\t\t";

mat = Mat();
mat.Load(sys.argv[1]);
m = mat.GetMatrix(sys.argv[2]);

if(type(m) == TextMatrix):
	t = 1;
	print("Type: ", "TextMatrix");
	print("Number of strings: ", m.GetNumberOfStrings());
else:
	t = 0;
	print("Type: ", "Matrix");
	print("Size ('Rows'x'Columns'): ", str(m.GetNumberOfRows()) + "x" + str(m.GetNumberOfColumns()));
print("----");

if(t == 1):
	for i in range(0, m.GetNumberOfStrings()):
		print(m.GetString(i));
else:
	for y in range(0, m.GetNumberOfRows()):
		line = "";
		for x in range(0, m.GetNumberOfColumns()):
			line += str(m.GetValue(x, y)) + ", ";
		print(line);