#choice
from choice import *
from classes import *
from start_fire import generate_universe, start_fire, initiate_game
from neighborhood import *
from display_im import *
from choice import *
from main_pygame import *

def test_choix_click():
    '''Test sur les fonctions de choix utilisateur'''
    # Test du choix des modes
    print('Sélectionnez le mode pompier.')
    assert mode_choice() == 'firefighter'
    screen.fill(white)

    print('Sélectionnez le mode classique.')
    assert mode_choice() == 'classic'
    screen.fill(white)


    # Test du choix de la météo.
    print('Sélectionnez du vent avec de la sécheresse.')
    assert weather_choice() == [True, 'drought']
    screen.fill(white)

    print('Sélectionnez temps clair')
    assert weather_choice() == [False, '']
    screen.fill(white)

    print('Sélectionnez pluie')
    assert weather_choice() == [False, 'rain']
    screen.fill(white)


    # Test du choix de la taille de l'univers.
    print('Sélectionnez un univers petit.')
    assert size_choice() == 20
    screen.fill(white)

    print('Sélectionnez un univers moyen.')
    assert size_choice() == 50
    screen.fill(white)

    print('Sélectionnez un univers grand.')
    assert size_choice() == 70
    screen.fill(white)


    # Test du choix de la difficulté.
    print('Sélectionnez une difficulté facile.')
    assert difficulty_choice() == 0
    screen.fill(white)

    print('Sélectionnez une difficulté moyenne.')
    assert difficulty_choice() == 1
    screen.fill(white)

    print('Sélectionnez une difficulté forte.')
    assert difficulty_choice() == 2
    screen.fill(white)


    # Test du choix du feu.
    print('Choisissez la cigarette.')
    assert fire_choice() == 'cigarette'
    screen.fill(white)

    print('Choisissez essence.')
    assert fire_choice() == 'gasoline'
    screen.fill(white)

    print('Choisissez le buisson.')
    assert fire_choice() == 'bush'
    screen.fill(white)


    print('entrez 100')
    assert generation_input() == 100
    screen.fill(white)


#classes
def test_obj():
    '''Fonction de test sur les classes Cell, Tree, Plain et Water'''
    # Test de l'initialisation d'un objet Cell par défaut
    example_cell = Cell()
    assert example_cell.state == 0
    assert not example_cell.is_burning()

    # Test sur le changement des attributs de Cell
    example_cell.state = 1
    assert example_cell.state == 1
    assert example_cell.is_burning()
    assert example_cell.type == 'Cell'
    assert example_cell.time == 0

    # Test sur les attributs de Cell
    example_cell.time = 20
    assert example_cell.time == 20
    assert example_cell.transmission_factor == 1
    assert example_cell.reception_factor == 1

    # Test sur l'initialisation d'un objet Cell avec données
    example_cell = Cell(1, reception_factor = 0.5)
    assert example_cell.state == 1
    assert example_cell.is_burning()
    assert example_cell.transmission_factor == 1
    assert example_cell.reception_factor == 0.5

    # Test sur un objet Tree
    example_tree = Tree()
    assert example_tree.type == 'Tree'
    assert example_tree.lifetime == 3
    assert example_tree.state == 0
    assert not example_tree.is_burning()

    example_tree.state = 1
    assert example_tree.state == 1
    assert example_tree.is_burning()
    assert example_tree.time == 0
    assert not example_tree.is_burnt()

    example_tree.time = 20
    assert example_tree.time == 20
    assert example_tree.is_burnt()
    assert example_tree.transmission_factor == 1
    assert example_tree.reception_factor == 1

    example_tree = Tree(1)
    assert example_tree.state == 1
    assert example_tree.is_burning()

    # Test sur un objet Plain
    example_plain = Plain()
    assert example_plain.type == 'Plain'
    assert example_plain.lifetime == 2
    assert example_plain.state == 0
    assert not example_plain.is_burning()

    example_plain.state = 1
    assert example_plain.state == 1
    assert example_plain.is_burning()
    assert example_plain.time == 0
    assert not example_plain.is_burnt()

    example_plain.time = 20
    assert example_plain.time == 20
    assert example_plain.is_burnt()
    assert example_plain.transmission_factor == 0.5
    assert example_plain.reception_factor == 0.5

    example_plain = Plain(1)
    assert example_plain.state == 1
    assert example_plain.is_burning()

    # Test sur un objet Water
    example_water = Water()
    assert example_water.type == 'Water'
    assert example_water.state == 0
    assert not example_water.is_burning()

    assert example_water.transmission_factor == 0
    assert example_water.reception_factor == 0
    
    # Test sur l'entrée de paramètres non valides sur les différents objets
    obj = Cell()
    assert obj.state == 0
    assert obj.type == 'Cell'
    score = 0
    try:
        Cell(0.5)
    except:
        score += 1
    try:
        Cell(5)
    except:
        score += 1
    try:
        Cell(0, '', 0)
    except:
        score += 1
    try:
        Cell(0, 1.4, 0)
    except:
        score += 1
    try:
        Cell(0, 0, '')
    except:
        score += 1
    try:
        Cell(0,0,1.4)
    except:
        score += 1
    assert score == 6
    
#start_fire

def test_generate_universe():
    '''Cette fonction teste la création d'un univers avec la fonction generate_universe'''
    univ = generate_universe((3,3),1)
    verif = True
    for i in range(len(univ)):
        for j in range(len(univ[0])):
            if not isinstance(univ[i][j], Tree):
                verif = False
    assert verif

def test_start_fire():
    '''Cette fonction teste la fonction start_fire'''
    jeu=start_fire(np.array([[Tree(),Tree()],[Tree(),Tree()]]),'cigarette',0,0)
    assert jeu[0][0].state == 1
    assert jeu[0][1].state == 0
    assert jeu[1][0].state == 0
    assert jeu[1][1].state == 0

def test_initiate_game():
    '''Cette fonction teste la fonction initiate_game'''
    universe = initiate_game((2,2),'cigarette',(0,0),1)
    assert universe[0][0].state == 1
    assert universe[0][1].state == 0
    assert universe[1][0].state == 0
    assert universe[1][1].state == 0 
    
#voisinage


def test_coord_neighbour_without_wind():
    '''On vérifie que la fonction coord_neighbour prend bien en compte les effets de bords'''
    assert set(coord_neighbour_without_wind((3,3),1,1)) == set([(0,0),(0,1),(0,2),(1,2),(2,2),(2,1),(2,0),(1,0)]) #sans bords
    assert set(coord_neighbour_without_wind((3,3),0,1)) == set([(0,0),(0,2),(1,0),(1,1),(1,2)]) #au bord
    assert set(coord_neighbour_without_wind((3,3),0,0)) == set([(0,1),(1,0),(1,1)]) #au coin

def test_coord_neighbour_wind():
    '''On vérifie que la fonction coord_neighbour prend bien en compte les effets de bords'''
    assert set(coord_neighbour_wind((5,5),2,2)) == set([(0,1),(0,2),(0,3),(1,0),(1,1),(1,2),(1,3),(1,4),(2,0),(2,1),(2,3),(2,4),(3,0),(3,1),(3,2),(3,3),(3,4),(4,1),(4,2),(4,3)]) #sans bords
    assert set(coord_neighbour_wind((5,5),0,2)) == set([(0,0),(0,1),(0,3),(0,4),(1,0),(1,1),(1,2),(1,3),(1,4),(2,1),(2,3),(2,2)]) #au bord
    assert set(coord_neighbour_wind((5,5),0,0)) == set([(0,1),(1,0),(1,1),(0,2),(1,2),(2,0),(2,1)]) #au coin

def test_update():
    '''Cette fonction appelle une fois la fonction pour vérifier l'absence d'erreurs. 
    Seulement on ne la teste pas bien à cause de la présence d'aléatoire
    '''
    update(generate_universe((20,20), 1), 0.5, False)

def test_burn():
    '''Cette fonction appelle une fois la fonction pour vérifier l'absence d'erreurs. 
    Seulement on ne la teste pas bien à cause de la présence d'aléatoire
    '''
    burn(generate_universe((20,20), 1), 5,5,0.5,False)

def test_probability_without_wind():
    '''On vérifie que les probabilités renvoyés par la fonction correspondent bien avec les probabilités attendus, et ce dans plusieurs cas'''
    #Assert arbre-arbre
    universe = generate_universe((20,20), 1)
    universe[10,10].state = 1 
    assert probability_without_wind(universe, (10,10),(9,10), prob = 0.5) == 0.5
    assert probability_without_wind(generate_universe((20,20), 1), (5,6),(5,5), prob = 0.5)  == 0
    
    #Assert arbre-plaine
    universe = generate_universe((20,20), 1)
    universe[10,10]= Plain(1)
    assert probability_without_wind(universe, (10,10),(9,10), prob = 0.5) == 0.25
    
    #Assert plaine-arbre
    universe = generate_universe((20,20), 1)
    universe[10,10]= Tree(1)
    universe[9,10]= Plain()
    assert probability_without_wind(universe, (10,10),(9,10), prob = 0.5) == 0.25

def test_probability_wind():
    '''On vérifie que les probabilités renvoyés par la fonction correspondent bien avec les probabilités attendues, et ce dans plusieurs cas'''
    #test propogation arbre-arbre
    universe = generate_universe((20,20), 1)
    universe[10,10].state = 1 
    assert probability_without_wind(universe, (10,10),(9,10), prob = 0.5) == 0.5
    assert probability_without_wind(generate_universe((20,20), 1), (5,6),(5,5), prob = 0.5)  == 0
    
    #test propogation arbre-plaine
    universe = generate_universe((20,20), 1)
    universe[10,10]= Plain(1)
    assert probability_without_wind(universe, (10,10),(9,10), prob = 0.5) == 0.25
    
    #test propogation plaine-arbre
    universe = generate_universe((20,20), 1)
    universe[10,10]= Tree(1)
    universe[9,10]= Plain()
    assert probability_without_wind(universe, (10,10),(9,10), prob = 0.5) == 0.25

def test_is_burnt():
    '''On vérifie que après le temps de vie passé la case est bien considéré comme brulé'''
    universe = generate_universe((20,20), 1)
    universe[5,5].time = 100
    assert  universe[5,5].is_burnt()
    assert not universe[4,5].is_burnt()

# Test des fonctions de display_im

def test_display_im():
    '''Cette fonction teste les différentes catégories de generate_universe et teste les affichages de ces univers 
    avec des filtres, ainsi que l'affichage de tous les objets et tous leurs états, ainsi que l'affichage de la barre d'eau et du score final'''
    univ_1 = generate_universe((3,3), 1)
    univ_2 = generate_universe((3,3), 2)
    univ_3 = generate_universe((3,3), 3)
    display_universe_new(univ_1, {})
    display_universe_new(univ_2, {"filtre" : pygame.image.load("Images\\filtre_jaune.png").convert_alpha(), "pos" : (0,0), "type" : 'drought'})
    display_universe_new(univ_3, {"filtre" : pygame.image.load("Images\\vent_secheresse.png").convert_alpha(), "pos" : (-9000,0), "type" : 'vent', "type" : 'rain'})
    univ_3[1][0] = Tree(1)
    univ_3[1][1] = Tree(2)
    univ_3[1][2] = Tree(3)
    univ_3[0][0] = Plain(1)
    univ_3[0][1] = Plain(2)
    display_universe_new(univ_3, {})
    display_universe_new_bar(univ_3, 100,{})
    pygame.init()
    screen = pygame.display.set_mode(screen_size)
    screen.fill(white)
    display_score(85)

def test_main():
    '''Cette fonction teste le jeu dans sa globalité'''
    screen.fill(white)
    print("lancez mode simulation, temps normal, facile, petit")
    display_game()
    screen.fill(white)
    print("lancez mode simulation, vent et pluie, moyen, moyen")
    display_game()
    screen.fill(white)
    print("lancez mode simulation, vent, moyen, moyen")
    display_game()
    screen.fill(white)
    print("lancez mode simulation, pluie, moyen, moyen")
    display_game()
    screen.fill(white)
    print("lancez mode simulation, sécheresse, difficile, grand")
    display_game()
    screen.fill(white)
    print("lancez mode pompier, facile, temps normal, petit")
    display_game()
    screen.fill(white)
    print("lancez mode pompier, moyen, vent et pluie, moyen")
    pygame.init()
    display_game()
    screen.fill(white)
    print("lancez mode pompier, difficile, sécheresse, grand")
    pygame.init()
    display_game()
    screen.fill(white)
