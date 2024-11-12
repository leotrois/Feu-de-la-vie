from variables import *
import numpy
from classes import *
from choice import *
from math import ceil

def display_universe_new(universe : numpy.array, filter : dict) -> None :
	'''
	Principe. Prend en argument une matrice d'objets de la classe Cell() et l'affiche avec pygame.
	Argument(s) :
		universe : l'univers que l'on souhaite afficher
		filter : un dictionnaire contenant des informations sur un hypothétique filtre, soit le dictionnaire est vide, soit il a les clés 
	Résultat. Aucun.'''
	size_object = min(screen_size[0]/len(universe), screen_size[1]/len(universe[0])) # Calcule la taille que prend un élément.
	for key, value in dico_image.items():
		value = pygame.transform.scale(value, (size_object+1, size_object+1))
		dico_image[key] = value
	for i in range(len(universe)) :
		for j in range(len(universe[0])) : # Boucle de traitement pour chaque élément
			if universe[i, j].state == 0 and isinstance(universe[i, j], Tree) : # Si c'est un arbre sain, on affiche l'image arbre sain.
				screen.blit(dico_image["tree"], (i*size_object, j*size_object))
			if universe[i, j].state == 0 and isinstance(universe[i, j], Plain) : # Si c'est une plaine saine, on affiche l'image plaine saine.
				screen.blit(dico_image["plain"], (i*size_object, j*size_object))
			if universe[i, j].state == 0 and isinstance(universe[i, j], Water) : # Si c'est de l'eau, on affiche l'image d'eau.
				screen.blit(dico_image["water"], (i*size_object, j*size_object))
			if universe[i, j].state == 1 and isinstance(universe[i, j], Tree) : # Si l'élément brûle, on affiche l'image d'arbre en feu.
				screen.blit(dico_image["tree_fire"], (i*size_object, j*size_object))
			if universe[i, j].state == 1 and isinstance(universe[i, j], Plain) : # Si l'élément brûle, on affiche l'image de plaine en feu.
				screen.blit(dico_image["plain_fire"], (i*size_object, j*size_object))
			if universe[i, j].state == 2: # Si l'élément est brûlé, on affiche l'image de plaine brulée.
				screen.blit(dico_image["dead_plain"], (i*size_object, j*size_object))
			if universe[i, j].state == 3: #Si l'élément est presque brulé mais ne brule plus, on affiche l'image d'arbre mort.
				screen.blit(dico_image["dead_tree"], (i*size_object, j*size_object))
	# On ajoute par dessus le pourcentage de la carte qui a brulé.
	burnt_percentage(universe)
	# On fait une disjonction de cas sur la présence ou non de filtre à ajouter par dessus l'image.
	if filter == {}:
		# S'il n'y a pas de filtre, on actualise seulement l'affichage.
		pygame.display.flip() # On actualise l'affichage.
	else:
		# S'il y a un filtre, on l'affiche à l'écran puis on met à jour l'écran.
		screen.blit(filter["filtre"], filter["pos"])
		pygame.display.flip()
	
def display_universe_new_bar(universe : numpy.array , water_remaining : int, filter : dict) -> None:
	'''
	Principe. La fonction affiche l'univers et une barre d'eau restante.
	Argument(s) :
		universe : l'univers que l'on veut afficher ;
		water_remaining : l'eau restante à afficher ;
		filter : un dictionnaire contenant des informations sur un hypothétique filtre, soit le dictionnaire est vide, soit il a les clés.
	Résultat. Aucun.
	'''
	size_object = min(screen_size[0]/len(universe), screen_size[1]/len(universe[0])) #Calcule la taille que prend un élément
	for  key, value in dico_image.items():
		value = pygame.transform.scale(value, (size_object +1, size_object + 1))
		dico_image[key]=value
	for i in range(len(universe)) :
		for j in range(len(universe[0])): # Boucle de traitement pour chaque élément.
			if universe[i, j].state == 0 and isinstance(universe[i, j], Tree): # Si c'est un arbre sain, on affiche l'image arbre sain.
				screen.blit(dico_image["tree"], (i*size_object, 50 + j*size_object))
			if universe[i, j].state == 0 and isinstance(universe[i, j], Plain): # Si c'est une plaine saine, on affiche l'image plaine saine.
				screen.blit(dico_image["plain"], (i*size_object,50 + j*size_object))
			if universe[i, j].state == 0 and isinstance(universe[i, j], Water): # Si c'est de l'eau, on affiche l'image d'eau.
				screen.blit(dico_image["water"], (i*size_object,50 + j*size_object))
			if universe[i, j].state == 1 and isinstance(universe[i, j], Tree): # Si l'élément brûle, on affiche l'image d'arbre en feu.
				screen.blit(dico_image["tree_fire"], (i*size_object,50 + j*size_object))
			if universe[i, j].state == 1 and isinstance(universe[i, j], Plain): # Si l'élément brûle, on affiche l'image de plaine en feu.
				screen.blit(dico_image["plain_fire"], (i*size_object,50 + j*size_object))
			if universe[i, j].state == 2: # Si l'élément est brûlé, on affiche l'image de plaine brulée.
				screen.blit(dico_image["dead_plain"], (i*size_object,50 + j*size_object))
			if universe[i, j].state == 3: # Si l'élément est presque brulé mais ne brule plus, on affiche l'image d'abre mort.
				screen.blit(dico_image["dead_tree"], (i*size_object,50 + j*size_object))
	# On fait une disjonction de cas sur la présence ou non de filtre
	# et on affiche la barre d'eau restante et le taux brulé.
	if filter == {} :
		# S'il n'y a pas de filtre, on actualise seulement l'affichage.
		pygame.draw.rect(screen, white, (0, 0, 500, 50))
		burnt_percentage(universe)
		water_bar(water_remaining)
		pygame.display.flip() # On actualise l'affichage.
	else :
		# S'il y a un filtre, on l'affiche à l'écran puis on met à jour l'écran.
		x, y = filter["pos"]
		screen.blit(filter["filtre"], (x, y + 50))

		pygame.draw.rect(screen, (255, 255, 255), (0, 0, 500, 50))
		water_bar(water_remaining)
		pygame.display.flip()

def display_score(score : float) -> None :
	'''
	Principe. Affiche le score par-dessus l'écran final à la fin du jeu.
	Argument(s) :
		score : le score en pourcentage de cellules brûlées.
	Résultat. Aucun.
	'''
	# Définition des coordonnées de la première ligne d'affichage.
	x_1 = 100
	y_1 = 100
	
	# Définition des coordonnées de la deuxième ligne d'affichage.
	x_2 = 100
	y_2 = 125

	# Définition des coordonnées du bouton de fin.
	x_validate = 100
	y_validate = 200
	
	# Texte à afficher sur les lignes et le bouton.
	display_1 = 'Score :'
	display_2 = str(int(score)) + '% de végétation sauvée'
	validate_display = 'Fin'

	# Utilisaiton d'un 'faux' 'bouton' pour chaque ligne, car la fonction déjà implémentée permet de tracer des rectangles. 
	display_button_with_text(x_1, y_1, padding, display_1, font, black, False)
	display_button_with_text(x_2, y_2, padding, display_2, font, black, False)
	# Récupération de la zone du bouton.
	validate_rectangle = display_button_with_text(x_validate, y_validate, padding, validate_display, font, black)
	
	pygame.display.flip()
	# Répéter indéfiniment :
	while True :
		# Récupération de la liste des évènements, et pour chaque évènement :
		for event in pygame.event.get() :
			# Si c'est un appui sur la croix rouge :
			if event.type == pygame.QUIT :
				# Quitter pygame.
				screen.fill(white)
				pygame.quit()
			# Sinon si c'est un clic de souris :
			elif event.type == pygame.MOUSEBUTTONDOWN :
				# Et s'il est dans la zone du bouton de fin :
				if validate_rectangle.collidepoint(event.pos) :
					# Quitter pygame.
					screen.fill(white)
					pygame.quit()
		pygame.display.flip()
  
def water_bar(percentage : int) -> None :
	"""
	Principe. Cette fonction dessine une barre qui représente la quantité d'eau disponible.
	Argument(s) :
		percentage : le pourcentage d'eau disponible.
	Résultat. Aucun."""
	if percentage > 100 :
		percentage = 100
	pygame.draw.rect(screen, (0,0,0), (10, 10, 480, 30))
	pygame.draw.rect(screen, (0,0,200), (15, 15, 4.7 * percentage, 20))
	pygame.draw.rect(screen, (50,50,50), (15 + 4.7 * percentage, 15, 470 - 4.7 * percentage, 20))

def burnt_percentage(universe : numpy.array) -> None :
	'''
	Principe. Cette fonction prend en argument un univers et affiche le taux de végétation brûlée en haut à gauche de l'écran.
	Argument(s) :
		universe : l'univers actuel.
	Résultat. Aucun.
	'''
	nb_burnt = 0
	possible_buring_number = 0
	# Calcul du pourcentage.
	for i in range(len(universe)):
		for j in range(len(universe[0])):
			if not isinstance(universe[i, j], Water):
				possible_buring_number += universe[i, j].lifetime + 1
			nb_burnt += universe[i, j].time
	# Affichage du pourcentage.
	text = str(ceil((nb_burnt / possible_buring_number *100))) + "%"
	text_surface = font.render(text, True, black)
	text_rectangle = text_surface.get_rect()
	text_rectangle.midleft = (440, 28)
	screen.blit(text_surface, text_rectangle.topleft)
