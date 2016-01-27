import sys;
from PySimLib.Mat.Mat import Mat;
from PySimLib.Mat.TextMatrix import TextMatrix;

space = "\t\t";

mat = Mat();
mat.Load(sys.argv[1]);
matrices = mat.GetMatrices();

print("Size is either 'Rows x Columns' or, for a Textmatrix, the number of strings");

print("Type", space, "Size", space, "Name")
print("----");
for key in matrices:
	if(type(matrices[key]) == TextMatrix):
		t = "TextMatrix\t";
		size = matrices[key].GetNumberOfStrings();
	else:
		t = "Matrix\t\t";
		size = str(matrices[key].GetNumberOfRows()) + "x" + str(matrices[key].GetNumberOfColumns());
	print(t, size, space, key);