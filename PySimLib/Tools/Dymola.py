"""
  Copyright (C) 2014-2018  Alexandra Mehlhase <a.mehlhase@tu-berlin.de>, All Rights Reserved
  
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
from PySimLib import Log, Platform;
from PySimLib.Config import *;
from PySimLib.Exceptions.SimulationFailedException import SimulationFailedException;
from PySimLib.Mat.Mat import Mat;
from PySimLib.Tools.ModelicaTool import ModelicaTool;

class Dymola(ModelicaTool):
	#Static class members
	__dymolaIsOpen = False;
	__ddeServer = None;
	__ddeConversation = None;
	__openFiles = {};
	
	__solverMap = {
		'deabm' : 1,
		'lsodar' : 4,
		'dassl' : 8
		#TODO THE REST
	};
	
	#Constructor
	def __init__(this):
		ModelicaTool.__init__(this);
		
		if(GetBoolConfigValue("Dymola", "SimByExe") == False):
			print("Warning: You're using Dymola with a reduced feature set. Models may won't be simulated altough they're working directly in Dymola (independent of PySimLib). Please make sure you've read and understood section 2.6.4 of the PySimLib user Guide - specifically the part about the 'SimByExe' flag.");
	
	#Private methods
	def __CheckIfModelIsCompiled(this, mdl):
		from PySimLib.Exceptions.UncompiledModelException import UncompiledModelException;
		
		#check if model is compiled
		if(not this._FileExists(this.__GetExeFilePath(mdl))):
			raise UncompiledModelException(mdl, this);
			
	def __DeleteUnnecessaryFiles(this):
		this._DeleteFile("alistlog.txt");
		this._DeleteFile("buildlog.txt");
		this._DeleteFile("dsfinal.txt");
		this._DeleteFile("dsin.txt");
		this._DeleteFile("dslog.txt");
		this._DeleteFile("dsmodel.c");
		this._DeleteFile("dymosim.exe");
		this._DeleteFile("dymosim.exp");
		this._DeleteFile("dymosim.lib");
			
	def __EnsureDymolaIsOpen(this):
		if(not Dymola.__dymolaIsOpen):
			import win32ui;
			import dde;
			import time;
			from PySimLib import Platform;
			
			Dymola.__ddeServer = dde.CreateServer();
			Dymola.__ddeServer.Create("TestClient");
			Dymola.__ddeConversation = dde.CreateConversation(Dymola.__ddeServer);
			Dymola.__dymolaIsOpen = True;
			
			Platform.Execute([GetConfigValue("Dymola", "PathExe")], False);
			time.sleep(float(GetConfigValue("Dymola", "StartupDelay")));
			Dymola.__ddeConversation.ConnectTo("dymola", " ");
			Dymola.__ddeConversation.Exec("OutputCPUtime:=true;");
			
	def __GetExeFilePath(this, mdl):
		from PySimLib import Platform;
		
		return mdl.outputDir + os.sep + mdl.outputName + Platform.GetExeFileExtension();
			
	def __GetInitFilePath(this, mdl):
		return mdl.outputDir + os.sep + mdl.outputName + "_in.mat";
		
	def __GetSimInitFilePath(this, sim):
		mdl = sim.GetModel();
		return mdl.simDir + os.sep + str(sim.GetSimNumber()) + "_in.mat";
		
	def __MapSolver(this, solver):
		for key in Dymola.__solverMap:
			if(solver.Matches(key)):
				return Dymola.__solverMap[key];
				
		raise Exception("Illegal solver '" + str(solverNumber) + "'");
			
	def __OpenFile(this, mdl, fileName):
		path = mdl.simDir + os.sep + fileName;
		path = path.replace('\\', '/');
		
		if(path not in Dymola.__openFiles):
			Dymola.__ddeConversation.Exec("openModel(\"" + path + "\")");
			Dymola.__openFiles[path] = True;
			
	def __ReadVarsFromMat(this, names, values, varTypeFilter):
		from PySimLib.VariableDescriptor import VariableDescriptor;
		
		result = {};
		
		for i in range(0, names.GetNumberOfStrings()):
			if(values.GetValue(4, i) in varTypeFilter):
				varDesc = VariableDescriptor();
				varDesc.start = values.GetValue(1, i);
				result[names.GetString(i)] = varDesc;
						
		return result;
			
	def __ReverseMapSolver(this, solverNumber):
		from PySimLib import FindSolver;
		
		solverNumber = int(solverNumber);
		for key in Dymola.__solverMap:
			if(Dymola.__solverMap[key] == solverNumber):
				return FindSolver(key);
		
		raise Exception("Illegal solver number '" + str(solverNumber) + "'");
		
	def __WriteInit(this, sim):
		from PySimLib.Mat.OutputStream import OutputStream;
		from PySimLib.Mat.MatrixTypeEvaluator import TYPE_INT32;
		
		mdl = sim.GetModel();
		
		mat = Mat();
		mat.Load(this.__GetInitFilePath(mdl));
		
		#set experiment values
		experiment = mat.GetMatrix("experiment");
		experiment.SetValue(0, 0, sim.startTime);
		experiment.SetValue(0, 1, sim.stopTime);
		experiment.SetValue(0, 4, sim.solver.tolerance);
		experiment.SetValue(0, 6, this.__MapSolver(sim.solver));
		#TODO: STEPSIZE
		
		#set variable start values
		names = mat.GetMatrix("initialName");
		values = mat.GetMatrix("initialValue");
		for i in range(0, names.GetNumberOfStrings()):
			name = names.GetString(i);
			
			if(name not in sim.variables):
				continue;
				
			if(sim.variables[name].start is not None):
				value = sim.variables[name].start;
				values.SetValue(1, i, value);
		
		#write output		
		file = open(this.__GetSimInitFilePath(sim), "wb");
		stream = OutputStream(file);
		#mat.Write(stream);
		
		#we need to set precision values for the matrices or dymola wont accept the input
		settings = mat.GetMatrix("settings");
		
		settings.SetDesiredOutputPrecision(TYPE_INT32);

		mat.GetMatrix("initialDescription").SetString(0, "Dymola");
		
		#we need to write the matrices in the exact order or dymola can't read the file		
		mat.GetMatrix("Aclass").Write("Aclass", stream);
		mat.GetMatrix("experiment").Write("experiment", stream);
		mat.GetMatrix("method").Write("method", stream);
		settings.Write("settings", stream);
		mat.GetMatrix("initialName").Write("initialName", stream);
		mat.GetMatrix("initialValue").Write("initialValue", stream);
		mat.GetMatrix("initialDescription").Write("initialDescription", stream);
		
		file.close();
			
	#Public methods
	def Close(this):
		if(Dymola.__ddeConversation is not None):
			Dymola.__ddeConversation.Exec("exit();");
			Dymola.__ddeConversation = None;
		
	def Compile(this, mdl):
		from PySimLib import Platform;
		
		this.__EnsureDymolaIsOpen();
		
		#open all needed mo files
		for x in mdl.GetFiles():
			this.__OpenFile(mdl, x);
			
		#go to sim dir			
		Dymola.__ddeConversation.Exec("cd(\"" + mdl.simDir.replace('\\', '/') + "\")");
		
		#simulate to run model
		Dymola.__ddeConversation.Exec("translateModel(\"" + mdl.GetModelicaClassString() + "\")");
		#Dymola.__ddeConversation.Exec("simulateModel(\"" + mdl.GetModelicaClassString() + "\", stopTime=0)"); #method=\"" + this.solver.name + "\"
		
		this._EnsureOutputFolderExists(mdl);
		
		#Convert the dsin
		args = [
			GetConfigValue("Dymola", "PathAlist"),
			"-b",
			mdl.simDir + os.sep + "dsin.txt",
			this.__GetInitFilePath(mdl)
		];
		Platform.Execute(args);
		
		#this._DeleteFile("dsres.mat");
		
		#Rename important files
		this._RenameFile("dymosim" + Platform.GetExeFileExtension(), this.__GetExeFilePath(mdl));
		
		this.__DeleteUnnecessaryFiles();
		
	def GetCompatibleSolvers(this):
		from PySimLib import FindSolver;
		
		solvers = [];
		
		for key in Dymola.__solverMap:
			solvers.append(FindSolver(key));
		
		return solvers;
		
	def GetName(this):
		return "Dymola";
		
	def ReadInit(this, mdl):		
		this.__CheckIfModelIsCompiled(mdl);
		
		initMat = Mat();
		initMat.Load(this.__GetInitFilePath(mdl));
		
		#read parameters
		varTypeFilter = {
			1, #parameters
		};
		
		parameters = this.__ReadVarsFromMat(initMat.GetMatrix("initialName"), initMat.GetMatrix("initialValue"), varTypeFilter);
		for name in parameters:
			mdl.parameters[name] = parameters[name].start;
			
		#read variables
		varTypeFilter = {
			2, #state variable
			6, #auxiliary variable
		};
		
		mdl.variables = this.__ReadVarsFromMat(initMat.GetMatrix("initialName"), initMat.GetMatrix("initialValue"), varTypeFilter);
			
		#read experiment values
		experiment = initMat.GetMatrix("experiment");
		mdl.startTime = experiment.GetValue(0, 0);
		mdl.stopTime = experiment.GetValue(0, 1);
		mdl.solver = this.__ReverseMapSolver(experiment.GetValue(0, 6));
		#sim.solver.stepSize = TODO: ???
		mdl.solver.tolerance = experiment.GetValue(0, 4);
		
	def Simulate(this, sim):
		mdl = sim.GetModel();
		
		#paths
		dsinPaths = mdl.simDir + os.sep + "dsin.txt";
		
		#error checks
		this.__CheckIfModelIsCompiled(mdl);
		
		this._EnsureResultFolderExists(mdl);
			
		#prepare init file
		this.__WriteInit(sim);
		
		#simulate
		if(GetBoolConfigValue("Dymola", "SimByExe")):
			from PySimLib import Log, Platform;
			
			args = [this.__GetExeFilePath(mdl), this.__GetSimInitFilePath(sim)];
			Platform.Execute(args, True, mdl.simDir);
		else:
			from PySimLib import Log, Platform;
			#convert back to dsin
			args = [
				GetConfigValue("Dymola", "PathAlist"),
				"-a",
				this.__GetSimInitFilePath(sim),
				dsinPaths
			];
			#Platform.Execute(args);
			
			#load simulation config --- apparently not working like this
			#Dymola.__ddeConversation.Exec("importInitial(\"" + this.__GetSimInitFilePath(sim).replace('\\', '/') + "\")");
			
			#run
			this.__EnsureDymolaIsOpen();
			Dymola.__ddeConversation.Exec("simulateModel(\"" + mdl.GetModelicaClassString(True, sim) + "\", startTime=" + str(sim.startTime) + ", stopTime=" + str(sim.stopTime) + ", method=\"" + str(sim.solver.GetName()) + "\", tolerance=" + str(sim.solver.tolerance) + ")");
			
			#we always need to close the model, so that dymola recompiles it			
			Dymola.__ddeConversation.Exec("closeModel();");
			
			#delete dsin
			this._DeleteFile(dsinPaths);
			
		failed = False;		
		if(this._FileExists("failure")):
			failed = True;
		
		#keep things clean
		#this._DeleteFile("status");
		#this._DeleteFile("success");
		#this._DeleteFile("failure");
		
		if(failed):
			this._DeleteFile("dsres.mat");
			raise SimulationFailedException(sim, this);
			
		this._DeleteFile(this.__GetSimInitFilePath(sim));
		
		#rename results
		this._RenameFile(mdl.simDir + os.sep + "dsres.mat", this._GetSimResultFilePath(sim));
		
		this.__DeleteUnnecessaryFiles();
		
	#Class functions
	def IsAvailable():
		return HasConfigValue("Dymola", "PathExe") and HasConfigValue("Dymola", "StartupDelay") and HasConfigValue("Dymola", "PathAlist") and HasConfigValue("Dymola", "SimByExe");
