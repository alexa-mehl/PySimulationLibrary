#Global
import shutil;
import os;
import xml.dom.minidom;
#Local
from PySimLib.Config import *;
from PySimLib import Log, Platform;
from PySimLib.Tools.ModelicaTool import ModelicaTool;

class OpenModelica(ModelicaTool):
	#Private methods
	def __FindValueFromXMLVar(this, var):
		from PySimLib.VariableDescriptor import VariableDescriptor;
		store = False;
		
		varName = var.getAttribute("name");
		if(var.getAttribute("isValueChangeable") == "false"):
			return None;
		
		for node in var.childNodes: #find the value
			if(node.nodeType == xml.dom.Node.ELEMENT_NODE):
				if(node.getAttribute("useStart") == "false"):
					return None;
					
				varDesc = VariableDescriptor();
					
				start = node.getAttribute("start");
				if(start == ""):
					varDesc.start = 0;
				else:
					varDesc.start = float(start);
				
				return varName, varDesc;
				
		return None;
		
	def __GetSolverString(this, solver):
		if(solver.Matches("dassl")):
			return "dassl";
			
		raise NotImplementedError("OpenModelica::__GetSolverString");
		
	def __ReadVarsFromXML(this, mv, classTypeFilter):
		result = {};
		
		for var in mv.childNodes:
			if(var.nodeType == xml.dom.Node.ELEMENT_NODE):
				if(var.getAttribute("classType") in classTypeFilter):
					nameAndValue = this.__FindValueFromXMLVar(var);
					
					if(not(nameAndValue is None)):
						varName, value = nameAndValue;
						result[varName] = value;
						
		return result;
		
	def __WriteInit(this, sim):
		mdl = sim.GetModel();
		
		initFilePath = mdl.simDir + os.sep + mdl.outputName + "_init.xml";
		outputFilePath = mdl.simDir + os.sep + str(sim.GetSimNumber()) + ".xml";
		
		initDom = xml.dom.minidom.parse(initFilePath);
		mv = initDom.getElementsByTagName("ModelVariables")[0];
		de = initDom.getElementsByTagName("DefaultExperiment")[0];
		
		if(sim.solver.stepSize == 0):
			sim.solver.stepSize = 1e-6; #this is bad... but else OM simulates endlessly
		
		#Set experiment values
		de.setAttribute("startTime", str(sim.startTime));
		de.setAttribute("stopTime", str(sim.stopTime));
		de.setAttribute("stepSize", str(sim.solver.stepSize));
		de.setAttribute("tolerance", str(sim.solver.tolerance));
		de.setAttribute("solver", this.__GetSolverString(sim.solver));
		
		#Set initial variables		
		for var in mv.childNodes:
			if(var.nodeType == xml.dom.Node.ELEMENT_NODE):
				varName = var.getAttribute("name");
				
				if(varName not in sim.vars):
					continue;
					
				for node in var.childNodes: #find the value
					if(node.nodeType == xml.dom.Node.ELEMENT_NODE):
						#node.setAttribute("useStart", "true");
						#node.setAttribute("fixed", "true");
						node.setAttribute("start", str(sim.vars[varName].start));
						break;
						
		this._DeleteFile(outputFilePath);
		file = open(outputFilePath, "w");
		initDom.writexml(file);
		file.close();
		
	#Public methods		
	def Compile(this, mdl):
		from PySimLib.Exceptions.CompilationFailedException import CompilationFailedException;
		
		#write a mos file to be executed by openmodelica
		SCRIPTNAME = mdl.simDir + os.sep + mdl.GetName() + ".mos";
		mosfile = open(SCRIPTNAME, 'w', 1);
		mosfile.write("loadModel(Modelica);\r\n");
		
		for item in mdl.GetFiles():
			mosfile.write("loadFile(\"" + item + "\");\r\n");
			
		#evaluate parameters #TODO looks like structural parameters cant be set in openmodelica
		overrideString = "";
		if(mdl.parameters):
			overrideString = ', simflags="-override ';
			for k in mdl.parameters:
				overrideString += k + "=" + str(mdl.parameters[k]) + " ";
			overrideString += '"';
			
		# do a dummy simulation since it is not yet possible to do a translation only
		#mosfile.write("simulate(" + mdl.GetModelicaClassString() + ", startTime = " + str(0) + ", stopTime = " + str(1) + ", method = \"" + "dassl" + "\", outputFormat=\"mat\");\r\n");
		mosfile.write("simulate(" + mdl.GetName() + ", startTime = " + str(0) + ", stopTime = " + str(1) + ", method = \"" + "dassl" + "\", outputFormat=\"mat\"" + overrideString + ");\r\n");
		mosfile.close();
		
		#call the open modelica compiler
		omcArgs = [
			GetConfigValue("OpenModelica", "PathExe"),
			os.path.abspath(SCRIPTNAME),
			"Modelica"
		];
		
		this._DeleteFile(mdl.outputName + Platform.GetExeFileExtension()); #delete old exe to be sure that a new one is created
		
		Platform.Execute(omcArgs); #omc seems to return always 0
				
		this._DeleteFile(SCRIPTNAME); #we don't need the mos script anymore
		if(not this._FileExists(mdl.GetName() + Platform.GetExeFileExtension())): #if simulation failed there will be no exe
			raise CompilationFailedException(mdl, this);
		
		#Remove unnecessary files		
		this._DeleteFile(mdl.GetName() + ".c");
		this._DeleteFile(mdl.GetName() + ".libs");
		this._DeleteFile(mdl.GetName() + ".log");
		this._DeleteFile(mdl.GetName() + ".makefile");
		this._DeleteFile(mdl.GetName() + ".o");
		this._DeleteFile(mdl.GetName() + "_01exo.c");
		this._DeleteFile(mdl.GetName() + "_01exo.o");
		this._DeleteFile(mdl.GetName() + "_02nls.c");
		this._DeleteFile(mdl.GetName() + "_02nls.o");
		this._DeleteFile(mdl.GetName() + "_03lsy.c");
		this._DeleteFile(mdl.GetName() + "_03lsy.o");
		this._DeleteFile(mdl.GetName() + "_04set.c");
		this._DeleteFile(mdl.GetName() + "_04set.o");
		this._DeleteFile(mdl.GetName() + "_05evt.c");
		this._DeleteFile(mdl.GetName() + "_05evt.o");
		this._DeleteFile(mdl.GetName() + "_06inz.c");
		this._DeleteFile(mdl.GetName() + "_06inz.o");
		this._DeleteFile(mdl.GetName() + "_07dly.c");
		this._DeleteFile(mdl.GetName() + "_07dly.o");
		this._DeleteFile(mdl.GetName() + "_08bnd.c");
		this._DeleteFile(mdl.GetName() + "_08bnd.o");
		this._DeleteFile(mdl.GetName() + "_09alg.c");
		this._DeleteFile(mdl.GetName() + "_09alg.o");
		this._DeleteFile(mdl.GetName() + "_10asr.c");
		this._DeleteFile(mdl.GetName() + "_10asr.o");
		this._DeleteFile(mdl.GetName() + "_11mix.c");
		this._DeleteFile(mdl.GetName() + "_11mix.o");
		this._DeleteFile(mdl.GetName() + "_11mix.h");
		this._DeleteFile(mdl.GetName() + "_12jac.c");
		this._DeleteFile(mdl.GetName() + "_12jac.h");
		this._DeleteFile(mdl.GetName() + "_12jac.o");
		this._DeleteFile(mdl.GetName() + "_13opt.c");
		this._DeleteFile(mdl.GetName() + "_13opt.o");
		this._DeleteFile(mdl.GetName() + "_13opt.h");
		this._DeleteFile(mdl.GetName() + "_14lnz.c");
		this._DeleteFile(mdl.GetName() + "_14lnz.o");
		this._DeleteFile(mdl.GetName() + "_15syn.c");
		this._DeleteFile(mdl.GetName() + "_15syn.o");
		this._DeleteFile(mdl.GetName() + "_functions.c");
		this._DeleteFile(mdl.GetName() + "_functions.h");
		this._DeleteFile(mdl.GetName() + "_functions.o");
		this._DeleteFile(mdl.GetName() + "_includes.h");
		this._DeleteFile(mdl.GetName() + "_literals.h");
		this._DeleteFile(mdl.GetName() + "_model.h");
		this._DeleteFile(mdl.GetName() + "_records.c");
		this._DeleteFile(mdl.GetName() + "_records.o");
		this._DeleteFile(mdl.GetName() + "_res.mat");
		
		#Rename important files
		this._RenameFile(mdl.GetName() + Platform.GetExeFileExtension(), mdl.simDir + os.sep + mdl.outputName + Platform.GetExeFileExtension());
		this._RenameFile(mdl.GetName() + "_init.xml", mdl.simDir + os.sep + mdl.outputName + "_init.xml");
		this._RenameFile(mdl.GetName() + "_info.json", mdl.simDir + os.sep + mdl.outputName + "_info.json");
		
	def CreateSimulation(this, mdl):
		from PySimLib.Simulation import Simulation;
		from PySimLib import FindSolver;
		from PySimLib.Exceptions.UncompiledModelException import UncompiledModelException;
		
		initFilePath = mdl.simDir + os.sep + mdl.outputName + "_init.xml";
		
		if(not this._FileExists(initFilePath)):
			raise UncompiledModelException(mdl, this);
			
		initDom = xml.dom.minidom.parse(initFilePath);
		mv = initDom.getElementsByTagName("ModelVariables")[0];
		de = initDom.getElementsByTagName("DefaultExperiment")[0];
		
		sim = Simulation(mdl);
			
		#read experiment values
		sim.startTime = de.getAttribute("startTime");
		sim.stopTime = de.getAttribute("stopTime");
		sim.solver = FindSolver(de.getAttribute("solver"));
		sim.solver.stepSize = float(de.getAttribute("stepSize"));
		sim.solver.tolerance = float(de.getAttribute("tolerance"));
		
		#read variables			
		classTypeFilter = {
		"rSta" #state variables
		};
		
		sim.vars = this.__ReadVarsFromXML(mv, classTypeFilter);
		
		return sim;
		
	def GetCompatibleSolvers(this):
		from PySimLib import FindSolver;
		
		solvers = [];
		
		solvers.append(FindSolver("dassl"));
		solvers.append(FindSolver("euler"));
		
		return solvers;
		
	def GetName(this):
		return "OpenModelica";
		
	def Simulate(this, sim):
		from PySimLib.Exceptions.SimulationFailedException import SimulationFailedException;
		from PySimLib.Exceptions.UncompiledModelException import UncompiledModelException;
		
		mdl = sim.GetModel();
		
		#paths
		simInitFilePath = mdl.simDir + os.sep + str(sim.GetSimNumber()) + ".xml";
		simInfoFilePath = mdl.simDir + os.sep + mdl.GetName() + "_info.json";
		exePath = mdl.simDir + os.sep + mdl.GetName() + Platform.GetExeFileExtension();
		
		#check if model is compiled
		if(not this._FileExists(exePath)):
			raise UncompiledModelException(mdl, this);
		
		#make sure result folder exists
		if(not this._DirExists(mdl.outputDir)):
			os.makedirs(mdl.outputDir);
		
		#prepare init file		
		this.__WriteInit(sim);
		
		#info file can't be specified as arg to openmodelica
		if(not(mdl.outputName == mdl.GetName())):
			shutil.copyfile(mdl.simDir + os.sep + mdl.outputName + "_info.json", simInfoFilePath);
			
		#run compiled model		
		simArgs = [
			exePath,
			"-f",
			simInitFilePath,
		];		
		exitCode = Platform.Execute(simArgs);
		if(not(exitCode == 0)):
			raise SimulationFailedException(sim, this);
		
		#keep things clean
		if(not(mdl.outputName == mdl.GetName())):
			this._DeleteFile(simInfoFilePath);
		this._DeleteFile(simInitFilePath);
		
		#rename results
		this._RenameFile(mdl.GetName() + "_res.mat", mdl.outputDir + os.sep + mdl.outputName + "_res.mat");
		
	#Class functions
	def IsAvailable():		
		return HasConfigValue("OpenModelica", "PathExe");
