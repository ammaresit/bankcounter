import requests
from time import sleep
import json
import RPi.GPIO as GPIO

#Butonlarin GPIO pin Tanimlamasi
btnSira = 21
btnGise1 = 20
btnGise2 = 16
#Sira Display GPIO pin Tanimlamasi
dispSira = [12, 7, 8, 25, 24, 23, 18]
#Gise1 Display GPIO pin Tanimlamasi
dispGise1 = [2, 3, 4, 17, 27, 22, 10]
#Gise2 Display GPIO pin Tanimlamasi
dispGise2 = [9, 11, 5, 6, 13, 19, 26]

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#GPIO Pin Kurulumlarinin Yapilmasi ve Tamamen Sonuk Baslatilmalari
GPIO.setup(btnSira, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(btnGise1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(btnGise2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
for g in dispSira:
    GPIO.setup(g, GPIO.OUT)
    #GPIO.output(g, 1)
for g in dispGise1:
    GPIO.setup(g, GPIO.OUT)
    #GPIO.output(g, 1)
for g in dispGise2:
    GPIO.setup(g, GPIO.OUT)
    #GPIO.output(g, 1)

#Web Server icin hazirlik
URLread = "http://192.168.137.1:80/read"
URLwrite = "http://192.168.137.1:80/write"
PARAMS = {'id':0}

# [A, B, C, D, E, F, G]
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

#ilk siradaki kayit icin (zaten 1 adet kayit olacak. Baska kayit olursa bu sayiyi onun idsine gore duzenle!)
id = 1


try:
	# Let's loop forever:
	while True:

		#Telefondan sira alma islemi oldu mu olmadi mi kontrolunu yapmak icin surekli servera istek atar

		try:
			PARAMS = {'id':id}
			r = requests.get(URLread, PARAMS, timeout=2)
			data = json.loads(r.text)
		except requests.exceptions.ConnectionError:
			print(r.status_code)

		#burasi en son kaldirilacak
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
			print("sira'ya basildi")
			sleep(0.5)
			if sira != 9:
				sira += 1
				#dispSira'nin rakamini bir arttir
				for g in dispSira:
					for i in range(7):
						GPIO.output(g, rakamlar[sira][i])
					
		if GPIO.input(btnGise1) == GPIO.HIGH:
			print("gise1'e basildi")
			sleep(0.5)
			if gise1!=9 or gise2!=9:
				if sira>gise1:
					if sira>gise2:
						if gise1<gise2:
							gise1 = gise2+1
						else:
							gise1 += 1
						#dispGise1'in rakamini bir arttir
						for g in dispGise1:
							for i in range(7):
								GPIO.output(g, rakamlar[gise1][i])
					
		if GPIO.input(btnGise2) == GPIO.HIGH:
			print("gise2'ye basildi")
			sleep(0.5)
			if gise2!=9 or gise1!=9:
				if sira>gise2:
					if sira>gise1:
						if gise2<gise1:
							gise2 = gise1+1
						else:
							gise2 += 1
						#dispGise2'nin rakamini bir arttir
						for g in dispGise2:
							for i in range(7):
								GPIO.output(g, rakamlar[gise2][i])

		try:
			#butonlara basildi ise bilgileri alip serverda update yapacak istegi gonderir!
			PARAMS = {'id':id, 'sira':sira, 'gise1':gise1, 'gise2':gise2}
			r = requests.get(URLwrite, PARAMS, timeout=2)
		except requests.exceptions.ConnectionError:
			print(r.status_code)


	sleep(0.5)

except KeyboardInterrupt:
    print('Shutting down')
    GPIO.cleanup()
