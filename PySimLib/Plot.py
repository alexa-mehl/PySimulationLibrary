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
