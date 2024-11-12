import pygame

# On définit la taille de l'écran.
screen_size = (500, 500)

# On définit plusieurs couleurs que l'on peut appeler plus tard.
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 100, 0)
padding = 10

# On initialise pygame pour toutes les autres fonctions.
pygame.init()

screen = pygame.display.set_mode(screen_size)
screen.fill(white)
font = pygame.font.Font(None, 36)

# On importe les images de cellules dans Python.
fire_tree_image = pygame.image.load("Images\\Arbre en feu.png").convert_alpha()
healthy_tree_image = pygame.image.load("Images\\Arbre sain.png").convert_alpha()
water_image = pygame.image.load("Images\\Eau.png").convert_alpha()
plain_image = pygame.image.load("Images\\Plaine.png").convert_alpha()
fire_plain_image = pygame.image.load("Images\\Plaine en feu.png").convert_alpha()
dead_plain_image = pygame.image.load("Images\\Plaine morte.png").convert_alpha()
dead_tree_image = pygame.image.load("Images\\Arbre mort.png").convert_alpha()
saved_plain_image = pygame.image.load("Images\\Plaine sauve.png").convert_alpha()

rain_image = pygame.image.load("Images\\pluie.png").convert_alpha()
wind_image = pygame.image.load("Images\\vent.png").convert_alpha()

# On utilise un dictionnaire pour trouver plus simplement ces images.
dico_image = {"tree_fire" : fire_tree_image, "tree" : healthy_tree_image, "water" : water_image, "plain" : plain_image,
			  "plain_fire" : fire_plain_image, "dead_plain" : dead_plain_image, "dead_tree" : dead_tree_image, "saved_plain" : saved_plain_image}