from variables import *
from classes import *
from sound import *
import pygame
import numpy
from math import sqrt
from display_im import *
from neighborhood import update
import time as time_module

clock = pygame.time.Clock()

plane = pygame.image.load("Images\\Avion.png")
plane = pygame.transform.scale(plane, (47, 30))

def turn_off_zone(universe : numpy.array, size : int, pos : tuple, size_screen : int) -> numpy.array:
		'''
		Principe. Cette fonction éteind les arbres en feu dans le carré centré sur pos et de taille size ** 2.
		Argument(s) :
			universe : l'univers sur lequel on travaille ;
			size : la taille du carré que l'on souhaite éteindre ;
			pos : la position du clique ;
			size_screen : la taille de l'écran en pixel.
		Résultat. L'univers mis à jour.
		'''
		# On commence par trouver la taille en pixel d'une cellule.
		size_square = size_screen[0]/max(universe.shape[0], universe.shape[1])
		
		# On itère sur toutes les cases.
		for i in range(universe.shape[0]):
			for j in range(universe.shape[1]):
				# On vérifie que la case se trouve dans le cercle centrée en pos.
				if sqrt((i - int(pos[0]/size_square))**2 + (j - int(pos[1]/size_square)) **2) <= size and universe[i, j].state == 1:
					# On change l'état de la case en "ayant presque brulée".
					universe[i, j].state = 3
		return universe

def display_water_firefighter(universe : numpy.array, size : int, pos : tuple, size_screen : int) -> None :
	'''
	Principe. Cette fonction affiche de l'eau sur les cases qui viennent d'être éteintes par eteindre_zone.
	Argument(s).
		universe : l'univers considéré ;
		size : la taille de la zone ;
		pose : la position de là où l'on veut afficher ;
		size_screen : la taille de l'écran.
	Résultat. Aucun.
	'''
	size_object = min(screen_size[0] / len(universe), screen_size[1] / len(universe[0]))
	size_square = size_screen[0] / max(universe.shape[0], universe.shape[1])
	
	for i in range(len(universe)) :
		for j in range(len(universe[0])) : # Boucles de traitement pour chaque élément.
			# Si la case est dans le cercle centré en pos, on affiche de l'eau dessus.
			if sqrt((i - int(pos[0]/size_square))**2 + (j - int(pos[1]/size_square)) **2) <= size :
				# On affiche une image d'eau sur les cases concernées.
				screen.blit(dico_image["water"], (i * size_object, j * size_object))

def mode_firefighter(universe : numpy.array, n_generations : int, size_screen : int, wind : bool, difficulty : int, filter: dict, prob : float) -> None :
	'''
	Principe. Cette fonction lance le mode de jeu pompier où le joueur essaie d'éteindre le feu.
	Argument(s). 
		universe : l'univers initialisé sur lequel on va itérer ;
		n_generations : le nombre de générations que l'on va itérer ;
		size_screen : la taille de l'écran en pixel ;
		wind : True si l'on prend en compte le vent, False sinon ; 
		difficulty : l'entier correspondant au niveau de diffculté (1, 2 ou 3) ;
		filter : le filtre à appliquer sur l'image ;
		prob : la probabilité de propagation générale.
	Résultat. Aucun.    
	'''
	# On regarde les coefficients multiplicatifs en fonction de la météo, et on importe les filtres correspondant.
	if difficulty == 0 :
		time_actualisation = 1
	elif difficulty == 1 :
		time_actualisation = 0.5
	else:
		time_actualisation = 0.24
		
	if 'type' in filter and filter['type'] == 'rain' :
		begin_sound_background("rain")
		begin_sound_background('fire')
	elif 'type' in filter and filter['type'] == 'drought' :
		begin_sound_background('drought')
	elif 'type' in filter and filter['type'] == 'rain_wind' :
		begin_sound_background('rain')
	else:
		begin_sound_background('fire')

	pos_plane = (0,0)
	water_restante=100
	size_screen = (500,550)
	i = 0
	pygame.mouse.set_visible(False) #On cache la souris
	time_animations = time_module.time()
	finished = False
	
	while ((i < n_generations) and (not finished)): #Boucle sur le nombre d'itérations
		
		time_wait = time_module.time()
		
		if water_restante <=90:
			water_restante = water_restante + 10
			
		while time_module.time() - time_wait < time_actualisation:
			#Animation de la pluie
			if "filtre" in filter and filter["type"] == 'rain' and time_module.time() - time_animations >=0.05:
				#Actualisation de la pluie
				time_animations = time_module.time()
				#On déplace le sprite de pluie
				filter["pos"] = (filter['pos'][0] ,((filter['pos'][1] + 2 )))
				#On affiche la carte
				display_universe_new_bar(universe, water_restante, filter)
				#On affiche l'avion
				screen.blit(plane, (pos_plane[0] -47/2, pos_plane[1] -30/2 ))
				#On met à jour l'écran
				pygame.display.flip()
				
			if "filtre" in filter and filter['type'] == 'vent'   and time_module.time() - time_animations >= 0.05:
				#Actualisation de la pluie
				time_animations = time_module.time()
				filter["pos"] = (filter['pos'][0] + 2,((filter['pos'][1] )))
				
				display_universe_new_bar(universe, water_restante, filter)
				screen.blit(plane, (pos_plane[0] -47/2, pos_plane[1] -30/2 ))
				pygame.display.flip()       
			if "filtre" in filter and filter['type'] == 'rain_wind'   and time_module.time() - time_animations >= 0.05:
				#Actualisation de la pluie
				time_animations = time_module.time()
				filter["pos"] = (filter['pos'][0] + 2,((filter['pos'][1] + 2)))
				
				display_universe_new_bar(universe, water_restante, filter)
				screen.blit(plane, (pos_plane[0] -47/2, pos_plane[1] -30/2 ))
				pygame.display.flip()       
				
			for event in pygame.event.get():
					if event.type == pygame.QUIT: #On quitte si la croix est cliquée
						pygame.quit()
					#Utilisation du canadair
					elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and water_restante >= 20: # Si le joueur clique sur la grille, on lance eteindre_zone
						x, y = event.pos
						#On joue un son d'eau
						begin_sound_point("water")
						#On éteind la zone concernée
						universe = turn_off_zone(universe, size = 3, pos = (x, y - 50), size_screen = size_screen)
						pygame.event.clear() #On clear la pile d'event pour éviter d'appeller plusieurs fois la fonction précédente et faire planter...
						#On affiche ensuite un effet d'eau
						display_water_firefighter(universe,size = 1, pos = event.pos, size_screen= size_screen)
						screen.blit(plane, (pos_plane[0] - 47/2, pos_plane[1] - 30/2 ))
						pygame.display.flip()
						pygame.time.wait(50)
						
						screen.blit(plane, (pos_plane[0] - 47/2, pos_plane[1] - 30/2 ))
						display_water_firefighter(universe,size = 2, pos = event.pos, size_screen= size_screen)
						pygame.display.flip()
						pygame.time.wait(50)
						
						display_water_firefighter(universe,size = 3, pos = event.pos, size_screen= size_screen)
						screen.blit(plane, (pos_plane[0] - 47/2, pos_plane[1] - 30/2 ))
						pygame.display.flip()
						pygame.time.wait(30)
						water_restante = water_restante - 20
						
					# On affiche une image de canadair sur la position de la souris
					elif event.type == pygame.MOUSEMOTION:
						pos_plane = event.pos
						#On réaffiche l'univers puis l'avion par dessus
						display_universe_new_bar(universe, water_restante, filter)
						screen.blit(plane, (pos_plane[0] -47/2, pos_plane[1] -30/2 ))
						pygame.display.flip()
						
		universe = update(universe, prob = prob, wind= wind) 
		display_universe_new_bar(universe, water_restante, filter) #On mets à jour l'écran
		screen.blit(plane, (pos_plane[0] -47/2, pos_plane[1] -30/2 ))
		pygame.display.flip()
		
		#On fait passer l'univers à la génération suivante
		
		finished = True
		for k in range(len(universe)) :
			for j in range(len(universe[0])) :
				if universe[k,j].state == 1:
					finished = False

		i = i + 1 # On compte l'itérations à laquelle on est.
	# On affiche le score.
	pygame.mouse.set_visible(True)    
	display_score(score_firefighter(universe))

def mode_normal(universe : numpy.array, n_generations : int, wind : bool, filter : dict, prob : float) -> None :
	'''
	Principe. Cette fonction lance simplement une simulation.
	Argument(s) :
		universe : l'univers de départ ;
		n_generations : le nombre de générations voulues ;
		wind : True si l'on prend en compte le vent, False sinon ;
		filter : le filtre à apliquer sur l'image ;
		prob : la probabilité générale de propagation.
	Résultat. Aucun.
	'''
	i = 0
	# On regarde les coefficients multiplicatifs en fonction de la météo, et on importe les filtres correspondant.
	if 'type' in filter and filter['type'] == 'rain':
		begin_sound_background("rain")
		begin_sound_background('fire')
	elif 'type' in filter and filter['type'] == 'drought':
		begin_sound_background('drought')
	elif 'type' in filter and filter['type'] == 'rain_wind':
		begin_sound_background('rain')
	else:
		begin_sound_background('fire')
		
	time_animations = time_module.time()
	
	while i < n_generations:
		time_wait = time_module.time()
		while time_module.time() - time_wait < 0.5 :
			if "filtre" in filter and filter["type"] == 'rain' and time_module.time() - time_animations >= 0.05 :
				# Actualisation de la pluie.
				time_animations = time_module.time()
				# On met à jour la position du sprite (avion, allumette ou le filtre).
				filter["pos"] = (filter['pos'][0] ,((filter['pos'][1] + 2 )))
				# On affiche l'univers avec le sprite (avion, allumette ou le filtre) actualisé.
				display_universe_new(universe, filter)
				pygame.display.flip()
				
			if "filtre" in filter and filter['type'] == 'vent'   and time_module.time() - time_animations >= 0.05:
				# Actualisation de la pluie.
				time_animations = time_module.time()
				filter["pos"] = (filter['pos'][0] + 2,((filter['pos'][1] )))
				
				display_universe_new(universe, filter)
				pygame.display.flip()       
				
			if "filtre" in filter and filter['type'] == 'rain_wind'   and time_module.time() - time_animations >= 0.05:
				# Actualisation de la pluie.
				time_animations = time_module.time()
				filter["pos"] = (filter['pos'][0] + 2,((filter['pos'][1] + 2)))
				
				display_universe_new(universe, filter)
				pygame.display.flip() 
					 
		for event in pygame.event.get() :
				# Si on clique sur quitter, la simulation s'arrête.
				if event.type == pygame.QUIT:
					pygame.quit()
					
				pygame.display.flip()
		# On affiche l'univers actuel, puis on mets à jour l'univers.
		display_universe_new(universe, filter)
		universe = update(universe, prob = prob, wind = wind)
		i = i + 1
		
def score_firefighter(universe : numpy.array)-> int:
	"""
	Principe. Cette fonction prend un univers et nous renvoit son score (on définit le score comme le pourcentage de végétation sauvée).
	Argument(s)
		universe : l'univers.
	Résultat. Le pourcentage.
	"""
	nb_burnt = 0
	possible_burning_number = 0
	# Calcul du pourcentage.
	for i in range(len(universe)) :
		for j in range(len(universe[0])) :
			if not isinstance(universe[i, j], Water) :
				possible_burning_number += universe[i, j].lifetime + 1
			nb_burnt += universe[i, j].time
	# Affichage du pourcentage
	score = 100 - ceil((nb_burnt/(possible_burning_number) * 100))
	
	return score