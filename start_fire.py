
import numpy 
from classes import *
from sound import *

# Dictionnaire contenant les différents types de départs de feu.
starters = { 'cigarette': [[1]], 'gasoline':[[0,1,0],[1,1,1],[0,1,0]], 'bush' : [[1,1],[1,1]] }

# Fonction de génération procédurale, où p1 represente la quantité d'arbre et p2 celle d'eau.
def generation_2(size : tuple, p1 : float, p2 : float) -> numpy.array :
	"""
	Principe. Cette fonction génére un univers aléatoirement avec des forêts, des plaines et des lacs.
	Argument(s) :
		size : dimension de l'univers ;
		p1 : proportion de plaine ;
		p2 : proportion de lac.
	Résultat. L'univers généré.
	"""
	# On utilise noise, qui sort une valeur entre -0.5 et 0.5, et on calcule de quel type est la case en fonction de p1 et p2.
	import noise
	
	universe = numpy.array([[None for _ in range(size[1])] for _ in range(size[0])])
	
	for i in range(size[0]):
		for j in range(size[1]):
			value=noise.pnoise2(i/30,j/30,2,1.2,2.0,size[0],size[1],0)
			if value+0.5<p2:
				universe[i][j]=Water()
			elif value+0.5<(1-p2)*p1+p2:
				universe[i][j]=Plain()
			else:
				universe[i][j]=Tree()
	return universe

# Fonction de génération procédurale avec rivière, où p1 représente la quantité d'arbre et p2 celle d'eau. 
def generation_3(size : tuple, p1 : float, p2 : float) -> numpy.array:
	"""
	Principe. Cette fonction génère un univers aléatoirement avec une rivière, des forêts, des plaines et des lacs.
	Argument(s) :
		size : dimension de l'univers ;
		p1 : proportion de plaine ;
		p2 : proportion de lac.
	Résultat. L'univers généré.
	"""
	# On utilise noise, qui sort une valeur entre -0.5 et 0.5, et on calcule de quel type est la case en fonction de p1 et p2.
	import noise
	
	universe = numpy.array([[None for _ in range(size[1])] for _ in range(size[0])])

	for i in range(size[0]):
		for j in range(size[1]):
			value=noise.pnoise2(i/30,j/30,2,1.3,2.0,size[0],size[1],0)
			if value+0.5<p2:
				universe[i][j]=Water()
			elif value+0.5<(1-p2)*p1+p2:
				universe[i][j]=Plain()
			else:
				universe[i][j]=Tree()
	#Creation de riviere
	point_entry=prob=numpy.random.randint(0,size[0]-1)
	point_out=numpy.random.randint(0,size[0]-1)
	delta=abs(point_entry-point_out)
	#sign exprime le fait d'aller à gauche ou droite
	if delta!=0:
		sign=int((point_out-point_entry)/delta)
	else:
		sign=0
	coord=[point_entry,0] #coordonnee de la case explorée
	universe[coord[0]][coord[1]]=Water()
	#on parcours l'univers en descendant, et en allant à gauche (droite) de maniere aléatoire jusqu'à atteindre la coordonnée de sortie
	while coord[1]<size[1]-1:
		if numpy.random.randint(0,delta+size[1]-coord[1])<delta:
			coord[0]+= sign
			if (universe[coord[0]-sign][coord[1]-1].type=='Water')and(numpy.random.randint(0,2)==0):
				universe[coord[0]][coord[1]-1]=Water()
				
		else:
			coord[1]+=1
		universe[coord[0]][coord[1]]=Water() 
		delta=abs(coord[0]-point_out) 
		
	return universe

# Création de la carte, pour une catégorie spécifiée.
def generate_universe(size : tuple, cat : int) -> numpy.array :
	"""
	Principe. Cette fonction génère un univers de catégorie choisie.
	Argument(s) :
		size : dimension de l'univers ;
		cat : entier donnant le type de génération utilisée (1,2,3 ou 4).
	Résultat. L'univers généré
	"""
	universe = numpy.array([[None for _ in range(size[1])] for _ in range(size[0])])
	# Première carte avec seulement des arbres (catégorie 1).
	if cat == 1:
		for i in range(size[0]):
			for j in range(size[1]):
				universe[i][j]= Tree()
		return universe
	#Aléatoire sans rivière (proportions fixées)
	elif cat == 2:
		return generation_2(size, 0.4, 0.08)
	# Aléatoire avec rivière (proportions fixées)
	elif cat == 3:
		return generation_3(size, 0.4, 0.08)

def start_fire(universe : numpy.array, starter : list, x : int, y : int) -> numpy.array :
	"""
	Principe. Cette fonction ajoute du feu dans l'univers.
	Argument(s) :
		universe : tableau numpy d'objets des classes Tree(), Plain(), Water() ;
		starter : clé du dictionnaire starters, type de départ de feu ;
		x : position du départ de feu dans l'univers (colonne) ;
		y : position du départ de feu dans l'univers (ligne).
	Résultat. L'univers avec le feu placé.
	"""
	fire = starters[starter]
	if x + len(fire) > len(universe) or y + len(fire[0]) > len(universe[0]) : # Si le feu est plus grand que la carte, le jeu n'est pas lancé.
		raise AttributeError('Le départ de feu ne peut pas être plus grand que a carte !')
	for i in range(len(fire)):
		for j in range(len(fire[0])):
			if fire[i][j]==1 and universe[x+i][y+j].state==0  : # Ajoute le feu aux endroits qui ne sont pas encore brulés.
				if not isinstance(universe[x+i][y+j], Water): # On n'ajoute pas de feu sur l'eau.
					universe[x+i][y+j].state = 1
					universe[x+i][y+j].time = 1
	begin_sound_point(starter)
	return universe 

def initiate_game(size : tuple, starter : str, position : tuple, cat : int) -> numpy.array :
	"""
	Principe. Cette fonction lance le jeu, en créant un univers et en y ajoutant un départ de feu.
	Argument(s) :
		size : dimension de l'univers ;
		starter : clé du le dictionnaire starters, type de départ de feu ;
		position : coordonnées du départ de feu dans l'univers ;
		cat : entier donnant le type de génération utilisée (1, 2 ou 3).
	Résultat. L'univers créé avec le feu placé.
	"""
	return start_fire(generate_universe(size, cat), starter, position[0],position[1])

	
