class Ball():

	def __init__(self,coordsNew=[0,0],colorNew='',itemNew='',spinNew=[0,0],directionNew=[0,0],pulseNew=0,pulseSpinNew=0,numberNew=0,moveNew=True,coordsGuessNew=[0,0]):
		self.coords=coordsNew
		self.coordsGuess=coordsGuessNew
		self.spin=spinNew
		self.color=colorNew
		self.item=itemNew
		self.direction=directionNew
		self.pulse=pulseNew
		self.pulseSpin=pulseSpinNew
		self.number=numberNew
		self.move=moveNew

	def getCoords(self):
		return(self.coords)
	
	def getCoordsGuess(self):
		return(self.coordsGuess)

	def getSpin(self):
		return(self.spin)

	def getColor(self):
		return(self.color)

	def getItem(self):
		return(self.item)
		
	def getDirection(self):
		return(self.direction)

	def getPulse(self):
		return(self.pulse)
	
	def getPulseSpin(self):
		return(self.pulseSpin)

	def getNumber(self):
		return(self.number)
	
	def getMove(self):
		return(self.move)

	def setCoords(self,coordsNew):
		self.coords=coordsNew
	
	def setCoordsGuess(self,coordsGuessNew):
		self.coordsGuess=coordsGuessNew
		
	def setSpin(self,spinNew):
		self.spin=spinNew

	def setColor(self,colorNew):		
		self.color=colorNew
	
	def setItem(self,itemNew):
		self.item=itemNew

	def setDirection(self,directionNew):
		self.direction=directionNew

	def setPulse(self,pulseNew):
		self.pulse=pulseNew

	def setPulseSpin(self,pulseSpinNew):
		self.pulseSpin=pulseSpinNew

	def setNumber(self,numberNew):
		self.number=numberNew

	def setMove(self,moveNew):
		self.move=moveNew
		#if	not moveNew:
		#	print('move set to:',moveNew)

	def info(self):
		print('XY=',self.coords,'S=',self.spin,'itm=',self.item,'dir=',self.direction,'p=',self.pulse, 'pS=',self.pulseSpin,'XYG=',self.coordsGuess,'clr=',self.color)

	def paint(self,field):
		x=self.getCoords()[0]
		y=self.getCoords()[1]
		color=self.getColor()
		item=field.create_oval(x-5,y-5,x+5,y+5,fill=color,outline=color)
		self.setItem(item)

	def erase(self,field):
		field.delete(self.getItem())

class Stick():
	
	def __init__(self,coordsStartNew=[0,0],coordsFinishNew=[0,0],lengthNew=200,itemNew='',directionNew=[0,0]):
		self.coordsStart=coordsStartNew
		self.coordsFinish=coordsFinishNew	
		self.length=lengthNew	
		self.item=itemNew
		self.direction=directionNew
		
	def getCoordsStart(self):
		return(self.coordsStart)

	def getCoordsFinish(self):
		return(self.coordsFinish)
	
	def getLength(self):
		return(self.length)

	def getItem(self):
		return(self.item)

	def getDirection(self):
		return(self.direction)

	def setCoordsStart(self,coordsStartNew):
		self.coordsStart=coordsStartNew	

	def setCoordsFinish(self,coordsFinishNew):	
		self.coordsFinish=coordsFinishNew

	def setItem(self,itemNew):
		self.item=itemNew

	def setDirection(self,directionNew):
		self.direction=directionNew

	def paint(self,field):
		#color=stick.getColor()
		color='firebrick'
		xS=self.getCoordsStart()[0]
		yS=self.getCoordsStart()[1]
		xF=self.getCoordsFinish()[0]
		yF=self.getCoordsFinish()[1]
		item=field.create_line(xS,yS,xF,yF,fill=color)
		self.setItem(item)

	def erase(self,field):
		field.delete(self.getItem())

if __name__=='__main__':
	whiteBall=Ball([1,1,2],[0,0,1],'white')
	redBall=Ball([2,1,3],[4,5,6],'red')
	whiteBall.info()
	redBall.info()
	whiteBall.setCoords([10,10])
	redBall.setSpin([1,-1,10])
	whiteBall.info()
	redBall.info()
