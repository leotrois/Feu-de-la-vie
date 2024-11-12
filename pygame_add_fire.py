import pygame 
from variables import *
from start_fire import *
from neighborhood import *
from display_im import *
import time as time_module

def placement_fire(size : tuple, starter : str, position: tuple, universe : np.array) -> np.array:
	"""
	Principe. Cette fonction permet d'ajouter le feu dans l'univers aux coordonnées choisies
	Argument(s) :
		size : dimension de l'univers ;
		starter : type de départ de feu ;
		position : position de placement ;
		universe : carte du jeu.
	Résultat. La carte du jeu avec le départ de feu placé.
	"""
	size_square = 500 / max(size[0], size[1])
	universe = start_fire(universe, starter, int(position[0]/size_square), int(position[1]/size_square))
	return universe

def add_fire_click(size : tuple, starter : str, screen : pygame.surface.Surface, universe : np.array, filter : dict) -> None:
	"""
	Principe. Cette fonction permet d'ajouter un départ de feu à l'écran en cliquant sur l'écran.
	Argument(s) :
		size : dimension de l'univers ;
		starter : type de départ de feu ;
		screen : ce qui est affiché à l'écran ;
		universe : map du jeu ;
		filter : filtre à afficher sur l'image.
	Résultat. Aucun.
	"""
	flag = True
	screen.fill(white)
	display_universe_new(universe, filter = filter)
	
	matchstick = pygame.image.load("Images\\Allumette.png")
	matchstick =  pygame.transform.scale(matchstick, (40,40))
	
	pygame.mouse.set_visible(False)
	
	time_animations = time_module.time()
	pos_matchstick = (0,0)
	
	while flag :
			if "filtre" in filter and filter["type"] == 'rain' and time_module.time() - time_animations >=0.05:
				# Actualisation de la pluie.
				time_animations = time_module.time()
				# On met à jour la position du sprite.
				filter["pos"] = (filter['pos'][0] ,((filter['pos'][1] + 2 )))
				# On affiche l'univers avec le sprite actualisée.
				display_universe_new(universe, filter)
				screen.blit(matchstick, (pos_matchstick[0] -40/2, pos_matchstick[1] -40/2 ))
				pygame.display.flip()
			if "filtre" in filter and filter['type'] == 'vent'   and time_module.time() - time_animations >= 0.05:
				# Actualisation de la pluie.
				time_animations = time_module.time()
				filter["pos"] = (filter['pos'][0] + 2,((filter['pos'][1] )))
				display_universe_new(universe, filter)
				screen.blit(matchstick, (pos_matchstick[0] -40/2, pos_matchstick[1] -40/2 ))
				pygame.display.flip()       
			if "filtre" in filter and filter['type'] == 'rain_wind' and time_module.time() - time_animations >= 0.05 :
				# Actualisation de la pluie.
				time_animations = time_module.time()
				filter["pos"] = (filter['pos'][0] + 2,((filter['pos'][1] + 2)))
				display_universe_new(universe, filter)
				screen.blit(matchstick, (pos_matchstick[0] -40/2, pos_matchstick[1] -40/2 ))
				pygame.display.flip()
			for event in pygame.event.get() :
				if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 : 
					pygame.mouse.set_visible(True)
					return placement_fire(size, starter, event.pos, universe) # Génération de l'univers.
				elif event.type == pygame.MOUSEMOTION: # On déplace une allumette qui sert de curseur.
						pos_matchstick = event.pos
						display_universe_new(universe, filter= filter)
						screen.blit(matchstick, (pos_matchstick[0] -40/2, pos_matchstick[1] -40/2 ))
						pygame.display.flip()
				if event.type == pygame.QUIT :
					flag = False
				pygame.display.flip()
	pygame.quit()