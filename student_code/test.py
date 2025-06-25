import RPi.GPIO as GPIO
import time

GPIO.setmode (GPIO.BCM)
GPIO.setup (3, GPIO.OUT)
a=0

while a<5:
	GPIO.output(3, True)
	time.sleep(1)
	GPIO.output(3, False)
	time.sleep(1)
	a+=1
	print(a)