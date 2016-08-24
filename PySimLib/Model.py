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

import os;

class Model:
	#Constructor
	def __init__(this, name, files):
		#Private members
		this.__name = name;
		
		#Public members
		this.outputName = name;
		this.outputDir = None;
		this.resultDir = None;
		this.simDir = None;
		this.variables = {};
		
		if(len(files) == 1):
			this.outputDir = os.path.abspath(os.path.dirname(files[0]));
			this.resultDir = this.outputDir;
			this.simDir = this.outputDir;
			
	#Public methods
	def GetCompatibleTools(this):
		from . import GetTools;
		
		tools = GetTools();
		result = [];
		
		for tool in tools:
			if(tool.Accepts(this)):
				result.append(tool);
		
		return result;
		
	def GetName(this):
		return this.__name;
