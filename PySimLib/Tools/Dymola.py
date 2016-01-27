#Local
from PySimLib import Log, Platform;
from PySimLib.Config import *;
from PySimLib.Mat.Mat import Mat;
from PySimLib.Tools.ModelicaTool import ModelicaTool;

class Dymola(ModelicaTool):
	#Static class members
	__dymolaIsOpen = False;
	__ddeServer = None;
	__ddeConversation = None;
	__openFiles = {};
	
	__solverMap = {
		'deabm' : 0,
		'dassl' : 8
		#TODO THE REST
	};
	
	#Private methods
	def __CheckIfModelIsCompiled(this, mdl):
		from PySimLib.Exceptions.UncompiledModelException import UncompiledModelException;
		
		#check if model is compiled
		if(not this._FileExists(this.__GetExeFilePath(mdl))):
			raise UncompiledModelException(mdl, this);
			
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
		
		return mdl.simDir + os.sep + mdl.outputName + Platform.GetExeFileExtension();
			
	def __GetInitFilePath(this, mdl):
		return mdl.simDir + os.sep + mdl.outputName + "_in.mat";
		
	def __GetSimInitFilePath(this, sim):
		mdl = sim.GetModel();
		return mdl.simDir + os.sep + str(sim.GetSimNumber()) + "_in.mat";
		
	def __MapSolver(this, solver):
		for key in Dymola.__solverMap:
			if(solver.Matches(key)):
				return Dymola.__solverMap[key];
				
		raise Exception("Illegal solver '" + str(solverNumber) + "'");
			
	def __OpenFile(this, mdl, fileName):
		path = mdl.simDir + '/' + fileName;
		
		if(path not in Dymola.__openFiles):
			path = path.replace('\\', '/');
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
			if(name in sim.vars):
				value = sim.vars[name].start;
				values.SetValue(1, i, value);
		
		#write output		
		file = open(this.__GetSimInitFilePath(sim), "wb");
		stream = OutputStream(file);
		mat.Write(stream);
		
		#we need to write the matrices in the exact order or dymola can't read the file
		#outMat.GetMatrix("Aclass").Write("Aclass", stream);
		#outMat.GetMatrix("experiment").Write("experiment", stream);
		#outMat.GetMatrix("method").Write("method", stream);
		#outMat.GetMatrix("settings").Write("settings", stream);
		#outMat.GetMatrix("initialName").Write("initialName", stream);
		#outMat.GetMatrix("initialValue").Write("initialValue", stream);
		#outMat.GetMatrix("initialDescription").Write("initialDescription", stream);
		
		file.close();
			
	#Public methods
	def Close(this):
		Dymola.__ddeConversation.Exec("exit();");
		
	def Compile(this, mdl):
		from PySimLib import Platform;
		
		this.__EnsureDymolaIsOpen();
		
		#open all needed mo files
		for x in mdl.GetFiles():
			this.__OpenFile(mdl, x);
			
		#go to sim dir			
		Dymola.__ddeConversation.Exec("cd(\"" + mdl.simDir.replace('\\', '/') + "\")");
		
		#simulate to run model
		Dymola.__ddeConversation.Exec("simulateModel(\"" + mdl.GetModelicaClassString() + "\", stopTime=0)"); #method=\"" + this.solver.name + "\"
		
		#Delete unnecessary files
		this._DeleteFile("buildlog.txt");
		this._DeleteFile("dsfinal.txt");
		this._DeleteFile("dslog.txt");
		this._DeleteFile("dsmodel.c");
		this._DeleteFile("dsres.mat");
		this._DeleteFile("dymosim.exp");
		this._DeleteFile("dymosim.lib");
		
		#Convert the dsin
		args = [
			GetConfigValue("Dymola", "PathAlist"),
			"-b",
			mdl.simDir + os.sep + "dsin.txt",
			mdl.simDir + os.sep + mdl.outputName + "_in.mat"
		];
		Platform.Execute(args);
		
		this._DeleteFile("alistlog.txt");
		this._DeleteFile("dsin.txt");
		
		#Rename important files
		this._RenameFile("dymosim" + Platform.GetExeFileExtension(), mdl.outputName + Platform.GetExeFileExtension());
		
	def CreateSimulation(this, mdl):
		from PySimLib.Simulation import Simulation;
		
		this.__CheckIfModelIsCompiled(mdl);
			
		sim = Simulation(mdl);
			
		initMat = Mat();
		initMat.Load(this.__GetInitFilePath(mdl));
			
		#read experiment values
		experiment = initMat.GetMatrix("experiment");
		sim.startTime = experiment.GetValue(0, 0);
		sim.stopTime = experiment.GetValue(0, 1);
		sim.solver = this.__ReverseMapSolver(experiment.GetValue(0, 6));
		#sim.solver.stepSize = TODO: ???
		sim.solver.tolerance = experiment.GetValue(0, 4);
		
		#read variables			
		varTypeFilter = {
			1, #parameters
			2, #state variable
		};
		
		sim.vars = this.__ReadVarsFromMat(initMat.GetMatrix("initialName"), initMat.GetMatrix("initialValue"), varTypeFilter);
		
		return sim;
		
	def GetCompatibleSolvers(this):
		from PySimLib import FindSolver;
		
		solvers = [];
		
		solvers.append(FindSolver("dassl"));
		
		return solvers;
		
	def GetName(this):
		return "Dymola";
		
	def Simulate(this, sim):
		mdl = sim.GetModel();
		
		#error checks
		this.__CheckIfModelIsCompiled(mdl);
		
		#make sure result folder exists
		if(not this._DirExists(mdl.outputDir)):
			os.makedirs(mdl.outputDir);
			
		#prepare init file		
		this.__WriteInit(sim);
		
		#simulate
		if(GetBoolConfigValue("Dymola", "SimByExe")):
			args = [this.__GetExeFilePath(mdl), this.__GetSimInitFilePath(sim)];
			Platform.Execute(args);
		else:
			#TODO: Load simconfig
			from PySimLib import Log, Platform;
			#convert back to dsin
			args = [
				GetConfigValue("Dymola", "PathAlist"),
				"-a",
				this.__GetSimInitFilePath(sim),
				mdl.simDir + os.sep + "dsin.txt",
			];
			Platform.Execute(args);
			
			#run
			this.__EnsureDymolaIsOpen();
			Dymola.__ddeConversation.Exec("simulateModel(\"" + mdl.GetModelicaClassString() + "\")");
			
			#delete dsin
			this._DeleteFile(mdl.simDir + os.sep + "dsin.txt");
			
		failed = False;		
		if(this._FileExists("failure")):
			failed = True;
		
		#keep things clean
		this._DeleteFile("dsfinal.txt");
		this._DeleteFile("dslog.txt");
		this._DeleteFile("status");
		this._DeleteFile("success");
		this._DeleteFile("failure");
		
		if(failed):
			this._DeleteFile("dsres.mat");
			raise SimulationFailedException();
			
		this._DeleteFile(this.__GetSimInitFilePath(sim));
		
		#rename results
		this._RenameFile(mdl.simDir + os.sep + "dsres.mat", mdl.outputDir + os.sep + mdl.outputName + "_res.mat");
		
	#Class functions
	def IsAvailable():
		return HasConfigValue("Dymola", "PathExe") and HasConfigValue("Dymola", "StartupDelay") and HasConfigValue("Dymola", "PathAlist") and HasConfigValue("Dymola", "SimByExe");