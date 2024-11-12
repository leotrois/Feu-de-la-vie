import numpy as np
import random
from classes import *
from copy import deepcopy

# Fonctions pour les voisins avec vent.
def coord_neighbour_wind(size : tuple, x : int, y : int) -> list :
	'''
	Principe. La fonction renvoie les voisins de (x, y).
	Arugment(s) :
		size : La taille de l'univers ;
		x : première coordonnée ;
		y : deuxième coordonnée ;
	Résultat. La liste des voisins de la case de coordonnées (x, y).
	'''
	coord = [(x-1,y),(x+1,y),(x,y+1),(x,y-1),(x+1,y+1),(x-1,y-1),(x-1,y+1),(x+1,y-1),
			(x+2,y-1),(x+2,y),(x+2,y+1),(x-2,y-1),(x-2,y),(x-2,y+1),   
			(x-1,y+2),(x,y+2),(x+1,y+2),(x-1,y-2),(x,y-2),(x+1,y-2), ] #Liste coordonnées étendues possibles
	viable_neighbour = []
	for v in coord :
		if v[0] >= 0 and v[0] < size[0] and v[1] >= 0 and v[1] < size[1]: #Test position bien dans l'universe
			viable_neighbour.append(v)
	return viable_neighbour

# FOnctions pour les voisins sans vent.
def coord_neighbour_without_wind(size : tuple,x : int,y : int) -> list:
	'''
	Principe. La fonction renvoie les voisins de (x, y).
	Arugment(s) :
		size : La taille de l'univers ;
		x : première coordonnée ;
		y : deuxième coordonnée ;
	Résultat. La liste des voisins de la case de coordonnées (x, y).
	'''
	coord = [(x-1,y),(x+1,y),(x,y+1),(x,y-1),(x+1,y+1),(x-1,y-1),(x-1,y+1),(x+1,y-1)] # Liste des coordonnées possibles.
	viable_neighbour = []
	for v in coord :
		if v[0] >= 0 and v[0] < size[0] and v[1] >= 0 and v[1] < size[1]: # Vérification du fait que la position est bien dans l'univers.
			viable_neighbour.append(v)
	return viable_neighbour

def burn(universe : np.array, x : int, y : int, prob : float, wind: bool) -> bool :
	'''
	Principe. Cette fonction nous dit si la case encore intacte (x, y) prend feu.
	Agrument(s) :
		universe : l'univers considéré ;
		x : première coordonnée ;
		y : deuxième coordonnée.
	Résultat. True si elle prend feu, False sinon.
	'''
	if wind :
		proba_neighbour = [probability_wind(universe,v,(x,y), prob) for v in coord_neighbour_wind(universe.shape, x, y)] # Probabilité que le voisin passe le feu à cette case.
	else: 
		proba_neighbour = [probability_without_wind(universe,v,(x,y), prob) for v in coord_neighbour_without_wind(universe.shape,x,y)]
	p = 1 # Neutre.
	for proba in proba_neighbour:
		p = p * (1 - proba) # Réunion d'évenements indépendants (la case ne brule pas).
	# À ce stade, p est la probabilité que la case reste intacte.
	p = 1 - p 
	if random.random() <= p:
		return True
	else : return False
	 
proba = 0.15 # Valeur par défaut de proba générale.
# > 0.4 donne 100%
# 0.2 donne environ 95%
# 0.15 donne environ 75%
# 0.1 s'arrête très probablement avant d'atteindre un bord

def probability_without_wind(universe : np.array, c_neighbour : tuple, c_case : tuple, prob : float) -> float :
	'''
	Principe. Probabilité que c_neighbour transmette du feu à c_case.
	Argument(s).
		universe : l'univers considéré ;
		c_neighbour : la case voisine ;
		c_case : la case dont on cherche la probabilité d'être en feu ;
		prob : la probabilité générale de transmission.
	Résultat. La probabilité.
	'''
	case_neighbour = universe[c_neighbour]
	case = universe[c_case]
	if not case_neighbour.is_burning(): # Si la case voisine ne brûle pas, pas de propagation.
		return 0
	else :
		return prob * case_neighbour.transmission_factor * case.reception_factor # Calcul de la probabilité.
	
def probability_wind(universe : np.array,c_neighbour : tuple, c_case : tuple, prob : float) -> float:
	'''
	Principe. Probabilité que c_neighbour transmette du feu à c_case.
	Argument(s).
		universe : l'univers considéré ;
		c_neighbour : la case voisine ;
		c_case : la case dont on cherche la probabilité d'être en feu ;
		prob : la probabilité générale de transmission.
	Résultat. La probabilité.
	'''
	# Modification de probabilité en fonction du vent.
	prob_wind = 0
	match ((c_case[0] - c_neighbour[0]), abs(c_case[1] - c_neighbour[1])):
		case(1, 0) :
			prob_wind = 1
		case(2, 0) :
			prob_wind = 0.6
		case(1, 1) :
			prob_wind = 1
		case(2, 1) :
			prob_wind = 0.55
		case(-1, 0) :
			prob_wind = 0.8
		case(-1, 1) :
			prob_wind = 0.9
		case(0, 1) :
			prob_wind = 1
	case_neighbour = universe[c_neighbour]
	case = universe[c_case]
	if not case_neighbour.is_burning(): # Si la case voisine ne brûle pas, pas de propagation.
		return 0
	else :
		return prob * case_neighbour.transmission_factor * case.reception_factor * prob_wind # Calcul de la probabilité.

def update(universe : np.array,  prob : float, wind:bool ) -> np.array:
	'''
	Principe. Cette fonction met à jour l'univers à l'aide des fonctions créées précédemment.
	Argument(s) :
		universe : l'univers à l'état actuel ;
		prob : le facteur multiplicatif qui ralentit ou accèlère la propagation du feu ;
		wind : est-ce qu'on prend en compte le vent.
	Résultat. L'univers mis à jour.
	'''
	size = universe.shape
	new_universe = np.array([[None for _ in range(size[1])] for _ in range(size[0])])
	for i in range(size[0]):
		for j in range(size[1]):
			new_universe[i, j] = deepcopy(universe[i, j])
			if new_universe[i, j].state == 1 : # La case est en train de bruler.
				if not universe[i, j].is_burnt() :
					new_universe[i, j].time += 1
				else :
					new_universe[i, j].time += 1
					new_universe[i, j].state = 2
			else : # La case est intacte ou est brulée.
				if (new_universe[i, j].state == 0 or new_universe[i, j].state == 3) and burn(universe,i, j,prob,wind) :
					new_universe[i, j].state = 1
					new_universe[i, j].time += 1
			# Si la case est brulée ou doit rester intacte, elle ne change pas.
	return new_universe