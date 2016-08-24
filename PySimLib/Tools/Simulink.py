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

#Local
from PySimLib.Config import *;
from PySimLib.Mat.Mat import Mat;
from PySimLib.Tool import Tool;

class Simulink(Tool):
	#Static class members
	__matlabConnection = None;
	__matlabStarted = False;
	
	#Constructor
	def __init__(this):
		from pymatbridge import Matlab;
		
		Tool.__init__(this);
		
		Simulink.__matlabConnection = Matlab(executable=GetConfigValue('Simulink', 'PathExe'));
	
	#Private methods
	def __EnsureMatlabConnectionIsSetup(this):
		if(Simulink.__matlabStarted == False):
			Simulink.__matlabConnection.start();
			Simulink.__matlabStarted = True;
			
	def __GetSimResultFilePath(this, sim):
		mdl = sim.GetModel();
		
		return mdl.resultDir + os.sep + str(sim.GetSimNumber()) + "_" + mdl.outputName + ".mat";
	
	#Public methods
	def Accepts(this, mdl):
		from PySimLib.Models.SimulinkModel import SimulinkModel;
		
		return isinstance(mdl, SimulinkModel);
	
	def Close(this):
		if(Simulink.__matlabStarted):
			Simulink.__matlabConnection.stop();
			Simulink.__matlabStarted = False;
	
		
	def Compile(this, mdl):
		pass #nothing to be done here
		
	def GetName(this):
		return "Simulink";
		
	def ReadInit(this, mdl):
		from PySimLib import FindSolver;
		from PySimLib.VariableDescriptor import VariableDescriptor;
		
		mdl.startTime = None;
		mdl.stopTime = None;
		mdl.solver = FindSolver("dassl"); #TODO!!!!
		
		this.__EnsureMatlabConnectionIsSetup();
		
		cmd = "clear;"; #make sure workspace is clean
		cmd += "cd " + mdl.simDir + ";"; #go to sim dir
		Simulink.__matlabConnection.run_code(cmd);
		
		#exec init file
		if(this._FileExists(mdl.simDir + os.sep + mdl.GetName() + "_init.m")):
			Simulink.__matlabConnection.run_code(mdl.GetName() + "_init;");
		
		#get all variables
		varList = Simulink.__matlabConnection.get_variable('who');
		for x in varList:
			name = x[0][0];
			value = Simulink.__matlabConnection.get_variable(x[0][0]);
			
			var = VariableDescriptor();
			var.start = value;
			
			mdl.variables[name] = var;
		
	def ReadResult(this, sim):
		from PySimLib.SimulationResult import SimulationResult;
	
		mdl = sim.GetModel();
		
		result = {};
		m_res = Mat();
		m_res.Load(this.__GetSimResultFilePath(sim));
		
		for key in m_res.GetMatrices():
			m = m_res.GetMatrix(key);
			data = [];
			for y in range(0, m.GetNumberOfRows()):
				data.append(m.GetValue(0, y));
			
			result[key] = data;
		
		this._SetDerivedValuesFromSimulationResults(sim, result);
		
		return SimulationResult(result);
		
		
	def Simulate(this, sim):
		from PySimLib.Mat.OutputStream import OutputStream;
		
		mdl = sim.GetModel();
		
		this.__EnsureMatlabConnectionIsSetup();
		
		#make sure result folder exists
		if(not this._DirExists(mdl.resultDir)):
			os.makedirs(mdl.resultDir);
		
		#preparations
		cmd = "clear"; #clean up workspace
		cmd += "cd " + mdl.simDir + ";"; #go to sim dir
		Simulink.__matlabConnection.run_code(cmd);
		
		#send variables
		cmd = "";
		for name in mdl.variables:
			cmd += name + "=" + str(mdl.variables[name].start) + ";";
		Simulink.__matlabConnection.run_code(cmd);
			
		#simulate
		cmd = "sim('" + mdl.GetFile() + "'";
		if(not(mdl.startTime is None)):
			cmd += ", 'StartTime', " + str(mdl.startTime);
		if(not(mdl.stopTime is None)):
			cmd += ", 'StopTime', " + str(mdl.stopTime);
		cmd += ");";
		cmd += "logsout.unpack('all');"; #make all variables to top levels
		cmd += "clear logsout;"; #discard simulation results, as we have direct access to vars now
		Simulink.__matlabConnection.run_code(cmd);
		
		#get all timeserieses
		outMat = Mat();
		varList = Simulink.__matlabConnection.get_variable('who');
		time = None;
		for x in varList:
			data = Simulink.__matlabConnection.get_variable(x[0][0] + ".Data");
			if(not(data is None)):
				matrix = outMat.AddMatrix(x[0][0], 1, len(data));
				for y in range(0, len(data)):
					matrix.SetValue(0, y, data[y][0].item());
					
				tmp = Simulink.__matlabConnection.get_variable(x[0][0] + ".Time");
				if((time is None) or (len(tmp) > len(time))):
					time = tmp;
					
		#add time
		matrix = outMat.AddMatrix('time', 1, len(time));
		for y in range(0, len(time)):
			matrix.SetValue(0, y, time[y][0].item());
			
		#write mat file					
		file = open(this.__GetSimResultFilePath(sim), "wb");
		stream = OutputStream(file);					
		outMat.Write(stream);
		file.close();
		
	#Class functions
	def IsAvailable():
		return HasConfigValue("Simulink", "PathExe");
