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
stick=Stick()
listOfCheckedBalls=[]
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
fieldForse.place(x=750,y=850,width=100,height=20)

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
		balls.append(Ball([178+j*10-deltaX,178-i*10,0],[0,0,0],'red',mainField.create_oval(0,0,0,0)))
	deltaX+=5

balls.append(Ball([178,65,0],[0,0,0],'black',mainField.create_oval(0,0,0,0)))
balls.append(Ball([178,178,0],[0,0,0],'hot pink',mainField.create_oval(0,0,0,0)))
balls.append(Ball([178,356,0],[0,0,0],'blue',mainField.create_oval(0,0,0,0)))
balls.append(Ball([120,565,0],[0,0,0],'green',mainField.create_oval(0,0,0,0)))
balls.append(Ball([178,565,0],[0,0,0],'sienna',mainField.create_oval(0,0,0,0)))
balls.append(Ball([236,565,0],[0,0,0],'yellow',mainField.create_oval(0,0,0,0)))
balls.append(Ball([0,0,0],[0,0,0],'white',mainField.create_oval(0,0,0,0)))
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
		pass	
										#MAKE THIS!
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
			if distance<0:
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
	findTopPointDirection(x,y)					#RELATIVE!!!
	a=((x-100)**(2)+(y-100)**(2))**(1/2)
	v0=forse
	teta=0.13
	dM=float(1/3)
	h=a											#RECALC!!!!
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
		dirBallY=0
		dirBallX=1
		#print('1:calcBallDirection')
	if dirX!=0:
		dirBallY=dirY/dirX
	else:
		#print('2:calcBallDirection')
		dirBallX=0
		dirBallY=1
	d=(dirBallX**2+dirBallY**2)**(1/2)
	dirBallX=abs(dirBallX/d)
	dirBallY=abs(dirBallY/d)
	#print('3:calcBallDirection =1',dirBallX**2+dirBallY**2)
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

	pulseBall=(dirSummX*ballX+dirSummY*ballY)*pulseSumm
	pulseBallToCheck=(dirSummX*ballToCheckX+dirSummY*ballToCheckY)*pulseSumm

	#print('pulseBall=',round(pulseBall,5),'pulseBallToCheck=',round(pulseBallToCheck,5), 'pulseSumm=',round(pulseSumm,5))
	#print('X:',round(pulseBall*ballX,5),'+',round(pulseBallToCheck*ballToCheckX,5),'==',round(pulseSumm*dirSummX,5))
	#print('Y:',round(pulseBall*ballY,5),'+',round(pulseBallToCheck*ballToCheckY,5),'==',round(pulseSumm*dirSummY,5),'\n')
	return(pulseBall,pulseBallToCheck)

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

def refreshListOfCheckedBalls():
	global listOfCheckedBalls
	global balls
	if listOfCheckedBalls:
		for ball1 in balls:
			for ball2 in balls:
				dx=ball1.getCoords()[0]-ball2.getCoords()[0]
				dy=ball1.getCoords()[1]-ball2.getCoords()[1]
				distance=(dx**2+dy**2)**(1/2)
				if distance>10:
					b1N=ball1.getNumber()
					b2N=ball2.getNumber()
					for value in listOfCheckedBalls:
						if value[0]==b1N and value[1]==b2N:
							listOfCheckedBalls.remove(value)
							break
						elif value[1]==b1N and value[0]==b2N:
							listOfCheckedBalls.remove(value)
							break
						else:
							pass
				else:
					pass
	else:
		pass

def temp(ball,x,y):
	#global listOfCheckedBalls
	flag=False
	for ballToCheck in balls:
		if ball!=ballToCheck:
			ballNumber=ball.getNumber()
			ballToCheckNumber=ballToCheck.getNumber()
			deltaX=x-ballToCheck.getCoords()[0]
			deltaY=y-ballToCheck.getCoords()[1]
			distance=((deltaX)**2+(deltaY)**2)**(1/2)
			if distance<10:#and ballIsNotHitted(ballNumber,ballToCheckNumber):
				flag=True
				return(True)
				break
	if flag==False:
		return(False)
###########################				SIMPLE THINGS FINISH
###########################				CALCULATIONS START
def checkBallHit(ball,x,y):
	global balls
	global listOfCheckedBalls
	for ballToCheck in balls:
		if ball!=ballToCheck:
			ballNumber=ball.getNumber()
			ballToCheckNumber=ballToCheck.getNumber()
			deltaX=x-ballToCheck.getCoords()[0]
			deltaY=y-ballToCheck.getCoords()[1]
			distance=((deltaX)**2+(deltaY)**2)**(1/2)
			if distance<10 and ballIsNotHitted(ballNumber,ballToCheckNumber):
				#print('distance=',distance,'flag=',ballIsNotHitted(ballNumber,ballToCheckNumber))
				#print('listOfCheckedBalls=',listOfCheckedBalls)
				ball.setCoords([x,y])
				listOfCheckedBalls.append([ballNumber,ballToCheckNumber])
				if ball.getPulse()<ballToCheck.getPulse():
					tmp=ball
					ball=ballToCheck
					ballToCheck=tmp
				else:
					pass
				hitBallByBall(ball,ballToCheck)
			else:
				pass
		else:
			pass

def checkBoardHit(ball):
	if ball.getCoords()[0]<5 or ball.getCoords()[0]>350:
		x=ball.getDirection()[0]
		y=ball.getDirection()[1]
		ball.setDirection([-x,y])
	if ball.getCoords()[1]<5 or ball.getCoords()[1]>706:
		x=ball.getDirection()[0]
		y=ball.getDirection()[1]
		ball.setDirection([x,-y])

def hitBallByBall(ball,ballToCheck):
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
			x=ballToCheck.getCoords()[0]
			y=ballToCheck.getCoords()[1]
			#print('ballToCheckX=',ballToCheck.getDirection()[0],'ballToCheckY=',ballToCheck.getDirection()[1])
			#print('       ballX=',ball.getDirection()[0],'       ballY=',ball.getDirection()[1])
			#print('pB=',pulse[0],'pBTC=',pulse[1],'pS=',pulseSumm)
			#mainField.create_line(x,y,x+dirSummX*pulseSumm,y+dirSummY*pulseSumm,fill='white')
			#mainField.create_line(x,y,x-sinA*pulse[1],y-cosA*pulse[1],fill='black')
			#mainField.create_line(x-sinA*pulse[1],y-cosA*pulse[1],x-sinA*pulse[1]+dirX*pulse[0],y-cosA*pulse[1]+dirY*pulse[0],fill='red')
	else:
		pass
		#print('hitBallByBall d=0',ball.getColor(),'==',ball.getNumber(),ballToCheck.getColor(),'==',ballToCheck.getNumber())
		

def checkTimer():	
	global balls
	global mainField
	global listOfCheckedBalls
	flag=True
	t=0
	while flag:
		i=0
		t+=1
		for ball in balls:
			refreshListOfCheckedBalls()
			if ball.getPulse()>0.01 or ball.getPulseSpin()>0.01:
				i=0
				moveThread=Thread(target=moveTimer(ball,t))
				moveThread.setDaemon(True)
				moveThread.start()
				ball.setPulse(ball.getPulse()*0.91)
				ball.setPulseSpin(ball.getPulseSpin()*0.90)
				checkBoardHit(ball)
				ball.erase(mainField)
				ball.paint(mainField)
			else:
				i+=1
				ball.setPulse(0)
				ball.setPulseSpin(0)
		if i==22:
			flag=False

def moveTimer(ball,t):
	global frictionBallCloth
	global g
	flag=False
	f=frictionBallCloth
	pulse=ball.getPulse()
	pulseSpin=ball.getPulseSpin()
	dirX=ball.getDirection()[0]	
	dirY=ball.getDirection()[1]
	dx=abs(pulse*ball.getDirection()[0]-5/2*pulseSpin*ball.getSpin()[0])
	dy=abs(pulse*ball.getDirection()[1]-5/2*pulseSpin*ball.getSpin()[1])
#	if  pulseSpin!=0.0 and (dx>0.001 or dy>0.001):
#		#print('pulseSpin=',round(pulseSpin,5),'dx=',round(dx,5),'dy=',round(dy,5))
#		vAbsolute=((dirX*pulse-5/2*ball.getSpin()[0]*pulseSpin)**(2)+(dirY*pulse-5/2*ball.getSpin()[1]*pulseSpin)**(2))**(1/2)
#		cosA=-(dirX*pulse-5/2*ball.getSpin()[0]*pulseSpin)/vAbsolute
#		cosB=-(dirY*pulse-5/2*ball.getSpin()[1]*pulseSpin)/vAbsolute
#		x=(t/100)*dirX*pulse-f*g*cosB*(t/100)**(2)/2
#		y=(t/100)*dirY*pulse-f*g*cosA*(t/100)**(2)/2
#		xNew=x
#		yNew=y
#	else:
#		xNew=(t/100)*dirX*pulse
#		yNew=(t/100)*dirY*pulse
	xNew=t*dirX*pulse/100
	yNew=t*dirY*pulse/100
	x=ball.getCoords()[0]+xNew
	y=ball.getCoords()[1]+yNew
	checkBallHit(ball,x,y)
	#print('checkBallHit(ball,x,y)=',checkBallHit(ball,x,y))
	#mainField.create_line(ball.getCoords()[0],ball.getCoords()[1],x,y,fill=ball.getColor())
	ball.setCoords([x,y])
	#pulse*=(0.91)						#RECALC!
	#pulseSpin*=(0.90)					#RECALC!
	#ball.setPulse(pulse)
	#ball.setPulseSpin(pulseSpin)
	time.sleep(1/100)
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
		balls[-1].setCoords([event.x,event.y,0])
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
###########################           	BUTTONS
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

holdHit=False
holdStick=False
###########################
###########################				PROGRAMM START
i=0
for ball in balls:
	ball.paint(mainField)
	ball.setNumber(i)
	i+=1

root.mainloop()
###########################				PROGRAMM FINISH
