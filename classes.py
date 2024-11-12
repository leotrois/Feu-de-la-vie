class Cell() :
	'''
	Une cellule a un état (qui par défaut à la création est non-brûlé), un temps depuis lequel la cellule brûle (forcé à zéro à la création), et deux facteurs (voir transmission_factor et reception_factor).
	'''
	def __init__(self, state : int = 0, transmission_factor : float = 1., reception_factor : float = 1.) :
		# Réalisation de tests sur les types des arguments puis sur leurs valeurs s'ils sont conformes
		if not isinstance(state, int) :
			raise TypeError('L\'état doit être un entier.')
		elif not state in [0, 1, 2, 3] :
			raise ValueError('L\'état doit valoir 0, 1, 2 ou 3.')
		if not isinstance(transmission_factor, float) :
			raise TypeError('Le facteur de transmission doit être un flottant.')
		elif not 0 <= transmission_factor <= 1 :
			raise ValueError('Le facteur de transmission doit être compris entre 0 et 1.')
		if not isinstance(reception_factor, float) :
			raise TypeError('Le facteur de récpetion doit être un flottant.')
		if not 0 <= reception_factor <= 1 :
			raise ValueError('Le facteur de réception doit être compris entre 0 et 1.')
		# Mémorisation des arguments dans des attributs privés.
		self.__state = state
		self.__time = 0
		self.__transmission_factor = transmission_factor
		self.__reception_factor = reception_factor
	
	@property
	def state(self) -> int :
		'''
		state est un entier 0, 1, 2 ou 3 qui correspond respectivement aux états sain, en cours de brûlure et brûlure.	
		'''
		return self.__state
	
	# Définition d'un setter sur l'état.
	@state.setter
	def state(self, state : int) -> None :
		# Vérification de la validité du nouvel attribut (type et valeur, voir plus haut).
		if not isinstance(state, int) :
			raise TypeError('L\'état doit être un entier.')
		elif not state in [0, 1, 2, 3] :
			raise ValueError('L\'état doit valoir 0, 1, 2 ou 3.')
		self.__state = state

	@property
	def type(self) -> str :
		'''
		type est une chaîne de caractère indiquant le type de la cellule.
		'''
		return 'Cell'
	
	@property
	def time(self) -> int :
		'''
		time est un entier correspondant au temps passé à brûler (en nombre d'itérations).
		'''
		return self.__time
	
	# Définition d'un setter sur le temps.
	@time.setter
	def time(self, time : int) -> None :
		# Vérification de la validité du nouvel attribut (type et valeur, voir plus haut).
		if not isinstance(time, int) :
			raise TypeError('time doit être un entier.')
		elif not time >= 0 :
			raise ValueError('time doit être positif.')
		self.__time = time
	
	@property
	def transmission_factor(self) :
		'''
		transmission_factor est un flottant entre 0 et 1 correspondant à un facteur pour pondérer la probabilité qu'une cellule particulière enflamme un voisin quelconque.
		'''
		return self.__transmission_factor
	
	@property
	def reception_factor(self) :
		'''
		recetion_factor est un flottant entre 0 et 1 correspondant à un facteur pour pondérer la probabilité qu'une cellule particulière se fasse enflammer par un voisin quelconque.
		'''
		return self.__reception_factor
	
	def is_burning(self) -> bool :
		'''
		is_burning explicite l'état entrain de brûler d'une cellule en retournant un booléen.
		'''
		return self.__state == 1

	def is_burnt(self) -> bool :
		'''
		is_burnt explicite l'état brûlé d'une cellule en retournant un booléen.
		'''
		return self.time >= self.lifetime
	
	@property
	def lifetime(self) -> None :
		'''
		lifetime est un entier indiquant le temps de vie (nombre d'itérations) de la cellule.
		'''
	
class Tree(Cell) :
	'''
	Sous-classe de Cell correspondant à des cellules de type 'arbre'.
	Un arbre est une cellule avec entre autre des coefficients de transmission et réception particuliers.
	'''
	def __init__(self, state : int = 0) :
		super().__init__(state = state, transmission_factor = 1., reception_factor = 1.)
	
	@property
	def type(self) -> str :
		return 'Tree'
	
	# Un arbre a une durée de vie de 2 itérations
	@property
	def lifetime(self) -> int :
		return 3

class Plain(Cell) :
	'''
	Sous-classe correspondant à des cellules de type 'plaine'.
	Un morceau de plaine est une cellule avec entre autre des coefficients de transmission et réception particuliers.
	'''
	def __init__(self, state : int = 0) :
		super().__init__(state = state, transmission_factor = 0.5, reception_factor = 0.5)
	
	@property
	def type(self) -> str :
		return 'Plain'
	
	# Un morceau de plaine a une durée de vie de 1 itération.
	@property
	def lifetime(self) -> int :
		return 2

class Water(Cell) :
	'''
	Sous-classe correspondant à des cellules de type 'eau'.
	L'eau est une cellule qui ne brûle jamais.
	'''
	def __init__(self, state : int = 0) :
		super().__init__(state, transmission_factor = 0., reception_factor = 0.)

	@property
	def type(self) -> str :
		return 'Water'
	
	# L'eau ne brûle jamais.
	def is_burnt(self) -> bool :
		return False