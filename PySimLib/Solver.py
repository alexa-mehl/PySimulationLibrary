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

class Solver:
	#Constructor
	def __init__(this):
		#Public members
		this.stepSize = 0;
		this.tolerance = 1e-6;
		
	#Magic methods
	def __str__(this):
		return this.GetName() + "(stepSize: " + str(this.stepSize) + ", tolerance: " + str(this.tolerance) + ")";
		
	#Abstract
	def GetName(this):
		raise NotImplementedError("The method Solver::GetName is abstract.");
		
	def GetDetailedName(this):
		raise NotImplementedError("The method Solver::GetDetailedName is abstract.");
		
	def Matches(this, pattern):
		raise NotImplementedError("The method Solver::Matches is abstract.");
