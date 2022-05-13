class Vertice():
	def __init__(self, vertice_id, conexoes):
		super(Vertice, self).__init__()
		self.id = vertice_id
		self.conexoes = conexoes
		self.grau = 0
		self.grau_saturacao = 0
		self.colorido = False
		self.label = 0
		self.cor =  0 # A cor seria o mesmo valor que o número