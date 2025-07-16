import RPi.GPIO as GPIO
import math
from time import sleep, asctime
en=[5,25]
forw=[16,24]
back=[12,23]
speed=[0,0]
r_mult=0.5
l_mult=0.45
r_speed_const=75

s_r=100
s_l=100
# in4 = 23
# in3 = 24
# enB = 25
# in2 = 12
# in1 = 16
# enA = 5
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
#set in1/in2/en as output
for i in range(2):
	GPIO.setup(en[i],GPIO.OUT)
	GPIO.setup(forw[i],GPIO.OUT)
	GPIO.setup(back[i],GPIO.OUT)
	#stop motor
	GPIO.output(forw[i],GPIO.LOW)
	GPIO.output(back[i],GPIO.LOW)
	speed[i]=GPIO.PWM(en[i],100) # Set frequency to 100 hz
speed[0].start(75) # duty cycle between 0 and 100 #rechts
speed[1].start(100) #links

# GPIO.setup(in2,GPIO.OUT)
# GPIO.setup(enA,GPIO.OUT)
# GPIO.setup(in3,GPIO.OUT)
# GPIO.setup(in4,GPIO.OUT)
# GPIO.setup(enB,GPIO.OUT)
# GPIO.output(in1,GPIO.LOW)
# GPIO.output(in2,GPIO.LOW)
# GPIO.output(in3,GPIO.LOW)
# GPIO.output(in4,GPIO.LOW)
# Set speed
# speedA=GPIO.PWM(enA,100) # Set frequency to 100 hz
# speedA.start(100) # duty cycle between 0 and 100
# speedB=GPIO.PWM(enB,100) 
# speedB.start(100) 

def cont_forw():
	reset()
	for x in forw:
		GPIO.output(x, GPIO.HIGH)
	print(f"[{asctime()}]: Vorwärts")

def cont_back():
	reset()
	for x in back:
		GPIO.output(x, GPIO.HIGH)
	print(f"[{asctime()}]: Rückwärts")

def cont_right():
	reset()
	GPIO.output(back[0], GPIO.HIGH)
	GPIO.output(forw[1], GPIO.HIGH)
	print(f"[{asctime()}]: Drehung nach Rechts")

def cont_left():
	reset()
	GPIO.output(back[1], GPIO.HIGH)
	GPIO.output(forw[0], GPIO.HIGH)
	print(f"[{asctime()}]: Drehung nach Links")


def speed_r(val:int):
	global s_r,speed
	value=math.floor(val*r_speed_const*0.01)
	s_r=value
	if value >= r_speed_const:
		speed[0].ChangeDutyCycle(r_speed_const)
		s_r=100
	elif value <= 0:
		speed[0].ChangeDutyCycle(0)
		s_r=0
	else:
		speed[0].ChangeDutyCycle(value)
		s_r=math.floor(value/0.75)
	print(f"[{asctime()}]: Geschwindigkeit Rechts: {s_r}")

def speed_l(value:int):
	global s_l,speed
	if value >= 100:
		speed[1].ChangeDutyCycle(100)
		s_l=100
	elif value <= 0:
		speed[1].ChangeDutyCycle(0)
		s_l=0
	else:
		speed[1].ChangeDutyCycle(value)
		s_l=value
	print(f"[{asctime()}]: Geschwindigkeit Links: {s_l}")

def get_speed_r():
	return s_r
def get_speed_l():
	return s_l


def forward(l:float):
	cont_forw()
	sleep(l)
	for x in forw:
		GPIO.output(x, GPIO.LOW)
	sleep(0.5)

def reverse(l:float):
	cont_back()
	sleep(l)
	for x in back:
		GPIO.output(x, GPIO.LOW)
	sleep(0.5)

def right(l:float):
	cont_right()
	sleep(l*r_mult)
	GPIO.output(back[0], GPIO.LOW)
	GPIO.output(forw[1], GPIO.LOW)
	sleep(0.5)

def left(l:float):
	cont_left()
	sleep(l*l_mult)
	GPIO.output(back[1], GPIO.LOW)
	GPIO.output(forw[0], GPIO.LOW)
	sleep(0.5)

def reset():
	for i in range(2):
		GPIO.output(back[i], GPIO.LOW)
		GPIO.output(forw[i], GPIO.LOW)
	sleep(0.5)

def re_speed():
	speed_r(100)
	speed_l(100)

if __name__=="__main__":
	print('[press ctrl+c to end the test]')
	a=0
	try:
		while(a<5):
			forward(1)
			right(2)
			reverse(1)
			left(2)
			a=a+1
		# Scavenging work after the end of the program
	except KeyboardInterrupt:
		print('Test end!')
	finally:
		GPIO.cleanup()

