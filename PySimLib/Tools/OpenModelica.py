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
import shutil;
import os;
import xml.dom.minidom;
#Local
from PySimLib.Config import *;
from PySimLib import Log, Platform;
from PySimLib.Tools.ModelicaTool import ModelicaTool;

class OpenModelica(ModelicaTool):
	#Private methods
	def __AssertModelCompiled(this, mdl):
		from PySimLib.Exceptions.UncompiledModelException import UncompiledModelException;
		
		if(not this._FileExists(this.__GetInitFilePath(mdl))):
			raise UncompiledModelException(mdl, this);
		
	def __FindValueFromXMLVar(this, var):
		from PySimLib.VariableDescriptor import VariableDescriptor;
		store = False;
		
		varName = var.getAttribute("name");
		#if(var.getAttribute("isValueChangeable") == "false"):
			#return None;
		
		for node in var.childNodes: #find the value
			if(node.nodeType == xml.dom.Node.ELEMENT_NODE):					
				varDesc = VariableDescriptor();
				
				if(node.getAttribute("useStart") == "true"):
					start = node.getAttribute("start");
					if(start == ""):
						varDesc.start = 0;
					elif(start == "true"):
						varDesc.start = True;
					elif(start == "false"):
						varDesc.start = False;
					else:
						varDesc.start = float(start);
				else:
					varDesc.start = None;
				
				return varName, varDesc;
				
		return None;
		
	def __GetExeFilePath(this, mdl):
		return mdl.outputDir + os.sep + mdl.outputName + Platform.GetExeFileExtension();
		
	def __GetInfoFilePath(this, mdl):
		return mdl.outputDir + os.sep + mdl.outputName + "_info.json";
		
	def __GetInitFilePath(this, mdl):
		return mdl.outputDir + os.sep + mdl.outputName + "_init.xml";
		
	def __GetInitFileXML(this, mdl):		
		this.__AssertModelCompiled(mdl);
			
		return xml.dom.minidom.parse(this.__GetInitFilePath(mdl));
		
	def __GetSimInitFilePath(this, sim):
		mdl = sim.GetModel();
		
		return mdl.simDir + os.sep + str(sim.GetSimNumber()) + ".xml";
		
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
		
		initDom = this.__GetInitFileXML(mdl);
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
				
				if(varName not in sim.variables):
					continue;
					
				for node in var.childNodes: #find the value
					if(node.nodeType == xml.dom.Node.ELEMENT_NODE):
						if(sim.variables[varName].start is None):
							node.setAttribute("useStart", "false");
						else:
							node.setAttribute("useStart", "true");
							node.setAttribute("start", str(sim.variables[varName].start));
							#node.setAttribute("fixed", "true");
						break;
						
		this._DeleteFile(this.__GetSimInitFilePath(sim));
		file = open(this.__GetSimInitFilePath(sim), "w");
		initDom.writexml(file);
		file.close();
		
	#Public methods
	def Close(this):
		#we don't use any open process
		pass
		
	def Compile(this, mdl):
		from PySimLib.Exceptions.CompilationFailedException import CompilationFailedException;
		
		#write a mos file to be executed by openmodelica
		SCRIPTNAME = mdl.simDir + os.sep + mdl.outputName + ".mos";
		mosfile = open(SCRIPTNAME, 'w', 1);
		mosfile.write("loadModel(Modelica);\r\n");
		
		for item in mdl.GetFiles():
			mosfile.write("loadFile(\"" + item + "\");\r\n");
			
		#evaluate parameters
		#TODO looks like structural parameters cant be set in openmodelica
		overrideString = "";
		"""
		if(mdl.parameters):
			overrideString = ', simflags="-override ';
			for k in mdl.parameters:
				overrideString += k + "=" + str(mdl.parameters[k]) + " ";
			overrideString += '"';
		"""
			
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
			
		#make sure output folder exists
		if(not this._DirExists(mdl.outputDir)):
			os.makedirs(mdl.outputDir);
		
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
		this._DeleteFile(mdl.GetName() + "_16dae.h");
		this._DeleteFile(mdl.GetName() + "_16dae.c");
		this._DeleteFile(mdl.GetName() + "_16dae.o");
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
		this._RenameFile(mdl.GetName() + Platform.GetExeFileExtension(), this.__GetExeFilePath(mdl));
		this._RenameFile(mdl.GetName() + "_init.xml", this.__GetInitFilePath(mdl));
		this._RenameFile(mdl.GetName() + "_info.json", this.__GetInfoFilePath(mdl));
		
	def GetCompatibleSolvers(this):
		from PySimLib import FindSolver;
		
		solvers = [];
		
		solvers.append(FindSolver("dassl"));
		solvers.append(FindSolver("euler"));
		
		return solvers;
		
	def GetName(this):
		return "OpenModelica";
		
	def ReadInit(this, mdl):
		from PySimLib import FindSolver;
		
		initDom = this.__GetInitFileXML(mdl);
		mv = initDom.getElementsByTagName("ModelVariables")[0];
		de = initDom.getElementsByTagName("DefaultExperiment")[0];
		
		#read parameters			
		classTypeFilter = {
			"iPar", #integer parameter
			"rPar", #real parameter
		};
		
		parameters = this.__ReadVarsFromXML(mv, classTypeFilter);
		for name in parameters:
			mdl.parameters[name] = parameters[name].start;
			
		#read variables
		classTypeFilter = {
			"bAlg", #boolean algebraic
			"iAlg", #integer algebraic
			"rAlg", #real algebraic
			"rSta", #state variables
		};
		
		mdl.variables = this.__ReadVarsFromXML(mv, classTypeFilter);
		
		#read experiment values
		mdl.startTime = de.getAttribute("startTime");
		mdl.stopTime = de.getAttribute("stopTime");
		mdl.solver = FindSolver(de.getAttribute("solver"));
		mdl.solver.stepSize = float(de.getAttribute("stepSize"));
		mdl.solver.tolerance = float(de.getAttribute("tolerance"));
		
	def Simulate(this, sim):
		from PySimLib.Exceptions.SimulationFailedException import SimulationFailedException;
		
		mdl = sim.GetModel();
		
		#paths
		simInfoFilePath = mdl.simDir + os.sep + mdl.GetName() + "_info.json";
		
		#check if model is compiled
		this.__AssertModelCompiled(mdl);
		
		#make sure result folder exists
		if(not this._DirExists(mdl.resultDir)):
			os.makedirs(mdl.resultDir);
		
		#prepare init file		
		this.__WriteInit(sim);
		
		#info file can't be specified as arg to openmodelica
		if(not(mdl.outputName == mdl.GetName()) or not(mdl.simDir == mdl.outputDir)):
			shutil.copyfile(this.__GetInfoFilePath(mdl), simInfoFilePath);
			
		#run compiled model		
		simArgs = [
			this.__GetExeFilePath(mdl),
			"-f",
			this.__GetSimInitFilePath(sim),
		];
		
		exitCode = Platform.Execute(simArgs, True, mdl.simDir);
		if(not(exitCode == 0)):
			raise SimulationFailedException(sim, this);
		
		#keep things clean
		if(not(mdl.outputName == mdl.GetName()) or not(mdl.simDir == mdl.outputDir)):
			this._DeleteFile(simInfoFilePath);
		this._DeleteFile(this.__GetSimInitFilePath(sim));
		
		#rename results
		this._RenameFile(mdl.simDir + os.sep + mdl.GetName() + "_res.mat", this._GetSimResultFilePath(sim));
		
	#Class functions
	def IsAvailable():		
		return HasConfigValue("OpenModelica", "PathExe");
