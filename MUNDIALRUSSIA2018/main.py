import time
import random
import threading
from equipo import Equipo

semaforo = threading.Lock() # Inicializamos el semaforo

partido_transcurso = True
tiempo = 0
team1_end = False
team2_end = False

def jugar(Equipo1, Equipo2, duracion):
	starttime = time.time()
	global tiempo, partido_transcurso, team1_end, team2_end
	partido_transcurso = True
	team1_end = False
	team2_end = False
	tiempo = 0

	# Busco las probabilidades de encajar por cada equipo
	prob_encajar_eq1 = Equipo1.probabilidad_encajar()
	prob_encajar_eq2 = Equipo2.probabilidad_encajar()

	def jugar_equipo1(defensa_rival, duracion):
		global tiempo, team1_end

		while int(tiempo) < duracion:
			time.sleep(1 - ((time.time() - starttime) % 1))
			
			semaforo.acquire() # Bloqueo P(Critica)
			
			if Equipo1.hacer_pases():
				Equipo1.shoot(defensa_rival)
			tiempo = time.time() - starttime # Se incrementa el tiempo transcurrido
			
			semaforo.release() # Libero V(Critica)
		
		team1_end = True
		end_game() # Para comprobar si ambos hilos terminaron

	def jugar_equipo2(defensa_rival, duracion):
		global tiempo, team2_end

		while int(tiempo) < duracion:
			time.sleep(1 - ((time.time() - starttime) % 1))
			
			semaforo.acquire() # Bloqueo
			
			if Equipo2.hacer_pases():
				Equipo2.shoot(defensa_rival)
			tiempo = time.time() - starttime # Se incrementa el tiempo transcurrido
			
			semaforo.release() # Libero		
		
		team2_end = True
		end_game()

	def end_game():
		global partido_transcurso, team1_end, team2_end
		if team1_end and team2_end:
			partido_transcurso = False # Flag que indica el final del partido

	# Inicializo los hilos, en target paso el metodo a ejecutar.
	# en args paso las probabilidades de encajar del equipo rival
	hilo_equipo1 = threading.Thread(name = 'hilo_eq1', target = jugar_equipo1, args = (prob_encajar_eq2,duracion,))
	hilo_equipo2 = threading.Thread(name = 'hilo_eq2', target = jugar_equipo2, args = (prob_encajar_eq1,duracion,))

	# Se ejecutan ambos hilos
	hilo_equipo1.start()
	hilo_equipo2.start()


def sorteo_saque(equipo1, equipo2):
	lista = [equipo1, equipo2]
	ganador_sorteo = random.choice(lista)

	if ganador_sorteo.nombre == equipo1.nombre:
		equipos = {'gano_balon': equipo1, 'gano_cancha': equipo2}
	else:
		equipos = {'gano_balon': equipo2, 'gano_cancha': equipo1}

	return equipos

def prediccion_partido(equipo1, equipo2):
	prob_ganar_equipo1 = (equipo1.prob_ganar * 100) + random.randint(0,25)
	prob_ganar_equipo2 = (equipo2.prob_ganar * 100) + random.randint(0,25)

	if prob_ganar_equipo1 > prob_ganar_equipo2:
		return equipo1.nombre
	elif prob_ganar_equipo1 == prob_ganar_equipo2:
		return random.choice([equipo1.nombre, equipo2.nombre])
	else:
		return equipo2.nombre

def lista_equipos():
	equipos = [('Alemania','ALEMANIA'),('Arabia Saudi','ARABIASAUDI'),('Argentina','ARGENTINA'),('Australia','AUSTRALIA'),
	('Belgica','BELGICA'),('Brasil','BRASIL'),('Colombia','COLOMBIA'),('Costa Rica','COSTA RICA'),
	('Croacia','CROACIA'),('Dinamarca','DINAMARCA'),('Egipto','EGIPTO'),('Espana','ESPANA'),
	('Francia','FRANCIA'),('Inglaterra','INGLATERRA'),('Iran','IRAN'),('Islandia','ISLANDIA'),
	('Japon','JAPON'),('Marruecos','MARRUECOS'),('Mexico','MEXICO'),('Nigeria','NIGERIA'),('Panama','PANAMA'),
	('Peru','PERU'),('Polonia','POLONIA'),('Portugal','PORTUGAL'),('Republica de corea','REPUBLICA DE COREA'),
	('Rusia','RUSIA'),('Senegal','SENEGAL'),('Serbia','SERBIA'),('Suecia','SUECIA'),('Suiza','SUIZA'),
	('Tunez','TUNEZ'),('Uruguay','URUGUAY')]
	return equipos

def lista_fechas():
	fechas_partidos = [('14/06/18','14/06/18'),('15/06/18','15/06/18'),('16/06/18','16/06/18'),('17/06/18','17/06/18'),
	('18/06/18','18/06/18'),('19/06/18','19/06/18'),('20/06/18','20/06/18'),('21/06/18','21/06/18'),
	('22/06/18','22/06/18'),('28/06/18','28/06/18'),('30/06/18','30/06/18'),('01/07/18','01/07/18'),
	('02/07/18','02/07/18'),('03/07/18','03/07/18'),('06/07/18','06/07/18'),('07/07/18','07/07/18'),
	('10/07/18','10/07/18'),('11/07/18','11/07/18'),('14/07/18','14/07/18'),('15/07/18','15/07/18')]
	return fechas_partidos

def lista_horas():
	horas_partido = [('14:00','14:00'),('15:00','15:00'),('16:00','16:00'),('17:00','17:00'),('18:00','18:00'),
	('19:00','19:00'),('20:00','20:00'),('21:00','21:00'),('22:00','22:00')]
	return horas_partido

def lista_etapas():
	return [('Fase de Grupos','Fase de Grupos'),('8vos de Final','8vos de Final'),('4tos de Final','4tos de Final'),
    ('Semifinales','Semifinales'),('Tercer puesto','Tercer puesto'),('Final','Final')]

def lista_formaciones():
	formaciones = [('4-4-2','4-4-2'),('4-3-3','4-3-3'),('4-2-3-1','4-2-3-1'),('4-3-1-2','4-3-1-2'),('3-4-3','3-4-3'),
	('5-3-1','5-3-1')]
	return formaciones
