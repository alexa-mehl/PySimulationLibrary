#Global
import os;
#Local
from PySimLib.Tool import Tool;

class ModelicaTool(Tool):
	#Protected methods
	def _GetSimResultFilePath(this, sim):
		mdl = sim.GetModel();
		
		return mdl.resultDir + os.sep + str(sim.GetSimNumber()) + "_" + mdl.outputName + ".mat";
		
	#Public methods
	def Accepts(this, mdl):
		from PySimLib.Models.ModelicaModel import ModelicaModel;
		
		return isinstance(mdl, ModelicaModel);
		
	def GetDefaultSolver(this):
		from PySimLib import FindSolver;
		
		return FindSolver("dassl");
		
	def ReadResult(this, sim):
		from PySimLib.Mat.Mat import Mat;
		from PySimLib.SimulationResult import SimulationResult;
		
		mdl = sim.GetModel();
		
		result = {};
		m_res = Mat();
		m_res.Load(this._GetSimResultFilePath(sim));
		
		#dsres matrices are all transposed-.-
		names = m_res.GetMatrix("name");
		names.Transpose();
		dataInfo = m_res.GetMatrix("dataInfo");
		dataInfo.Transpose();
		
		for i in range(0, names.GetNumberOfStrings()):
			if(i == 0 and dataInfo.GetValue(0, i) == 0):
				dataMatrixIndex = 2; #hm... this is not necessarily the case... we need the biggest abscissa
			else:
				dataMatrixIndex = dataInfo.GetValue(0, i);
			dataMatrix = m_res.GetMatrix("data_" + str(dataMatrixIndex));
			k = dataInfo.GetValue(1, i);
			col = abs(k)-1;
			if(k > 0):
				sign = 1;
			else:
				sign = -1;
				
			currentVar = [];
			for j in range(0, dataMatrix.GetNumberOfColumns()):
				currentVar.append(sign * dataMatrix.GetValue(j, col));
			
			if(names.GetString(i) == "Time"):
				result["time"] = currentVar;
			else:
				result[names.GetString(i)] = currentVar;
				
		#set final values
		for key in result:
			if(key in sim.variables):
				f = result[key][-1];
				sim.variables[key].final = f;
				mdl.variables[key].final = f;
				
		return SimulationResult(result);
