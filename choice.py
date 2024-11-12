from classes import *
from variables import *
from sound import *
import pygame

def display_prompt(x_topleft : int, y_topleft : int, text : str, font : pygame.font.Font, font_color : pygame.color.Color) -> None :
	'''
	Principe. Affiche une consigne.
	Argument(s) :
		x_topleft : abscisse du coin supérieur gauche de la consigne ;
		y_topleft : ordonnée du coin supérieur gauche de la consigne ;
		text : la consigne à afficher ;
		font : la police de caractère pour le texte ;
		font_color : la couleur pour le texte.
	Résultat. Aucun.
	'''
	# Création de la zone de texte.
	surface = font.render(text, True, font_color)
	# Mémorisation de la position.
	position = (x_topleft, y_topleft)
	# Affichage.
	screen.blit(surface, position)

def display_button_with_text(x_topleft : float, y_topleft, padding : int, text : str, font : pygame.font.Font, font_color : pygame.color.Color, edge_border : bool = True) -> pygame.rect.Rect :
	'''
	Principe. Affiche un 'bouton' (un contour d'un rectangle et le rectangle qui servira de zone de sélection) avec du texte.
	Argument(s) :
		x_topleft : abscisse du coin supérieur gauche du contour du bouton ;
		y_topleft : ordonnée du coin supérieur gauche du contour du bouton ;
		padding : espacement entre le texte et le contour du bouton ;
		text : le texte à afficher sur le bouton ;
		font : la police de caractère pour le texte ;
		font_color : la couleur pour le texte ;
		edge_border : True si l'on souhaite une bordure, False sinon.
	Résultat. Le rectangle qui correspondra à la zone sur laquelle cliquer pour appuyer sur le bouton.
	'''
 
	# Création d'une zone d'écriture.
	surface = font.render(text, True, font_color)
 
	# Création d'un rectangle positionné où on le souhaite, dont les dimensions sont celles de l'écriture un peu agrandie.
	rectangle = pygame.Rect(x_topleft, y_topleft, surface.get_width() + padding, surface.get_height() + padding)
 
	# Dessin du fond du rectangle.
	pygame.draw.rect(screen, white, rectangle, 0)
 
	# Dessin de l'écriture sur l'écran sur un point légèrement décalé du point supérieur gauche (point de référence pour le dessin) du rectangle.
	screen.blit(surface, (x_topleft + padding / 2, y_topleft + padding / 2))
 
	# Si l'on souhaite une bordure :
	if edge_border :
	 
		# Dessin de la bordure noire du rectangle.
		pygame.draw.rect(screen, black, rectangle, 2)
  
	# Mise à jour de l'écran.
	pygame.display.flip()

	# Le rectangle sera utilisé dans le code pour la gestion des évènements (détection que l'on clique dans la zone).
	return rectangle

def change_selection(rectangle_to_select : pygame.rect.Rect, *rectangles_to_unselect : pygame.rect.Rect) -> None :
	'''
	Principe. Affiche un 'bouton' en apparence 'sélectionné' et affiche les autres en apparence 'désélectionné'.
	Argument(s) :
		rectangle_to_select : le rectangle du bouton à sélectionner :
		*rectangles_to_unselect : les rectangles des boutons à désélectionner.
	Résultat. Aucun.
	'''
 
	# 'Sélection' du premier rectangle.
	pygame.draw.rect(screen, green, rectangle_to_select, 4)

	# Pour chaque rectangle à déselectionner :
	for rectangle_to_unselect in rectangles_to_unselect :
	 
		# On efface le rectangle en repassant par-dessus en blanc (couleur de l'écran).
		pygame.draw.rect(screen, white, rectangle_to_unselect, 4)
  
		# Puis on redessine le rectangle
		pygame.draw.rect(screen, black, rectangle_to_unselect, 2)

def mode_choice() -> str :
	'''
	Principe. Affiche le sélecteur de mode qui permet de choisir entre le mode classique et le mode pompier.
	Argument(s). Aucun.
	Résultat. Une chaîne de caractère qui indique le nom du mode choisi : 'classic' ou 'firefighter'.
	'''
	# Variables utiles au positionnement des rectangles.
	x_rectangles = 50
	y_prompt = 50
	y_classic_mode_rectangle = 150
	y_firefighter_mode_rectangle = 200
	y_validate_button = 300

	# Affichage d'une consigne.
	prompt = 'Choisissez le mode de jeu.'
	display_prompt(x_rectangles, y_prompt, prompt, font, black)
	
	# Affichage des différents boutons.
	classic_mode_button_text = 'Mode simulation'
	classic_mode_rectangle = display_button_with_text(x_rectangles, y_classic_mode_rectangle, padding, classic_mode_button_text, font, black)
	
	firefighter_mode_button_text = 'Mode jeu'
	firefighter_mode_rectangle = display_button_with_text(x_rectangles, y_firefighter_mode_rectangle, padding, firefighter_mode_button_text, font, black)

	# choice contiendra le choix final.
	choice = None
 
	# Drapeau pour afficher le bouton de validation.
	displayed_validate_button = False

	# Répéter en boucle :
	while True :
		# Lecture des évènements, et pour chaque évènement :
		for event in pygame.event.get() :
			# Si c'est un clic sur la croix rouge :
			if event.type == pygame.QUIT :
				# Il s'arrête à la fin de cette boucle non bornée.
				pygame.quit()
			# Si c'est un clic de souris :
			elif event.type == pygame.MOUSEBUTTONDOWN :
				# S'il est au niveau du bouton 'mode classique' :
				if classic_mode_rectangle.collidepoint(event.pos) :
					# Dans le cas où le mode classique n'est pas déjà défini en tant que choix :
					if not choice == 'classic' :
						# On le définit en tant que tel.
						choice = 'classic'
						# On repasse le rectangle du mode classique en vert épais pour faire comprendre à l'utilisateur qu'il est sélectionné, on 'efface' le rectangle du mode pompier, et on le retrace en noir fin.
						change_selection(classic_mode_rectangle, firefighter_mode_rectangle)
					# Si le bouton 'Valider' n'était pas affiché :
					if not displayed_validate_button :
						# On l'affiche.
						validate_rectangle = display_button_with_text(x_rectangles, y_validate_button, padding, 'Valider', font, black)
						# Et on indique qu'il est affiché.
						displayed_validate_button = True
				# Sinon, s'il est au niveau du bouton 'mode pompier', on procède de même.
				elif firefighter_mode_rectangle.collidepoint(event.pos) :
					if not choice == 'firefighter' :
						choice = 'firefighter'
						change_selection(firefighter_mode_rectangle, classic_mode_rectangle)
					if not displayed_validate_button :
						validate_rectangle = display_button_with_text(x_rectangles, y_validate_button, padding, 'Valider', font, black)
						displayed_validate_button = True
				elif displayed_validate_button and validate_rectangle.collidepoint(event.pos) :
					return choice
					pygame.quit()
			pygame.display.flip()

def weather_choice() -> list :
	'''
	Principe. Affiche le sélecteur de météo qui permet de choisir entre les météos 'temps clair' (pas d'altérations), 'vent', 'pluie' et 'sécherresse'. 'pluie' et 'sécheresse' sont exclusifs l'un de l'autre.
	Argument(s). Aucun.
	Résultat. Liste de deux informations :
		- indice 0 : True pour du vent, False sinon ;
		- indice 1 : 'rain' pour de la pluie, 'drought' pour de la sécheresse, '' sinon.
	'''
	x_rectangles = 50
	y_prompt = 50
	y_clear_mode_rectangle = 150
	y_wind_mode_rectangle = 200
	y_rain_mode_rectangle = 250
	y_drought_mode_rectangle = 300
	y_validate_button = 400

	prompt = 'Choisissez la météo.'
	display_prompt(x_rectangles, y_prompt, prompt, font, black)

	clear_mode_button_text = 'Temps clair'
	clear_mode_rectangle = display_button_with_text(x_rectangles, y_clear_mode_rectangle, padding, clear_mode_button_text, font, black)

	wind_mode_button_text = 'Vent'
	wind_mode_rectangle = display_button_with_text(x_rectangles, y_wind_mode_rectangle, padding, wind_mode_button_text, font, black)

	rain_mode_button_text = 'Pluie'
	rain_mode_rectangle = display_button_with_text(x_rectangles, y_rain_mode_rectangle, padding, rain_mode_button_text, font, black)

	drought_mode_button_text = 'Sécheresse'
	drought_mode_rectangle = display_button_with_text(x_rectangles, y_drought_mode_rectangle, padding, drought_mode_button_text, font, black)

	choice = [None, False, '']
	displayed_validate_button = False

	while True :
		for event in pygame.event.get() :
			if event.type == pygame.QUIT :
				pygame.quit()
			elif event.type == pygame.MOUSEBUTTONDOWN :
				if clear_mode_rectangle.collidepoint(event.pos) :
					if not choice[0] :
						choice = [True, False, '']
						change_selection(clear_mode_rectangle, wind_mode_rectangle, rain_mode_rectangle, drought_mode_rectangle)
					if not displayed_validate_button :
						validate_rectangle = display_button_with_text(x_rectangles, y_validate_button, padding, 'Valider', font, black)
						displayed_validate_button = True
				elif wind_mode_rectangle.collidepoint(event.pos) :
					if not choice[1] :
						choice[1] = True
						choice[0] = False
						change_selection(wind_mode_rectangle ,clear_mode_rectangle)
					if not displayed_validate_button :
						validate_rectangle = display_button_with_text(x_rectangles, y_validate_button, padding, 'Valider', font, black)
						displayed_validate_button = True
				elif rain_mode_rectangle.collidepoint(event.pos) :
					if not choice[2] == 'rain' :
						choice[2] = 'rain'
						choice[0] = False
						change_selection(rain_mode_rectangle, clear_mode_rectangle, drought_mode_rectangle)
					if not displayed_validate_button :
						validate_rectangle = display_button_with_text(x_rectangles, y_validate_button, padding, 'Valider', font, black)
						displayed_validate_button = True
				elif drought_mode_rectangle.collidepoint(event.pos) :
					if not choice[2] == 'drought' :
						choice[2] = 'drought'
						choice[0] = False
						change_selection(drought_mode_rectangle, clear_mode_rectangle, rain_mode_rectangle)
					if not displayed_validate_button :
						validate_rectangle = display_button_with_text(x_rectangles, y_validate_button, padding, 'Valider', font, black)
						displayed_validate_button = True
				elif displayed_validate_button and validate_rectangle.collidepoint(event.pos) :
					return choice[1 :]
			pygame.display.flip()

def difficulty_choice() -> int :
	'''
	Principe. Affiche l'interface pour sélectionner le niveau de difficulté du jeu.
	Argument(s). Aucun.
	Résultat. Un entier naturel : 0 pour le niveau facile, 1 pour le niveau moyen et 2 pour le niveau difficile.
	'''
	x_rectangles = 50
	y_prompt = 50
	y_easy_mode_rectangle = 150
	y_medium_mode_rectangle = 200
	y_difficult_mode_rectangle = 250
	y_validate_button = 350

	prompt = 'Choisissez votre difficulté.'
	display_prompt(x_rectangles, y_prompt, prompt, font, black)

	easy_mode_button_text = 'Facile'
	easy_mode_rectangle = display_button_with_text(x_rectangles, y_easy_mode_rectangle, padding, easy_mode_button_text, font, black)

	medium_mode_button_text = 'Moyen'
	medium_mode_rectangle = display_button_with_text(x_rectangles, y_medium_mode_rectangle, padding, medium_mode_button_text, font, black)

	difficult_mode_button_text = 'Difficile'
	difficult_mode_rectangle = display_button_with_text(x_rectangles, y_difficult_mode_rectangle, padding, difficult_mode_button_text, font, black)

	choice = None
	displayed_validate_button = False

	while True :
		for event in pygame.event.get() :
			if event.type == pygame.QUIT :
				pygame.quit()
			elif event.type == pygame.MOUSEBUTTONDOWN :
				if easy_mode_rectangle.collidepoint(event.pos) :
					if not choice == 0 :
						choice = 0
						change_selection(easy_mode_rectangle, medium_mode_rectangle, difficult_mode_rectangle)
					if not displayed_validate_button :
						validate_rectangle = display_button_with_text(x_rectangles, y_validate_button, padding, 'Valider', font, black)
						displayed_validate_button = True
				elif medium_mode_rectangle.collidepoint(event.pos) :
					if not choice == 1 :
						choice = 1
						change_selection(medium_mode_rectangle, easy_mode_rectangle, difficult_mode_rectangle)
					if not displayed_validate_button :
						validate_rectangle = display_button_with_text(x_rectangles, y_validate_button, padding, 'Valider', font, black)
						displayed_validate_button = True
				elif difficult_mode_rectangle.collidepoint(event.pos) :
					if not choice == 2 :
						choice = 2
						change_selection(difficult_mode_rectangle, easy_mode_rectangle, medium_mode_rectangle)
					if not displayed_validate_button :
						validate_rectangle = display_button_with_text(x_rectangles, y_validate_button, padding, 'Valider', font, black)
						displayed_validate_button = True
				elif displayed_validate_button and validate_rectangle.collidepoint(event.pos) :
					return choice
			pygame.display.flip()
			
def generation_input() -> int :
	'''
	Principe. Demande à l'utilisateur de choisir un nombre de générations sur lesquelles l'univers évoluera.
	Argument(s). Aucun.
	Résultat. Le nombre de générations choisi.
	'''
	x_rectangles = 50
	y_text = screen_size[1] // 2
	y_prompt = screen_size[1] // 2 - 50
	prompt = 'Choisissez le nombre de générations.'
	
	# Variable mémorise le texte entré.
	text = ''
	# saisie_active = True

	# Initialisation du temps pour le rafraichissement de la page
	clock = pygame.time.Clock()

	# Rectangle qui servira à 'effacer' la zone de saisie pour afficher la zone de saisie mise à jour.
	erasing_rectangle = pygame.rect.Rect(x_rectangles, y_text, 100, 30)

	# Affichage de l'invite.
	display_prompt(x_rectangles, y_prompt, prompt, font, black)

	# Répéter en boucle
	while True :
		# Lecture des évènements, et pour chaque évènement :
		for event in pygame.event.get() :
			# Si c'est un appui sur la croix rouge :
			if event.type == pygame.QUIT :
				# On quitte le jeu.
				pygame.quit()
			# Si c'est un appui sur le clavier :
			elif event.type == pygame.KEYDOWN :
				# Si la touche appuyée est la touche 'entrée' et que la longueur du texte est non nulle (entrée non vide) : 
				if event.key == pygame.K_RETURN and len(text) > 0 :
					# On renvoie le nombre entré sous forme de nombre entier.
					return int(text)
				# Sinon si la touche appuyée est la touche 'retour' et que la longueur du texte est non nulle (au moins un caractère dans la zone de texte) :
				elif event.key == pygame.K_BACKSPACE and len(text) > 0 :
					# On efface le dernier caractère.
					text = text[:-1]
				# Sinon si c'est une touche numérique :
				elif event.unicode.isdigit() :
					# On ajoute ce chiffre dans la chaine de caractère en entrée.
					text += event.unicode

		# Effacement de la zone de saisie pour la reconstruction.
		pygame.draw.rect(screen, white, erasing_rectangle, 0)

		# Affichage d'un 'faux' 'bouton' pour récupérer le rectangle associé au texte, et affichage du texte entré.
		rectangle = display_button_with_text(x_rectangles, y_text, padding, text, font, black, False)
		
		# Modification de la largeur de ce rectangle pour en tracer un grand noir.
		rectangle.width = 100
		# Limite de la vitesse de rafraîchissement.
		clock.tick(1000)
		# Dessin du grand rectangle qui sert à matérialiser la zone de saisie.
		pygame.draw.rect(screen, black, rectangle, 2)
		# Rafraîchissement de l'écran.
		pygame.display.flip()

		# Limite de la vitesse de rafraîchissement.
		clock.tick(10)

def size_choice() -> int :
	'''
	Principe. Cette fonction crée une interface graphique pour laisser l'utilisateur choisir parmi trois tailles d'univers.
	Argument(s). Aucun.
	Résultat. La taille de l'univers choisi.
	'''
	x_rectangles = 50
	y_prompt = 50
	y_small_mode_rectangle = 150
	y_medium_mode_rectangle = 200
	y_large_mode_rectangle = 250
	y_validate_button = 350

	prompt = 'Choisissez la taille de l\'univers.'
	display_prompt(x_rectangles, y_prompt, prompt, font, black)

	small_mode_button_text = 'Petit'
	small_mode_rectangle = display_button_with_text(x_rectangles, y_small_mode_rectangle, padding, small_mode_button_text, font, black)

	medium_mode_button_text = 'Moyen'
	medium_mode_rectangle = display_button_with_text(x_rectangles, y_medium_mode_rectangle, padding, medium_mode_button_text, font, black)

	large_mode_button_text = 'Grand'
	large_mode_rectangle = display_button_with_text(x_rectangles, y_large_mode_rectangle, padding, large_mode_button_text, font, black)

	small_size = 20
	medium_size = 50
	large_size = 70

	choice = None
	displayed_validate_button = False

	while True :
		for event in pygame.event.get() :
			if event.type == pygame.QUIT :
				pygame.quit()
			elif event.type == pygame.MOUSEBUTTONDOWN :
				if small_mode_rectangle.collidepoint(event.pos) :
					if not choice == small_size :
						choice = small_size
						change_selection(small_mode_rectangle, medium_mode_rectangle, large_mode_rectangle)
					if not displayed_validate_button :
						validate_rectangle = display_button_with_text(x_rectangles, y_validate_button, padding, 'Valider', font, black)
						displayed_validate_button = True
				elif medium_mode_rectangle.collidepoint(event.pos) :
					if not choice == medium_size :
						choice = medium_size
						change_selection(medium_mode_rectangle, small_mode_rectangle, large_mode_rectangle)
					if not displayed_validate_button :
						validate_rectangle = display_button_with_text(x_rectangles, y_validate_button, padding, 'Valider', font, black)
						displayed_validate_button = True
				elif large_mode_rectangle.collidepoint(event.pos) :
					if not choice == large_size :
						choice = large_size
						change_selection(large_mode_rectangle, small_mode_rectangle, medium_mode_rectangle)
					if not displayed_validate_button :
						validate_rectangle = display_button_with_text(x_rectangles, y_validate_button, padding, 'Valider', font, black)
						displayed_validate_button = True
				elif displayed_validate_button and validate_rectangle.collidepoint(event.pos) :
					return choice
			pygame.display.flip()
				
def fire_choice() -> str :
	'''
	Principe. Affiche une interface graphique pour le choix du départ de feu.
	Argument(s). Aucun.
	Résultat. La chaîne de caractère correspondant au départ de feu choisi.	
	'''

	# Définition du catalogue des départs.
	starters = {'cigarette': [[0, 0, 0], [0, 1, 0], [0, 0, 0]], 'gasoline' : [[0, 1, 0], [1, 1, 1], [0, 1, 0]], 'bush' : [[0, 0, 0], [1, 1, 0], [1, 1, 0]]}

	# Définition d'un dictionnaire de traduction.
	translate = {'cigarette' : 'cigarette', 'gasoline' : 'essence', 'bush' : 'broussaille'}
	
	# Dictionnaire  qui référencera comme clés les noms des départs de feu, et comme valeur la position du rectangle permettant de les choisir.
	rectangles = {}

	# Taille à donner à l'espacement des rectangles affichant les boutons.
	rectangle_size = screen_size[1] / (len(starters) + 2)

	# Affichage de la consigne.
	x_rectangles = 50
	y_prompt = 20
	prompt = "Choisissez le type de feu de départ."
	display_prompt(x_rectangles, y_prompt, prompt, font, black)

	# Ordonnée du bouton 'Valider'.
	y_validate = screen_size[1] - 50

	# Dimensions des images élémentaires des départs de feu.
	height = 35
	width = 35

	# Affichage des différents 'boutons' des départs de feu.
	k = 0
	for name in starters.keys() :
		k += 1
		y_rectangle = k * rectangle_size
		rectangles[name] = display_button_with_text(x_rectangles, y_rectangle, padding, translate[name], font, black)
	pygame.display.flip()
	
	# Réglage vertical pour centrer les images des départs de feu verticalement avec les boutons.
	y_setting = rectangles['gasoline'].height

	# choice contiendra la chaîne de caractère du nom du départ de feu choisi.
	choice = ''
	displayed_validate_button = False

	# Rectangle visant à recouvrir les images pour les 'effacer'.
	erasing_rectangle = pygame.rect.Rect(screen_size[0] // 2, 60, screen_size[0] // 2, screen_size[1] - 60) 

	# Répéter en boucle :
	while True :
		# Lecture des évènements, on attend un clic sur l'un des rectangles des noms des départs de feu.
		for event in pygame.event.get() :
			# Si c'est un clic sur la croix rouge :
			if event.type == pygame.QUIT :
				# On quitte le jeu.
				pygame.quit()
			# Sinon si c'est un clic de souris :
			elif event.type == pygame.MOUSEBUTTONDOWN :
				# Pour chaque départ de feu :
				for name in rectangles.keys() :
					# Si le clic se situe dans sur le bouton :
					if rectangles[name].collidepoint(event.pos) :
						# Si le choix n'était pas déjà configuré sur ce départ de feu :
						if not choice == name :
							# On le configure.
							choice = name
							# Pour chaque départ de feu :
							for other_rectangle in rectangles.values() :
								# Si ce n'est pas le départ de feu que l'on vient de sélectionner :
								if other_rectangle != rectangles[name] :
									# On sélectionne le nouveau en déselection celui-ci.
									change_selection(rectangles[name], other_rectangle)
							# On efface l'ancienne image de départ de feu.
							pygame.draw.rect(screen, white, erasing_rectangle, 0)
							# On joue le son du départ de feu.
							begin_sound_point(name)
							# Pour chaque ligne du départ de feu.
							for i in range(3) :
								# Pour chaque colonne du départ de feu.
								for j in range(3) :
									# Si le départ de feu est fait pour que cette case soit en saine :
									if not starters[name][i][j] :
										# On prend une image d'arbre sain.
										image = healthy_tree_image
									# Sinon :
									else :
										# On prend une image d'arbre en feu.
										image = fire_tree_image
									# Adaptation la taille de l'image.
									image = pygame.transform.scale(image, (width, height))
									# Affichage de l'image pour le feu de cigarette à coté de la zone de sélection
									screen.blit(image, (rectangles[name].topleft[0] + 200 + i * width, rectangles[name].topleft[1] + j * height - 1.5 * height + y_setting / 2))
						if not displayed_validate_button :
							validate_rectangle = display_button_with_text(x_rectangles, y_validate, padding, 'Valider', font, black)
							displayed_validate_button = True
				if displayed_validate_button and validate_rectangle.collidepoint(event.pos) :
					return choice
		pygame.display.flip()