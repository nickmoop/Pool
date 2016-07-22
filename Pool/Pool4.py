import random
import time
import math
from threading import *
from tkinter import *
from tkinter import messagebox
from ClassBall import Ball
from ClassBall import Stick
#окно.на мониторе с разрешением 1280х1024 самое оно
root=Tk()
root.resizable(False,False)
root.geometry("856x912+0+20")   		#355/710(1/5)
#константы и глобальные переменные
balls=[]
bitPlaced=False
stick=Stick()
listOfCheckedBalls=[]			#если расстояние между центрами > 10pix, то шаров в списке не должно быть
ballFieldCoords=[0,0]					#from clickBallLeft to hitBallByStick
topPoint=[0,0,0]						#top point of ball[x,y,z??]
frictionBallCloth=0.25					#const=0.25
frictionBallBoard=0.20					#const=0.20
frictionBallBall=0.03					#const=0.03
lossBallStick=0.13						#const=0.13
lossBallBoard=0.55						#const=0.55
g=9.809									#const=9.809
##########################				PAINT FIELD START
#текстовое окно для считывания силы удара.100 самое оптимальное.пока
forse=StringVar()
forse.set('100')
fieldForse=Entry(root,textvariable=forse)
fieldForse.place(x=550,y=450,width=100,height=20)
#коричневая рамка вокруг поля
board=Label(root,bg='brown')
board.place(x=85,y=85,width=384,height=742)
#скролбар для регулировки силы удара.в процессе, нигде не используется
										#MAKE THIS!
powerBar=Scrollbar(root)
powerBar.place(x=800,y=85,width=20,height=742)
										#MAKE THIS!
#мелкое поле с шаром(справа сверху окна)
ballField=Canvas(root)
ballField.place(x=560,y=85,width=200,height=200)
ballField.create_oval(10,10,190,190,fill='white',outline='black')
ballField.create_line(10,100,190,100,fill='black')					#horizontal line
ballField.create_line(100,10,100,190,fill='black')					#vertical line
#ballField.create_oval(99,99,101,101,fill='black',outline='black')	#center
pointOfHit=ballField.create_oval(0,0,0,0,fill='red',outline='red')
rotationAxle=ballField.create_line(0,0,0,0,fill='red')
#игровое поле+разметка
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
				#красные шары.расстояние между соседями = 0.увеличивал до 5pix всё равно слипаются. 
deltaX=0		#для увеличения изменять множитель при i,j
for i in range(1,6):
	for j in range(i):
		balls.append(Ball([178+j*10-deltaX,178-i*10,0],[0,0,0],'red',mainField.create_oval(0,0,0,0)))
	deltaX+=5
#цветные шары ставим вручную
balls.append(Ball([178,65,0],[0,0,0],'black',mainField.create_oval(0,0,0,0)))
balls.append(Ball([178,178,0],[0,0,0],'hot pink',mainField.create_oval(0,0,0,0)))
balls.append(Ball([178,356,0],[0,0,0],'blue',mainField.create_oval(0,0,0,0)))
balls.append(Ball([120,565,0],[0,0,0],'green',mainField.create_oval(0,0,0,0)))
balls.append(Ball([178,565,0],[0,0,0],'sienna',mainField.create_oval(0,0,0,0)))
balls.append(Ball([236,565,0],[0,0,0],'yellow',mainField.create_oval(0,0,0,0)))
balls.append(Ball([0,0,0],[0,0,0],'white',mainField.create_oval(0,0,0,0)))
###########################				MAKE LIST OF BALLS FINISH
###########################				SIMPLE THINGS START
#для одноименной кнопки
def placeHit():
	global holdHit
	holdHit=False
#для одноименной кнопки.если holdHit=False то нельзя разместить кий
def holdHit():
	global holdHit
	holdHit=True
#для одноименной кнопки
def placeStick():
	global holdStick
	holdStick=False
#для одноименной кнопки.если holdStick=False то нельзя ударить кием(кнопка pushStick)
def holdStick():
	global holdStick
	holdStick=True
#для одноименной кнопки.находит минимальное и максимально расстояние среди всех шаров
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
#считает координаты кия.чтобы был всегда определенной длины + нужное направление при любом положении мыши
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
#для одноименной кнопки.проверка значения силы и прочих условий.ф-я stickHitBall = попытка ударить шар
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
#красивые пунктирчики, показывающие куда предположительно полетит шар после удара кием.не используется
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
									#двигает кий,проверяет есть ли на пути шар,если есть то происходит	
def stickHitBall():					#удар hitBallByStick(направление,сила кия передаются нужному шару)
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
#рассчет поступательной, вращательной скорости + направления шара(вращательное и поступательное)
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
	h=a									#RECALC!!!!надо пересчитать.не влияет при выкл.вращении
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
		messagebox.showinfo('Oops','Bad hit:a>0.6')#кий скользит и шар катится непонятно куда
#для вычисления направления вращения
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
#для вычисления направления поступательного движения шара. вызов в hitBallByBall
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
#работает вместе с calcBallDirection.см выше.  вызов в hitBallByBall
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
#скорость шаров после столкновения. вызов в hitBallByBall
def calcBallPulse(ball,ballToCheck,dirSummX,dirSummY,pulseSumm):
	ballX=ball.getDirection()[0]
	ballY=ball.getDirection()[1]
	ballToCheckX=ballToCheck.getDirection()[0]
	ballToCheckY=ballToCheck.getDirection()[1]
	pulseBall=abs(dirSummX*ballX+dirSummY*ballY)*pulseSumm
	pulseBallToCheck=abs(dirSummX*ballToCheckX+dirSummY*ballToCheckY)*pulseSumm
	return(pulseBall,pulseBallToCheck)
#эти шары сталкивались прежде(ballNumber,ballToCheckNumber)?
#если сталкивались и отодвинулись вернет False.проверка в removeBallsFromListOfCheckedBalls().
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
#этот шар столкнулся с бортом?
def checkBoardHit(ball):
	if ball.getCoords()[0]<5 or ball.getCoords()[0]>350:
		x=ball.getDirection()[0]
		y=ball.getDirection()[1]
		ball.setDirection([-x,y])
	if ball.getCoords()[1]<5 or ball.getCoords()[1]>706:
		x=ball.getDirection()[0]
		y=ball.getDirection()[1]
		ball.setDirection([x,-y])
#между центрами каких либо шаров расстояние более 10pix? => стереть из списка близких шаров
def removeBallsFromListOfCheckedBalls():
	global balls
	global listOfCheckedBalls
	if listOfCheckedBalls:				#список столкнувшихся ранее шаров.заполняется в checkBallHit
		for value in listOfCheckedBalls:#перебираем все пары столкнувшихся ранее шаров
			x1=0
			y1=0
			x2=0
			y2=0
			for ball in balls:
				if value[0]==ball.getNumber():	#первое значение из пары равно любому из номеров шаров?
					x1=ball.getCoords()[0]
					y1=ball.getCoords()[1]
				if value[1]==ball.getNumber():	#второе значение из пары равно любому из номеров шаров?
					x2=ball.getCoords()[0]		#если оба условия выполнены, то есть 2 шара с номерами
					y2=ball.getCoords()[1]		#указанными в списке listOfCheckedBalls и 2 набора значени
			if x1!=0 and x2!=0:		#есть 2 набора значений != 0?
				distance=((x1-x2)**2+(y1-y2)**2)**(1/2)	#расстояние между центрами пары шаров из списка
				if distance>10.0:
					listOfCheckedBalls.remove(value)	#расстояние > 10 => удаляем пару шаров из списка ###########################				SIMPLE THINGS FINISH
###########################				CALCULATIONS START
#расстояние между Шаром и каким либо другим шаром<10?
def checkBallHit(ball):
	global balls
	global listOfCheckedBalls
	x=ball.getCoords()[0]
	y=ball.getCoords()[1]
	for ballToCheck in balls:
		if ball!=ballToCheck:	#чтобы не проверять шар сам с собой
			ballNumber=ball.getNumber()
			ballToCheckNumber=ballToCheck.getNumber()
			deltaX=x-ballToCheck.getCoords()[0]
			deltaY=y-ballToCheck.getCoords()[1]
			distance=((deltaX)**2+(deltaY)**2)**(1/2)
			if distance<10.0 and ballIsNotHitted(ballNumber,ballToCheckNumber):
				listOfCheckedBalls.append([ballNumber,ballToCheckNumber])#добавляе в список шаров,т.к d<10
				if ball.getPulse()<ballToCheck.getPulse():	#пусть у ball скорость будет всегда больше
					tmp=ball								#просто для удобства
					ball=ballToCheck
					ballToCheck=tmp
				else:
					pass
				hitBallByBall(ball,ballToCheck)		#ф-я для обработки столкновений	
			else:
				pass
		else:
			pass
#ф-я для обработки столкновений.первая половина-два подвижных шара,вторая-один подвижный
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
	else:
		pass
#двигает шары с параметром pulse != 0.при этом запускает проверки на столкновения,перерисовывает,"тянет" 
#время.когда не осталось подвижных шаров выводит сообщение
def checkTimer():	
	global balls
	global mainField
	global listOfCheckedBalls
	flag=True
	t=0
	while flag:		#flag=True => еще есть двужушиеся шары pulse>0 или pulseSpin>0
		i=0			#счетчик для неподвижных шаров(i==2200 => все шары неподвижны,22*100)
		t+=1 		#счетчик времени(для синхронности,вращения.пока не используется)
		k=100			
		while k>0:	#100 небольших перемещений = 1 t(пока не используется) 
			for ball in balls:
				if ball.getPulse()>0.001 or ball.getPulseSpin()>0.001:#неподвижный шар?почему 0.01 см ниже
					i=0												#i==0 =>есть подвижный шар
					xOld=ball.getCoords()[0]
					yOld=ball.getCoords()[1]
					moveTimer(ball,t)								#двигаем шар
					checkBoardHit(ball)								#столкнулся с бортом?
					checkBallHit(ball)								#столкнулся с любым другим шаром?
					removeBallsFromListOfCheckedBalls()				#расстояние да какого-то шара > 10pix?
					xNew=ball.getCoords()[0]
					yNew=ball.getCoords()[1]
					dx=abs(int(xOld)-int(xNew))
					dy=abs(int(yOld)-int(yNew))
					if dx>0 or dy>0:								#перерисовываем шар только если он 
						ball.erase(mainField)						#сдвинулся на целый пиксель,чтобы 
						ball.paint(mainField)						#не было сильного мерцания
					if k==1:										#изменение скорости за 1t:
						ball.setPulse(ball.getPulse()*0.91)			#правильное изменение скорости +
						ball.setPulseSpin(ball.getPulseSpin()*0.90) #крохотные перемещения
				else:
					i+=1											#+1 к счетчику неподвижных шаров.
					ball.setPulse(0)								#точно 0 не получается и происходит 
					ball.setPulseSpin(0)							#зацикливание.поэтому так
			time.sleep(1/10000)
			k=k-1													#k=1 => прошло время 1t
		if i==2200:
			listOfCheckedBalls=[]
			flag=False
			messagebox.showinfo('Oops','OK.Ready to next push!')			
#ф-я для перемещения шара без столкновений.рассчет влияния поступательного и 
#вращательного движения(закоментировано)
def moveTimer(ball,t):
	global frictionBallCloth
	global g	
	dirX=ball.getDirection()[0]		#ед.вектор направления([0]=х, [1]=у)
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
	xNew=dirX*pulse/1000			#маленький шаг~ (0.01-0.001)pix
	yNew=dirY*pulse/1000
	x=ball.getCoords()[0]+xNew
	y=ball.getCoords()[1]+yNew
	ball.setCoords([x,y])			#всё равно где задаю координаты, слипаются как бы не пробовал(
###########################				CALCULATIONS FINISH
###########################				EVENTS START
#для рисования кия
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
#для рисования красного круга на мелком шаре(справа сверху) + вычисления для вращения
def clickBallLeft(event):
	global pointOfHit
	global ballFieldCoords
	ballField.delete(pointOfHit)
	ballField.delete(rotationAxle)
	x=event.x
	y=event.y
	pointOfHit=ballField.create_oval(x-20,y-20,x+20,y+20,fill='red',outline='red')
	ballFieldCoords=[x,y]
#размещение битка(hit ball) или если биток размещен(hold hit) размещение начальной координаты кия
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
#финальная координата кия если биток(hit ball) размещен
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
#присваеваем клики мышкой к окнам(главное и с белым шариком справа вверху).не интересно
mainField.bind('<Motion>',motionMain)
mainField.bind('<Button-1>',clickMainLeft)
mainField.bind('<Button-3>',clickMainRight)

ballField.bind('<Button-1>',clickBallLeft)
###########################
########################### 			BUTTONS
#рисуем кнопки, присваиваем команды.не интересно
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
#рисует все шары, присваивает Number(по нему удобно отличать шары друг от друга).
i=0
for ball in balls:
	ball.paint(mainField)
	ball.setNumber(i)
	i+=1
root.mainloop()
###########################				PROGRAMM FINISH
