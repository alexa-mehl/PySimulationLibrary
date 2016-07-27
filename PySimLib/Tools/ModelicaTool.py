"""
  Copyright (C) 2014-2016  Alexandra Mehlhase <a.mehlhase@tu-berlin.de>, All Rights Reserved
  
  Implemented by Alexandra Mehlhase, Amir Czwink
  
  This file is part of the AMSUN project
  (https://gitlab.tubit.tu-berlin.de/groups/amsun)

  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.
   
  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

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
				
		this._SetDerivedValuesFromSimulationResults(sim, result);
				
		return SimulationResult(result);
