import time
import RPi.GPIO as GPIO
GPIO.cleanup()
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
TRIG = [4,27,13]
ECHO = [17,22,26]
for i in range(3): 
	GPIO.setup(TRIG[i],GPIO.OUT)
	GPIO.setup(ECHO[i],GPIO.IN)
	GPIO.output(TRIG[i], False)

def dist(i:int)-> float:
	GPIO.output(TRIG[i], True)
	time.sleep(0.00001)
	GPIO.output(TRIG[i], False)
	while GPIO.input(ECHO[i]) == 0:
		pulse_start = time.time()
	while GPIO.input(ECHO[i]) == 1:
		pulse_end = time.time()
	pulse_duration = pulse_end - pulse_start
	distance = pulse_duration * 17150
	distance = round(distance, 2)
	return distance
	

if __name__=="__main__":
	print('[press ctrl+c to end the test]')
	time.sleep(2)
	try: # Main program loop
		while True:
			for i in [0,1,2]:				
				print('{}: {}cm'.format(i,dist(i)))
				time.sleep(1)
				
	# Scavenging work after the end of the program
	except KeyboardInterrupt:
		print('Test end!')
	finally:
		GPIO.cleanup()
