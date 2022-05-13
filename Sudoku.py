from Vertice import Vertice
from copy import deepcopy
from math import sqrt


class Sudoku():
	def __init__(self):
		super(Sudoku, self).__init__()

	def reseta_vertice(self, vertice):
		vertice.colorido = False
		vertice.label = 0
		vertice.cor = 0
		vertice.grau_saturacao = 0
		return vertice

	def gera_sudoku(self, tamanho, inicial):
		self.tamanho = tamanho
		self.inicial = inicial

		tabuleiro = self.monta_tabuleiro()
		vertices = self.cria_vertices(tabuleiro)
		matriz = self.gera_matriz(vertices)
		vertices = self.resolve_sudoku(matriz, vertices)
		
		return vertices

	def monta_tabuleiro(self):
		tabuleiro = []
		cont = 1
		for i in range(self.tamanho):
			linha_tabuleiro = []  # Cria linha do tabuleiro
			for j in range(self.tamanho):  # Cada coluna da linha
				nome_casa = cont  # Nome da casa varia de 1-N*N
				cont += 1

				linha_tabuleiro.append(nome_casa)  # Adiciona casa na linha

			tabuleiro.append(linha_tabuleiro)  # Adiciona linha no tabuleiro

		return tabuleiro

	def cria_vertices(self, tabuleiro):
		tam_quadrante = int(sqrt(self.tamanho))
		vertices = []

		for i in range(self.tamanho):  # Percorre linha
			for j in range(self.tamanho):  # Percorre coluna
				valor_casa = tabuleiro[i][j]

				# ======================================
				# VÉRTICES ADJACENTES DA CASA

				# Vértices adjacentes por linha
				vertices_linha = tabuleiro[i].copy()
				vertices_linha.remove(valor_casa)

				# Vértices adjacentes por coluna
				vertices_coluna = [tabuleiro[x][j] for x in range(self.tamanho)]
				vertices_coluna.remove(valor_casa)

				# Vértices adjacentes por quadrante
				vertices_quadrante = []
				quadrante_coluna = j // tam_quadrante
				quadrante_linha = i // tam_quadrante

				# Percorre vértices do quadrante
				for m in range(quadrante_linha * tam_quadrante, tam_quadrante * quadrante_linha + tam_quadrante):
					for n in range(tam_quadrante * quadrante_coluna, tam_quadrante * quadrante_coluna + tam_quadrante):
						if m != i and n != j:
							vertices_quadrante.append(tabuleiro[m][n])

				# Junta todos os vértices adjacentes
				conexoes = vertices_linha + vertices_coluna + vertices_quadrante

				# ======================================
				novo_vertice = Vertice(
					valor_casa,
					conexoes
				)

				vertices.append(novo_vertice)

		return vertices

	def gera_matriz(self, vertices):
		matriz = []

		# Percorre os vértices
		for vertice in vertices:
			linha_matriz = []
			# Verifica as conexões do vértice atual com os demais
			for aux_vertice in vertices:
				""" Adiciona 1 à linha se o vértice estiver nas conexões do
					vértice atual e 0 se não estiver """
				linha_matriz.append(1) if aux_vertice.id in vertice.conexoes else linha_matriz.append(0)
			matriz.append(linha_matriz)

		return matriz

	def todos_pintados(self, vertices):
		for vertice in vertices:
			if vertice.colorido is False:
				return False
		return True

	def define_cor(self, vertices, atual, coloridos):
		# Obtém as cores utilizadas pelos adjacentes do vértice atual
		cores_adj = [vertices[adj - 1].cor for adj in atual.conexoes if vertices[adj - 1].colorido is True]

		# Identifica quais cores já utilizadas estão disponíveis para reutilização
		cores_disponiveis = []
		for vertice in coloridos:
			if vertice.id not in atual.conexoes and vertice.cor not in cores_adj:
				cores_disponiveis.append(vertice)
		

		if cores_disponiveis != []:  # Se tiver cores disponíveis
			cor = cores_disponiveis[0]
			for iter_cor in cores_disponiveis:
				if iter_cor.grau_saturacao < cor.grau_saturacao:
					cor = iter_cor
			cor = cor.cor
		else:  # Se não tiver nenhuma cor disponível é criada uma cor nova
			maior_cor = coloridos[0].cor
			for colorido in coloridos:
				if colorido.cor > maior_cor:
					maior_cor = colorido.cor
			cor = maior_cor + 1

		return cor

	def resolve_sudoku(self, matriz, vertices):
		atual = vertices[self.inicial - 1]  # Pega o vertice inicial definido pelo usuário
		atual.colorido = True
		atual.label = 1
		atual.cor = 1

		coloridos = []  # Lista para adicionar os vértices já coloridos
		coloridos.append(atual)  # Adiciona o primeiro vértice colorido
		for i in range(len(matriz)):  # Percorre a matriz de adjacência
			# Aumenta o grau de saturação nos vértices adjacentes
			if matriz[self.inicial - 1][i] == 1:
				if i != self.inicial - 1:
					vertices[i].grau_saturacao += 1

		while self.todos_pintados(vertices) is False:  # Enquanto todos não estiverem pintados
			# Obtém o vértice atual a partir do anterior, verificando se já está colorido e se é o maior grau de saturação
			atual = next((vertice for vertice in vertices[atual.id - 1:] if vertice.colorido is False), None)
			if atual is None:
				atual = next((vertice for vertice in vertices if vertice.colorido is False))
			for vertice in vertices:
				if vertice.grau_saturacao > atual.grau_saturacao and vertice.colorido is False:
					atual = vertice

			atual.colorido = True
			# Obtém cor para o vértice atual
			cor = self.define_cor(vertices, atual, coloridos)
			atual.cor = cor
			atual.label = cor

			# Adiciona o vertice atual a lista de coloridos
			coloridos.append(atual)

			# Aumenta o grau de saturação de seus adjacentes
			for i in range(len(matriz)):
				if matriz[atual.id - 1][i] == 1:
					if i != (atual.id - 1):
						vertices[i].grau_saturacao += 1
		return vertices
