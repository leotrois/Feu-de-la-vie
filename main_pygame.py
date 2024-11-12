from variables import *
from start_fire import *
from choice import *
from display_im import *
from neighborhood import *
from gamemode import *
from pygame_add_fire import *

def display_game() :
    """
    Principe. Fonction principale qui va lancer la simulation en appelant toutes les fonctions auxilliaires.
    Argument. Aucun.
    Résultat. Aucun.
    """
    # On choisit le mode de jeu.
    game_mode = mode_choice()
    screen.fill(white)
    # On choisit les conditions météo de la simulation.
    wind, rain = weather_choice()
    screen.fill(white)
    # On demande à l'utilisateur de choisir la taille de la carte.
    size = size_choice()
    size = (size, size)
    screen.fill(white)
    # On fait une disjonction de cas suivant le mode de jeu choisi, on ne demande pas à l'utilisateur
    # de placer le feu dans le mode où il doit chercher à l'éteindre...
    if rain == "drought" and not wind :
        # On importe le filtre en lui donnant le bon type, ce qui permettra de l'animer en fonction.
        filter = {"filtre" : pygame.image.load("Images\\filtre_jaune.png").convert_alpha(), "pos" : (0, 0), "type" : 'drought'}
        # On modifie la probabilité générale qui dépend. 
        prob = 0.6
    elif rain == "drought" and wind:
        filter = {"filtre" : pygame.image.load("Images\\vent_secheresse.png").convert_alpha(), "pos" : (-9000 ,0), "type" : 'vent'}
        prob = 0.6
    elif rain == "rain" and not wind:
        filter = {"filtre" : pygame.image.load("Images\\pluie.png").convert_alpha(), "pos" : (0,-9000), "type" : 'rain'}
        prob = 0.17
    elif rain == "rain" and wind :
        filter = {"filtre" : pygame.image.load("Images\\pluie_vent.png").convert_alpha(), "pos" : (-3500,-3500), "type" : 'rain_wind'}
        prob = 0.17
    else :
        if wind :
            filter = {"filtre" : pygame.image.load("Images\\vent.png").convert_alpha(), "pos" : (-9000,0), 'type' : "vent"}
        else :
            filter = {}
        prob = 0.3
    if game_mode == 'firefighter' :
        difficulty = difficulty_choice()
        # On place un feu de broussaille aléatoirement.
        starter = "bush"
        univers = generate_universe(size, cat = 3)
        univers = placement_fire(univers.shape, starter, (random.randrange(50,450),random.randrange(50,450)), univers)
        # On lance le mode de jeu pompier.
        mode_firefighter(univers, 150, size_screen = screen_size, wind = wind, difficulty = difficulty, filter = filter, prob = prob)
    if game_mode == 'classic' :
        # On demande au joueur le nombre de simulation voulu.
        n_generations = generation_input()
        screen.fill(white)
        # On le laisse choisir son feu de départ.
        starter = fire_choice()
        univers = generate_universe(size, cat = 3)
        # On le laisse choisir là où il veut mettre sont départ de feu.
        univers = add_fire_click(size, starter, screen, univers, filter = filter)
        # On lance la simulation.
        mode_normal(univers, n_generations, wind = wind, filter = filter, prob = prob )
    
if __name__ == '__main__':
    display_game()