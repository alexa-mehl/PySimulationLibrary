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
import pylab;

class Plot:
	#Static variables
	__figureCounter = 1
	
	#Constructor
	def __init__(this):		
		this.__figureId = Plot.__figureCounter;
		Plot.__figureCounter += 1;
		
		pylab.figure(this.__figureId); #create the figure
		
	#Public methods
	def Add(this, x, y, color):
		pylab.figure(this.__figureId); #make sure to work on correct figure
		pylab.plot(x, y, color);
		
	def Save(this, fileName):
		pylab.figure(this.__figureId); #make sure to work on correct figure
		pylab.grid(1);
		pylab.savefig(fileName);
		
	def SetXLabel(this, label):
		pylab.figure(this.__figureId); #make sure to work on correct figure
		pylab.xlabel(label);
		
	def SetYLabel(this, label):
		pylab.figure(this.__figureId); #make sure to work on correct figure
		pylab.ylabel(label);
		
	def Show(this):
		pylab.figure(this.__figureId); #make sure to work on correct figure
		pylab.show();
