import pygame

# On initialise le mixer sonore et on importe les différents sons que l'on organise dans un dictionnaire.
pygame.mixer.init()

water_sound = pygame.mixer.Sound("sounds/ajout_eau.mp3")
cigarette_sound = pygame.mixer.Sound("sounds/cigarette.mp3")
essence_sound = pygame.mixer.Sound("sounds/essence.wav")
fire_sound = pygame.mixer.Sound("sounds/feu_classique.mp3")
drought_sound = pygame.mixer.Sound("sounds/feu_sec.mp3")
rain_sound = pygame.mixer.Sound("sounds/pluie.mp3")
forest_sound = pygame.mixer.Sound("sounds/vent_foret.mp3")

dico_sound = {"water" : water_sound, "cigarette" : cigarette_sound, "gasoline" : essence_sound, "bush" : fire_sound,
              "fire" : fire_sound, "drought" : drought_sound, "rain" : rain_sound, "forest" : forest_sound}

def begin_sound_point(sound_name: str) -> None :
    '''
    Principe. Cette fonction joue un son court.
    Arugment(s) :
	    sound_name : Le son que l'on veut jouer.
    Résultat. Aucun.
    '''
    dico_sound[sound_name].play(maxtime = 2000)

def begin_sound_background(sound_name: str) -> None :
    '''
    Principe. Cette fonction joue un son long qui peut servir de bruit de fond.
    Arugment(s) :
	    sound_name : Le son que l'on veut jouer.
    Résultat. Aucun.
    '''
    dico_sound[sound_name].play()