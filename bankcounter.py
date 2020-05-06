import requests
from time import sleep
import json
import RPi.GPIO as GPIO

#Buttons GPIO pin definition
btnSira = 21
btnGise1 = 20
btnGise2 = 16
#Sira Display GPIO pins definition
dispSira = [12, 7, 8, 25, 24, 23, 18]
#Gise1 Display GPIO pins definition
dispGise1 = [2, 3, 4, 17, 27, 22, 10]
#Gise2 Display GPIO pins definition
dispGise2 = [9, 11, 5, 6, 13, 19, 26]

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#GPIO Pins Setup
GPIO.setup(btnSira, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(btnGise1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(btnGise2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
for g in dispSira:
    GPIO.setup(g, GPIO.OUT)
for g in dispGise1:
    GPIO.setup(g, GPIO.OUT)
for g in dispGise2:
    GPIO.setup(g, GPIO.OUT)

#Preparation for Server
URLread = "http://192.168.137.1:80/read"
URLwrite = "http://192.168.137.1:80/write"
PARAMS = {'id':0}

# [A, B, C, D, E, F, G] on 8-segment display electronic component
rakamlar = [ [0,0,0,0,0,0,1] ,
	[1,0,0,1,1,1,1],
	[0,0,1,0,0,1,0],
	[0,0,0,0,1,1,0],
	[1,0,0,1,1,0,0],
	[0,1,0,0,1,0,0],
	[0,1,0,0,0,0,0],
	[0,0,0,1,1,1,1],
	[0,0,0,0,0,0,0],
	[0,0,0,0,1,0,0]
]

try:
	# Let's loop forever:
	while True:

		#Requests periodically for asking if a token has taken
		try:
			PARAMS = {'id':1}
			r = requests.get(URLread, PARAMS, timeout=2)
			data = json.loads(r.text)
		except requests.exceptions.ConnectionError:
			print(r.status_code)

		gise1 = int(data['gise1'])
		gise2 = int(data['gise2'])
		sira = int(data['sira'])
		
		i=0	
		for g in dispSira:
			GPIO.output(g, rakamlar[sira][i])
			i += 1
			
		i=0
		for g in dispGise1:
			GPIO.output(g, rakamlar[gise1][i])
			i += 1
			
		i=0
		for g in dispGise2:
			GPIO.output(g, rakamlar[gise2][i])
			i += 1


		if GPIO.input(btnSira) == GPIO.HIGH:
			sleep(0.5)
			if sira != 9:
				sira += 1
				for g in dispSira:
					for i in range(7):
						GPIO.output(g, rakamlar[sira][i])
					
		if GPIO.input(btnGise1) == GPIO.HIGH:
			sleep(0.5)
			if gise1!=9 or gise2!=9:
				if sira>gise1:
					if sira>gise2:
						if gise1<gise2:
							gise1 = gise2+1
						else:
							gise1 += 1
						for g in dispGise1:
							for i in range(7):
								GPIO.output(g, rakamlar[gise1][i])
					
		if GPIO.input(btnGise2) == GPIO.HIGH:
			sleep(0.5)
			if gise2!=9 or gise1!=9:
				if sira>gise2:
					if sira>gise1:
						if gise2<gise1:
							gise2 = gise1+1
						else:
							gise2 += 1
						for g in dispGise2:
							for i in range(7):
								GPIO.output(g, rakamlar[gise2][i])

		try:
			#if pressed, updates the database on server
			PARAMS = {'id':id, 'sira':sira, 'gise1':gise1, 'gise2':gise2}
			r = requests.get(URLwrite, PARAMS, timeout=2)
		except requests.exceptions.ConnectionError:
			print(r.status_code)

	sleep(0.5)

except KeyboardInterrupt:
    print('Shutting down')
    GPIO.cleanup()
