import RPi.GPIO as GPIO
from time import sleep
en=[5,25]
forw=[16,24]
back=[12,23]
speed=[0,0]
r_mult=0.5
l_mult=0.4
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
	speed[i].start(100) # duty cycle between 0 and 100

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
	print("Moving Forward")

def forward(l:float):
	cont_forw()
	sleep(l)
	for x in forw:
		GPIO.output(x, GPIO.LOW)
	sleep(0.5)

def reverse(l:float):	
	for x in back:
		GPIO.output(x, GPIO.HIGH)
	print("Moving backwards")
	sleep(l)
	for x in back:
		GPIO.output(x, GPIO.LOW)
	sleep(0.5)

def right(l:float):	
	GPIO.output(back[0], GPIO.HIGH)
	GPIO.output(forw[1], GPIO.HIGH)
	print("turning right")
	sleep(l*r_mult)
	GPIO.output(back[0], GPIO.LOW)
	GPIO.output(forw[1], GPIO.LOW)
	sleep(0.5)

def left(l:float):	
	GPIO.output(back[1], GPIO.HIGH)
	GPIO.output(forw[0], GPIO.HIGH)
	print("turning left")
	sleep(l*l_mult)
	GPIO.output(back[1], GPIO.LOW)
	GPIO.output(forw[0], GPIO.LOW)
	sleep(0.5)

def reset():
	for i in range(2):
		GPIO.output(back[i], GPIO.LOW)
		GPIO.output(forw[i], GPIO.LOW)
	sleep(0.5)

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

