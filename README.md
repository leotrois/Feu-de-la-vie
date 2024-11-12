# Firefighter/feu de la vie

## Description

MVP : Ce projet a pour but de modéliser la propagation d'un feu, tout en ajoutant des interactions avec l'utilisateur. 

Pour lancer le jeu, lancer la fonction display_game dans le fichier main_pygame.py .

## Équipe

Dorian 
Claire 
Margaux 
Justin 
Guillaume 
Xavier 
Léo 

## Description des fichiers

### choice.py

Ce fichier rassemble les fonctions permettant  à l'utilisateur de choisir différents paramètres sur les caractéristiques de la simulation (taille de l'univers, types de départ de feu et nombre de générations à observer).

Liste des fonctions :

    display_prompt(x_topleft, y_topleft, text, font, font_color)
    Cette fonction affiche une consigne pour l'utilisateur.

    display_button_with_text(x_topleft, y_topleft, padding, text, font, font_color, edge_border)
    Cette fonction affiche un 'bouton' (un contour d'un rectangle et le rectangle qui servira de zone de sélection) avec du texte.

    change_selection(rectangle_to_select, *rectangles_to_unselect)
    Cette fonction affiche un 'bouton' en apparence 'sélectionné' et affiche les autres en apparence 'désélectionné'.

    mode_choice()
    Cette fonction affiche le sélecteur de mode qui permet de choisir entre le mode classique et le mode pompier.

    weather_choice()
    Cette fonction affiche le sélecteur de météo qui permet de choisir entre les météos 'temps clair', 'vent', 'pluie' et 'sécherresse'.

    difficulty_choice()
    Cette fonction affiche l'interface pour sélectionner le niveau de difficulté du jeu.

    generation_input()
    Cette fonction demande à l'utilisateur de rentrer le nombre de générations à observer, affiche une zone de saisie et renvoie l'entier saisi.

    size_choice()
    Cette fonction crée une interface graphique pour laisser l'utilisateur choisir parmi trois tailles d'univers.

    fire_choice()
    Cette fonction affiche les différents modèles de départ de feu et demande à l'utilisateur d'en choisir un.

### classes.py

Liste des classes :

	Les entités présentes dans la grille du jeu sont toutes issues d'une classe :

    Cell() : Une cellule a un état (qui par défaut à la création est non-brûlé), un temps depuis lequel la cellule brûle (forcé à zéro à la création), et deux facteurs (voir transmission_factor et reception_factor).

    Cette surclasse permet de définir les propriétés suivantes pour toutes les cellules :

		- state est un entier 0, 1, ou 2 qui correspond respectivement aux états sain, en cours de brûlure et brûlure ;

		- type est une chaîne de caractère indiquant le type de la cellule ;

    	- time est un entier correspondant au temps passé à brûler (en nombre d'itérations) ;

		- transmission_factor est un flottant entre 0 et 1 correspondant à un facteur pour pondérer la probabilité qu'une cellule particulière enflamme un voisin quelconque ;

		- recetion_factor est un flottant entre 0 et 1 correspondant à un facteur pour pondérer la probabilité qu'une cellule particulière se fasse enflammer par un voisin quelconque.

	Elle définit pour ses sous-classes la propriété suivante :

		- lifetime est un entier indiquant le temps de vie (nombre d'itérations) de la cellule.

	Ele définit les @setters sur :

		- state

		- time

    Elle définit aussi les méthodes suivantes :
        
		- is_burning explicite l'état entrain de brûler d'une cellule en retournant un booléen

		- is_burnt explicite l'état brûlé d'une cellule en retournant un booléen.
	
    On définit aussi des sous-classe de Cell() :

	Tree(Cell) : Sous-classe de Cell correspondant à des cellules de type 'arbre'. Un arbre est une cellule avec entre autre des coefficients de transmission et réception particuliers.

	La classe redéfinit les propriétés :
		 - type ;
		 - lifetime.

	Plain(Cell) : Sous-classe correspondant à des cellules de type 'plaine'. Un morceau de plaine est une cellule avec entre autre des coefficients de transmission et réception particuliers.
	
	La classe redéfinit les propriétés :
		 - type ;
		 - lifetime.
    
    Water(Cell) : Sous-classe correspondant à des cellules de type 'eau'. L'eau est une cellule qui ne brûle jamais.

	La classe redéfinit la propriété :
		- type.

	Elle redéfinit la méthode :
		- is_burnt -> False.

### display_im.py

Ce fichier sert à gérer les graphismes finaux, avec des images pour chaque case

Liste des fonctions :

    display_universe_new(universe, filter)
    Cette fonction affiche à l'écran l'univers stylisé.

    display_universe_new_bar(universe, water_remaining, filter)
    Cette fonction affiche l'univers et la barre d'eau restante, avec des images à la place des pixels.

	display_score(score)
	Cette fonction affiche le score par-dessus l'écran final à la fin du jeu.

    water_bar(percentage)
    Cette fonction dessine une barre d'eau restante.

    burnt_percentage(universe)
    Cette fonction affiche le taux de végétation brulée en haut à gauche de l'écran.

### gamemode.py

Ce fichier définit les différents modes de jeu de firefighter.

Liste des fonctions :

    turn_off_zone(universe, size , pos, size_ecran)
    Cette fonction sert à éteindre le feu sur une zone.

    display_water_firefighter(universe, size, pos, size_screen)
    Cette fonction affiche de l'eau sur les cases qui viennent d'être éteintes par eteindre_zone.

    mode_firefighter(universe,n_generations,size_screen, wind, rain, difficulty)
    Cette fonction lance le mode de jeu pompier où le joueur essaie d'éteindre le feu.

    mode_normal(universe, n_generations, wind, rain)
    Cette fonction lance simplement une simulation d'un feu.

    score_firefighter(universe)
    Cette fonction renvoie le score du joueur dans le mode pompier, le taux de forêt preservé.
    
### main_pygame.py

Ce fichier contient la fonction principal permettant de lancer la simulation.

Liste des fonctions :

    display_game()
    Cette fonction va lancer la simulation en appelant toutes les fonctions auxilliaires

### neighborhood.py

Ce fichier prend en charge la gestion des voisins d'un point et la propagation du feu d'un arbre à l'autre.

Liste des fonctions : 

    coord_neighbour_wind(size, x, y)
    Cette fonction renvoie les coordonnées des voisins de (x, y) ainsi que leurs voisins.

    coord_neighbour_without_wind(size, x, y)
    Cette fonction renvoie les coordonnées des voisins de la cellule de coordonnées (x, y).

    burn(universe, x, y, prob, wind)
    Cette fonction nous dit si la case encore intacte de coordonnées (x, y) prend feu.

    probability_without_wind(universe, c_neighbour, c_case, prob)
    Cette fonction renvoie la probabilité que c_voisin transmette du feu à c_case.

    probability_wind(universe, c_neighbour, c_case, prob)
    Cette fonction renvoie la probabilité que c_voisin transmette du feu à c_case lorsque il y a du vent.

    update(universe, prob, wind)
    Cette fonction met à jour l'univers.

### pygame_add_fire.py

Ce fichier contient les fonctions permettant d'ajouter du feu sur la map du jeu.

Liste des fonctions:

    placement_fire(size, starter, screen, position, universe)
    Cette fonction permet d'ajouter le feu dans l'univers aux coordonnées choisi.

    add_fire_click(size, starter, screen, universe)
    Cette fonction permet d'ajouter un départ de feu à l'écran en cliquant sur les boutons.

### sound.py

Ce fichier gère la génération de son pendant l'animation du jeu.

Liste des fonctions:

    begin_sound_point(sound_name)
    Cette fonction joue le son appelé pendant un temps donné définit dans la fonction.

    begin_sound_background(sound_name)
    Cette fonction joue le son appelé jusqu'à ce que la fenêtre soit fermée.

### start_fire.py

Ce fichier génère les univers et initialise le jeu avec un départ de feu.

Liste des fonctions :

    generation_2(size,p1,p2)
    Cette fonction génère un univers aléatoirement avec des forêts, des plaines et des lacs.

    generation_3(size,p1,p2)
    Cette fonction génère un univers aléatoirement avec une rivière, des forêts, des plaines et des lacs.

    generate_universe(size, cat)
	Cette fonction génère un univers de catégorie choisie.

	start_fire(universe, starter, x, y)
	Cette fonction ajoute du feu dans l'univers.

	initiate_game(size, starter, position, cat)
	Cette fonction lance le jeu, en créant un univers et en y ajoutant un départ de feu.

### test_functions.py

Ce fichier gère les fonctions de test de toutes les fonctions du projet.

Liste des fonctions : 

    test_choix_click()
    Cette fonctions teste les fonctions de choix utilisateur : mode, temps, taille de l'univers, difficulté, départ de feu, nombre de générations. 

    test_coord_neighbour_wind():
    On vérifie que la fonction coord_neighbour prend bien en compte les effets de bords.

    test_coord_neighbour_without_wind():
    On vérifie que la fonction coord_neighbour prend bien en compte les effets de bords.

    test_display_im():
    Cette fonction teste les différentes catégories de generate_universe et teste les affichages de ces univers.
    avec des filtres, ainsi que l'affichage de tous les objets et tous leurs états, ainsi que l'affichage de la barre d'eau et du score final.

    test_generate_universe()
    Cette fonction teste la création d'un univers avec la fonction generate_universe.

    test_initiate_game():
    Cette fonction teste la fonction initiate_game.

    test_is_burnt():
    On vérifie que après le temps de vie passé la case est bien considéré comme brulé.

    test_main():
    Cette fonction teste le jeu dans sa globalité.

    test_obj()
    Cette fonction teste les fonctions de définition des classes, et leurs méthodes. 

    test_probability_wind():
    On vérifie que les probabilités renvoyées par la fonction correspondent bien avec les probabilités attendues, et ce dans plusieurs cas.
    
    test_probability_without_wind():
    On vérifie que les probabilités renvoyées par la fonction correspondent bien avec les probabilités attendues, et ce dans plusieurs cas.

    test_start_fire():
    Cette fonction teste la fonction start_fire.

    test_update():
    Cette fonction appelle une fois la fonction pour vérifier l'absence d'erreurs. 
    Seulement on ne la teste pas bien à cause de la présence d'aléatoire.

### variables.py

Ce fichier contient les variables utiles pour tous les programmes.