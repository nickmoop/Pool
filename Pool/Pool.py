import random
import time
import math
from threading import *
from tkinter import *
from tkinter import messagebox
from ClassBall import Ball
from ClassBall import Stick

root=Tk()
root.resizable(False,False)
root.geometry("856x912+0+20")   		#355/710(1/5)

balls=[]
bitPlaced=False
listOfCheckedBalls=[]
stick=Stick()			
ballFieldCoords=[0,0]					#from clickBallLeft to hitBallByStick
topPoint=[0,0,0]						#top point of ball[x,y,z??]
frictionBallCloth=0.25					#const=0.25
frictionBallBoard=0.20					#const=0.20
frictionBallBall=0.03					#const=0.03
lossBallStick=0.13						#const=0.13
lossBallBoard=0.55						#const=0.55
g=9.809									#const=9.809
##########################				PAINT FIELD START
forse=StringVar()
forse.set('100')
fieldForse=Entry(root,textvariable=forse)
fieldForse.place(x=550,y=450,width=100,height=20)

board=Label(root,bg='brown')
board.place(x=85,y=85,width=384,height=742)

										#MAKE THIS!
powerBar=Scrollbar(root)
powerBar.place(x=800,y=85,width=20,height=742)
										#MAKE THIS!
ballField=Canvas(root)
ballField.place(x=560,y=85,width=200,height=200)
ballField.create_oval(10,10,190,190,fill='white',outline='black')
ballField.create_line(10,100,190,100,fill='black')					#horizontal line
ballField.create_line(100,10,100,190,fill='black')					#vertical line
#ballField.create_oval(99,99,101,101,fill='black',outline='black')	#center
pointOfHit=ballField.create_oval(0,0,0,0,fill='red',outline='red')
rotationAxle=ballField.create_line(0,0,0,0,fill='red')

mainField=Canvas(root,bg='dark green')
mainField.place(x=100,y=100,width=356,height=712)
mainField.create_line(0,565,356,565,fill='white')
mainField.create_arc(120,507,236,623,start=180,extent=180,style='arc',outline='white')
mainField.create_oval(176,563,180,567,fill='white',outline='white')
mainField.create_oval(176,63,180,67,fill='white',outline='white')
mainField.create_oval(176,176,180,180,fill='white',outline='white')
mainField.create_oval(176,354,180,358,fill='white',outline='white')
###########################				PAINT FIELD FINISH
###########################				MAKE LIST OF BALLS START
###########################             BALLS, RADIUS=5(D=52.5mm/5/2)			
deltaX=0		
for i in range(1,6):
	for j in range(i):
		balls.append(Ball([178+j*10-deltaX,178-i*10],'red',mainField.create_oval(0,0,0,0)))
	deltaX+=5
balls.append(Ball([178,65],'black',mainField.create_oval(0,0,0,0)))
balls.append(Ball([178,178],'hot pink',mainField.create_oval(0,0,0,0)))
balls.append(Ball([178,356],'blue',mainField.create_oval(0,0,0,0)))
balls.append(Ball([120,565],'green',mainField.create_oval(0,0,0,0)))
balls.append(Ball([178,565],'sienna',mainField.create_oval(0,0,0,0)))
balls.append(Ball([236,565],'yellow',mainField.create_oval(0,0,0,0)))
balls.append(Ball([0,0],'white',mainField.create_oval(0,0,0,0)))
###########################				MAKE LIST OF BALLS FINISH
###########################				SIMPLE THINGS START
def placeHit():
	global holdHit
	holdHit=False

def holdHit():
	global holdHit
	holdHit=True

def placeStick():
	global holdStick
	holdStick=False

def holdStick():
	global holdStick
	holdStick=True

def FindDist():
	global balls
	distanceMin=100
	distanceMax=0
	for ball1 in balls:
		for ball2 in balls:
			if ball1.getNumber()!=ball2.getNumber():
				dx=ball1.getCoords()[0]-ball2.getCoords()[0]
				dy=ball1.getCoords()[1]-ball2.getCoords()[1]
				distance=(dx**2+dy**2)**(1/2)
				if distance<distanceMin:
					distanceMin=distance
				if  distance>distanceMax:
					distanceMax=distance
	messagebox.showinfo('Oops','Minimum distance='+str(round(distanceMin,1))+'\nMaximum distance='+str(round(distanceMax,1)))

def calcFinishCoords(x,y,stick): 
	dx=x-stick.getCoordsStart()[0]
	dy=y-stick.getCoordsStart()[1]
	length=((dx**2)+(dy**2))**(1/2)
	if length!=stick.getLength:
		try:
			koeffLen=(stick.getLength())/length
			x=koeffLen*dx+stick.getCoordsStart()[0]
			y=koeffLen*dy+stick.getCoordsStart()[1]
		except ZeroDivisionError:
			pass
	stick.setCoordsFinish([x,y])

def pushStick():
	global holdStick
	global holdHit
	global forse
	forseMin=0.0
	forseMax=1000.0
	try:
		forse=float(fieldForse.get())
		if not (forse<forseMin) and not (forse>forseMax):
			if holdStick and holdHit:
				stickHitBall()
				checkThread=Thread(target=checkTimer)
				checkThread.setDaemon(True)
				checkThread.start()
			else:
				messagebox.showinfo('Oops','Hold hit and stick first')
		else:
			messagebox.showinfo('Oops','Forse value not between '+str(forseMin)+' and '+str(forseMax))
			fieldForse.delete(0,END)
			fieldForse.insert(0,0)
	except ValueError:
		messagebox.showinfo('Oops','Forse value not digit')
		fieldForse.delete(0,END)
		fieldForse.insert(0,0)

def calcDashedCoords(x,y,stick):		#MAKE THIS!
	dx=x-stick.getCoordsStart()[0]
	dy=y-stick.getCoordsStart()[1]
	if dx>=0 or dy>=0:
		try:
			xTmp=0
			yTmp=((-stick.getCoordsStart()[0])*dy/dx)+stick.getCoordsStart()[1]
		except ZeroDivisionError:
			pass
	else:
		pass							#MAKE THIS!
										
def stickHitBall():					
	global stick
	global ball
	global mainField
	dirX=((stick.getCoordsStart()[0]-stick.getCoordsFinish()[0])/stick.getLength())
	dirY=((stick.getCoordsStart()[1]-stick.getCoordsFinish()[1])/stick.getLength())
	stick.setDirection([dirX,dirY])
	timer=0
	while timer<1000:
		time.sleep(1/1000)
		xStartNew=stick.getCoordsStart()[0]+dirX
		xFinishNew=stick.getCoordsFinish()[0]+dirX
		yStartNew=stick.getCoordsStart()[1]+dirY
		yFinishNew=stick.getCoordsFinish()[1]+dirY
		stick.setCoordsStart([(xStartNew),(yStartNew)])
		stick.setCoordsFinish([(xFinishNew),(yFinishNew)])
		stick.erase(mainField)
		stick.paint(mainField)
		for ball in balls:
			deltaX=ball.getCoords()[0]-xStartNew
			deltaY=ball.getCoords()[1]-yStartNew
			distance=((deltaX)**2+(deltaY)**2)**(1/2)-5
			if distance<0.0:
				hitBallByStick(ball,stick)
				timer=1274
			else:
				pass
		timer+=1

def hitBallByStick(ball,stick):
	global forse
	global topPoint
	global ballFieldCoords
	r=100
	x=ballFieldCoords[0]
	y=ballFieldCoords[1]
	findTopPointDirection(x,y)		  	#RELATIVE!!!
	a=((x-100)**(2)+(y-100)**(2))**(1/2)
	v0=forse
	teta=0.13
	dM=float(1/3)
	h=a									#RECALC!!!!
	if a<=60:
		v1Numerator=v0*(1+dM)*(1+(1-teta-teta*(1/dM)*(1+(5/2)*((a/r)**(2))))**(1/2))
		v1Denomenator=(1+dM+5/2*((a/r)**(2)))*(1+((1-teta-teta*(1/dM))**(1/2)))
		v1=v1Numerator/v1Denomenator
		rR=(v1*h*5)/(2*r)
		ball.setPulse(v1)
		ball.setPulseSpin(rR)
		ball.setDirection(stick.getDirection())
		dirX=stick.getDirection()[0]
		dirY=stick.getDirection()[1]
		x=-(topPoint[0]*dirY-topPoint[1]*dirX)	#ABSOLUTE.
		y=topPoint[0]*dirX+topPoint[1]*dirY
		ball.setSpin([x,y])
	else:
		messagebox.showinfo('Oops','Bad hit:a>0.6')

def findTopPointDirection(x,y):
	global topPoint
	dx=x-100
	dy=y-100
	l=((dx**2)+(dy**2))**(1/2)
	if l!=0:
		xNew=dx/l
		yNew=-dy/l
	else:
		xNew=0
		yNew=0
	topPoint[0]=xNew
	topPoint[1]=yNew

def calcBallDirection(dirX,dirY):
	if dirY!=0:
		dirBallX=dirX/dirY
	else:
		dirBallX=0
		dirBallY=1
	if dirX!=0:
		dirBallY=dirY/dirX
	else:
		dirBallX=1
		dirBallY=0
	d=(dirBallX**2+dirBallY**2)**(1/2)
	if d!=0:
		dirBallX=abs(dirBallX/d)
		dirBallY=abs(dirBallY/d)
	else:
		dirBallX=dirY
		dirBallY=dirX
	return([dirBallX,dirBallY])

def calcBallSign(dirSummX,dirSummY,dirX,dirY):
	signSummX=math.copysign(1,dirSummX)
	signSummY=math.copysign(1,dirSummY)
	signX=math.copysign(1,dirX)
	signY=math.copysign(1,dirY)
	signBallX=signSummX
	signBallY=signSummY
	if signSummX!=signX or signSummY!=signY:
		pass
	else:
		if abs(dirSummX)<abs(dirX):
			signBallX=-signSummX
		if abs(dirSummY)<abs(dirY):
			signBallY=-signSummY
	return([signBallX,signBallY])

def calcBallPulse(ball,ballToCheck,dirSummX,dirSummY,pulseSumm):
	ballX=ball.getDirection()[0]
	ballY=ball.getDirection()[1]
	ballToCheckX=ballToCheck.getDirection()[0]
	ballToCheckY=ballToCheck.getDirection()[1]
	pulseBall=abs(dirSummX*ballX+dirSummY*ballY)*pulseSumm#####	MAYBE NEED CORRECTION!!!
	pulseBallToCheck=abs(dirSummX*ballToCheckX+dirSummY*ballToCheckY)*pulseSumm
	return(pulseBall,pulseBallToCheck)

def checkBoardHit(ball):#####	MAYBE NEED CORRECTION!!!(accuracy)
	if ball.getCoordsGuess()[0]<5 or ball.getCoordsGuess()[0]>350:
		x=ball.getDirection()[0]
		y=ball.getDirection()[1]
		ball.setDirection([-x,y])
	if ball.getCoordsGuess()[1]<5 or ball.getCoordsGuess()[1]>706:
		x=ball.getDirection()[0]
		y=ball.getDirection()[1]
		ball.setDirection([x,-y])	

def ballIsNotHitted(ballNumber,ballToCheckNumber):
	global listOfCheckedBalls
	flag=True
	for value in listOfCheckedBalls:
		if value[0]==ballNumber and value[1]==ballToCheckNumber:
			flag=False
			break
		elif value[1]==ballNumber and value[0]==ballToCheckNumber:
			flag=False
			break
		else:
			flag=True
	return(flag)

def removeBallsFromListOfCheckedBalls():
	global balls
	global listOfCheckedBalls
	if listOfCheckedBalls:				
		for value in listOfCheckedBalls:
			x1=0
			y1=0
			x2=0
			y2=0
			for ball in balls:
				if value[0]==ball.getNumber():
					x1=ball.getCoords()[0]
					y1=ball.getCoords()[1]
					x1g=ball.getCoordsGuess()[0]
					y1g=ball.getCoordsGuess()[1]
				if value[1]==ball.getNumber():
					x2=ball.getCoords()[0]		
					y2=ball.getCoords()[1]
					x2g=ball.getCoordsGuess()[0]
					y2g=ball.getCoordsGuess()[1]		
			if x1!=0 and x2!=0:
				distance=((x1-x2)**2+(y1-y2)**2)**(1/2)
				distanceGuess=((x1g-x2g)**2+(y1g-y2g)**2)**(1/2)
				if distance>=10.0:
					listOfCheckedBalls.remove(value)
				elif distanceGuess>10:
					try:
						listOfCheckedBalls.remove(value)
					except:
						print(value,listOfCheckedBalls)
###########################				SIMPLE THINGS FINISH
###########################				CALCULATIONS START
def checkBallHitSimple(ball,step):
	global balls
	xg=ball.getCoordsGuess()[0]
	yg=ball.getCoordsGuess()[1]
	x=ball.getCoords()[0]
	y=ball.getCoords()[1]
	for ballToCheck in balls:
		if ball!=ballToCheck:
			xBTC=ballToCheck.getCoords()[0]
			yBTC=ballToCheck.getCoords()[1]	
			distance=((xg-xBTC)**2+(yg-yBTC)**2)**(1/2)
			distance1=((x-xBTC)**2+(y-yBTC)**2)**(1/2)
			if distance<10.0 and distance1>10.0:
				i=0
				#print(' in:',distance,distance1)
				while distance<10.0:
					xNew=x+step[0]/1000*i
					yNew=y+step[1]/1000*i
					deltaX=xNew-xBTC
					deltaY=yNew-yBTC
					distance=((deltaX)**2+(deltaY)**2)**(1/2)
					#print(distance)
					i+=1
				#print('out:',distance,'-',i)
				ball.setCoords([xNew,yNew])
				break

def checkBallHit(ball):
	global balls
	global listOfCheckedBalls
	ballsToCheck=[]
	x=ball.getCoordsGuess()[0]
	y=ball.getCoordsGuess()[1]
	k=0
	for ballToCheck in balls:
		if ball!=ballToCheck:
			xBTC=ballToCheck.getCoords()[0]
			yBTC=ballToCheck.getCoords()[1]
			xBTCg=ballToCheck.getCoordsGuess()[0]
			yBTCg=ballToCheck.getCoordsGuess()[1]
			ballNumber=ball.getNumber()
			ballToCheckNumber=ballToCheck.getNumber()		
			distance=((x-xBTC)**2+(y-yBTC)**2)**(1/2)	
			distanceG=((x-xBTCg)**2+(y-yBTCg)**2)**(1/2)
			if (distance<10.0 or distanceG<10.0) and ballIsNotHitted(ballNumber,ballToCheckNumber):
				k+=1
				listOfCheckedBalls.append([ballNumber,ballToCheckNumber])
				ball.setCoordsGuess(ball.getCoords())
				ballToCheck.setCoordsGuess(ballToCheck.getCoords())
				ballsToCheck.append(ballToCheck)
	if k==0:
		pass
	if k==1:
		hitBallByBall(ball,ballsToCheck[0])
	if k==2:
		hitBallByBallx2(ball,ballsToCheck[0],ballsToCheck[1])
	if k>2:
		print('ERROR in checkBallHit, K>2.K=',k)

def hitBallByBall(ball,ballToCheck):
	ball.setMove(False)
	ballToCheck.setMove(False)
	dx=ball.getCoords()[0]-ballToCheck.getCoords()[0]
	dy=ball.getCoords()[1]-ballToCheck.getCoords()[1]
	d=(dx**2+dy**2)**(1/2)
	if d!=0:
		sinA=dx/d
		cosA=dy/d
		if ballToCheck.getPulse()!=0:	
			dirNewX=cosA*ball.getDirection()[0]+sinA*ball.getDirection()[1]
			dirNewY=(-sinA)*ball.getDirection()[1]+cosA*ball.getDirection()[0]
			dirNewY=(-1.0)*dirNewY
			dirBackX=dirNewX*cosA-dirNewY*sinA
			dirBackY=dirNewX*sinA+dirNewY*cosA
			ball.setDirection([dirBackX,dirBackY])
			dirNewX=cosA*ball.getDirection()[0]+sinA*ball.getDirection()[1]
			dirNewY=(-sinA)*ball.getDirection()[1]+cosA*ball.getDirection()[0]
			dirNewY=(-1.0)*dirNewY
			dirBackX=dirNewX*cosA-dirNewY*sinA
			dirBackY=dirNewX*sinA+dirNewY*cosA
			ball.setDirection([dirBackX,dirBackY])
			tmp=ball.getPulse()
			ball.setPulse(ballToCheck.getPulse())
			ballToCheck.setPulse(tmp)
		else:
			pulseSumm=ball.getPulse()
			dirSummX=ball.getDirection()[0]
			dirSummY=ball.getDirection()[1]
			ballToCheck.setDirection([-sinA,-cosA])
			dirBall=calcBallDirection(-sinA,-cosA)
			signBall=calcBallSign(dirSummX,dirSummY,-sinA,-cosA)
			dirX=dirBall[0]*signBall[0]
			dirY=dirBall[1]*signBall[1]
			ball.setDirection([dirX,dirY])
			pulse=calcBallPulse(ball,ballToCheck,dirSummX,dirSummY,pulseSumm)
			ball.setPulse(pulse[0])
			ballToCheck.setPulse(pulse[1])
	else:
		print('ERROR in hitBallByBall.d=',d)

def hitBallByBallx2(ball,ballToCheck1,ballToCheck2):
	ball.setMove(False)
	ballToCheck1.setMove(False)
	ballToCheck2.setMove(False)
	pulseSumm=ball.getPulse()
	dirSummX=ball.getDirection()[0]
	dirSummY=ball.getDirection()[1]
	dx=ball.getCoords()[0]-ballToCheck1.getCoords()[0]
	dy=ball.getCoords()[1]-ballToCheck1.getCoords()[1]
	d=(dx**2+dy**2)**(1/2)
	if d!=0:
		sinA1=dx/d
		cosA1=dy/d
		ballToCheck1.setDirection([-sinA1,-cosA1])
		if dirSummX!=0:
			ballToCheck1.setPulse(abs(sinA1/dirSummX)*pulseSumm)
		else:
			ballToCheck1.setPulse(abs(cosA1/dirSummY)*pulseSumm)
	dx=ball.getCoords()[0]-ballToCheck2.getCoords()[0]
	dy=ball.getCoords()[1]-ballToCheck2.getCoords()[1]
	d=(dx**2+dy**2)**(1/2)
	if d!=0:
		sinA2=dx/d
		cosA2=dy/d
		ballToCheck2.setDirection([-sinA2,-cosA2])
		if dirSummX!=0:
			ballToCheck2.setPulse(abs(sinA2/dirSummX)*pulseSumm)
		else:
			ballToCheck2.setPulse(abs(cosA2/dirSummY)*pulseSumm)
	ball.setPulse(0)
	ball.setDirection([0,0])

def checkTimer():	
	global balls
	global mainField
	global listOfCheckedBalls
	flag=True
	t=0
	while flag:		
		i=0			
		t+=1 		
		k=100			
		while k>0:	
			for ball in balls:
				if ball.getPulse()>0.001 or ball.getPulseSpin()>0.001:
					i=0					
					ball.setMove(True)							
					moveTimer(ball,t)
					if k==1:										
						ball.setPulse(ball.getPulse()*0.91)			
						ball.setPulseSpin(ball.getPulseSpin()*0.90)
				else:
					i+=1											
					ball.setPulse(0)								 
					ball.setPulseSpin(0)
			for ball in balls:
				if ball.getPulse()>0.001 or ball.getPulseSpin()>0.001:							
					checkBoardHit(ball)								
					checkBallHit(ball)
			for ball in balls:
				if ball.getMove():
					dx=abs(int(ball.getCoords()[0])-int(ball.getCoordsGuess()[0]))
					dy=abs(int(ball.getCoords()[1])-int(ball.getCoordsGuess()[1]))
					ball.setCoords(ball.getCoordsGuess())
					if dx>0 or dy>0:
						ball.erase(mainField)						 
						ball.paint(mainField)
				else:
					#print('move set to: True')
					ball.setMove(True)
				#ball.setCoords(ball.getCoordsGuess())
			time.sleep(1/1000)
			k=k-1
			if listOfCheckedBalls:
				removeBallsFromListOfCheckedBalls()
			if i>22:
				k=-1
				flag=False
				messagebox.showinfo('Oops','OK.Ready to next push!')	

def moveTimer(ball,t):
	global frictionBallCloth
	global g
	dirX=ball.getDirection()[0]		
	dirY=ball.getDirection()[1]
	pulse=ball.getPulse()
###ВРАЩЕНИЕ!!!
#	f=frictionBallCloth	
#	pulseSpin=ball.getPulseSpin()
#	dx=abs(pulse*ball.getDirection()[0]-5/2*pulseSpin*ball.getSpin()[0])
#	dy=abs(pulse*ball.getDirection()[1]-5/2*pulseSpin*ball.getSpin()[1])
#	if  pulseSpin!=0.0 and (dx>0.001 or dy>0.001):
#		#print('pulseSpin=',round(pulseSpin,5),'dx=',round(dx,5),'dy=',round(dy,5))
#		vAbsolute=((dirX*pulse-5/2*ball.getSpin()[0]*pulseSpin)**(2)+(dirY*pulse-5/2*ball.getSpin()[1]*pulseSpin)**(2))**(1/2)
#		cosA=-(dirX*pulse-5/2*ball.getSpin()[0]*pulseSpin)/vAbsolute
#		cosB=-(dirY*pulse-5/2*ball.getSpin()[1]*pulseSpin)/vAbsolute
#		x1tmp=(t/100)*dirX*pulse
#		x2tmp=f*g*cosB*(t/100)**(2)/2
#		x=x1tmp-x2tmp
#		y=(t/100)*dirY*pulse-f*g*cosA*(t/100)**(2)/2
#		xNew=x
#		yNew=y
#	else:
#		xNew=(t/100)*dirX*pulse
#		yNew=(t/100)*dirY*pulse
###ВРАЩЕНИЕ!!!
	xNew=dirX*pulse/1000			
	yNew=dirY*pulse/1000
#	ball.setCoords([x,y])
	x=ball.getCoords()[0]+xNew
	y=ball.getCoords()[1]+yNew	
	ball.setCoordsGuess([x,y])	
	checkBallHitSimple(ball,[xNew,yNew])
###########################				CALCULATIONS FINISH
###########################				EVENTS START
def motionMain(event):
	global hitHold
	global stickHold
	global stick
	global mainField
	if holdHit:
		if not holdStick:
			calcFinishCoords(event.x,event.y,stick)
			calcDashedCoords(event.x,event.y,stick)
			stick.erase(mainField)
			stick.paint(mainField)

def clickBallLeft(event):
	global pointOfHit
	global ballFieldCoords
	ballField.delete(pointOfHit)
	ballField.delete(rotationAxle)
	x=event.x
	y=event.y
	pointOfHit=ballField.create_oval(x-20,y-20,x+20,y+20,fill='red',outline='red')
	ballFieldCoords=[x,y]

def clickMainLeft(event):
	global balls
	global stick
	global holdHit
	global holdStick
	global mainField
	if holdHit:
		if not holdStick:
			stick.erase(mainField)
			stick.setCoordsStart([event.x,event.y])
			x=stick.getCoordsFinish()[0]
			y=stick.getCoordsFinish()[1]
			calcFinishCoords(x,y,stick)
			stick.paint(mainField)
		else:
			holdStick=False
			clickMainLeft(event)
	else:
		balls[-1].erase(mainField)
		balls[-1].setCoords([event.x,event.y])
		balls[-1].setCoordsGuess([event.x,event.y])
		balls[-1].paint(mainField)

def clickMainRight(event):
	global stick
	global holdStick
	global holdHit
	global mainField
	if holdHit:
		if not holdStick:
			holdStick=True
			stick.erase(mainField)
			stick.paint(mainField)
		else:
			holdStick=False
			clickMainLeft(event)
	else:
		messagebox.showinfo('Oops','Place hit ball first')
###########################				EVENTS FINISH
###########################				BINDS
mainField.bind('<Motion>',motionMain)
mainField.bind('<Button-1>',clickMainLeft)
mainField.bind('<Button-3>',clickMainRight)

ballField.bind('<Button-1>',clickBallLeft)
###########################
########################### 			BUTTONS
buttHoldHit=Button(root,text='Hold hit',command=holdHit)
buttHoldHit.place(x=600,y=344,width=100,height=20)

buttHoldStick=Button(root,text='Hold stick',command=holdStick)
buttHoldStick.place(x=600,y=366,width=100,height=20)

buttPlaceHit=Button(root,text='Place hit',command=placeHit)
buttPlaceHit.place(x=600,y=300,width=100,height=20)

buttPlaceStick=Button(root,text='Place stick',command=placeStick)
buttPlaceStick.place(x=600,y=322,width=100,height=20)

buttPushStick=Button(root,text='Push stick',command=pushStick)
buttPushStick.place(x=600,y=388,width=100,height=20)

buttHoldHit=Button(root,text='Find min/max dist',command=FindDist)
buttHoldHit.place(x=600,y=410,width=100,height=20)

holdHit=False
holdStick=False
###########################
###########################				PROGRAMM START
i=0
for ball in balls:
#	ball.info()
	ball.setCoordsGuess(ball.getCoords())
	ball.paint(mainField)
	ball.setNumber(i)
	i+=1
root.mainloop()
###########################				PROGRAMM FINISH
