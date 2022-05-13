import matplotlib
import matplotlib.gridspec as gridspec
import matplotlib.pyplot as plt
import random
import networkx as nx

from math import sqrt
from matplotlib.widgets import Button
from matplotlib.widgets import TextBox


class App():
	def __init__(self, sudoku):
		super(App, self).__init__()

		self.sudoku = sudoku

		# Inicializa o plot
		self.fig, self.ax = plt.subplots()
		self.fig.canvas.manager.set_window_title('Sudoku NxN')
		self.fig.subplots_adjust(bottom=0.2, top=0.9)
		self.ax.get_xaxis().set_visible(False)
		self.ax.get_yaxis().set_visible(False)

		self.G = nx.Graph()  # Inicializa o grafo

		# Layout grid para as configurações
		gs = gridspec.GridSpec(2, 2)
		gs.update(left=0.45, right=0.65, bottom=0.05, top=0.15, hspace=0.3)

		axes = [self.fig.add_subplot(gs[i, j]) for i, j in [[0, 0], [1, 0], [0, 1]]]

		# Componentes para configuração do usuário
		self.tamanho = TextBox(axes[0], 'Tamanho do tabuleiro', hovercolor='0.975', initial='4', label_pad=0.05)
		self.inicial = TextBox(axes[1], 'Vértice inicial', hovercolor='0.975', initial='1', label_pad=0.05)
		submit_button = Button(axes[2], "Gerar")
		submit_button.on_clicked(self.submit)

		plt.show()  # Exibe o grafo

	def submit(self, event):
		# Obtém valores de tamanho e vértice inicial
		tamanho = int(self.tamanho.text)
		inicial = int(self.inicial.text)

		# Limpa o grafo desenhado anteriormente
		self.ax.clear()
		self.G.clear()
		self.fig.canvas.draw_idle()

		
		# Gera o sudoku e monta o grafo
		vertices = self.sudoku.gera_sudoku(tamanho, inicial)
		self.monta_grafo(tamanho, vertices)

	def monta_grafo(self, T, vertices):
		self.ax.set_title(label=f"Tabuleiro {T}x{T}", fontsize=20, pad=15)

		# Define cores
		# colors = ["red", "green", "blue", "yellow", "orange", "purple", "cyan", "gray", "chartreuse", "darkslateblue", "sienna", "aquamarine", "deeppink", "lightpink", "peru", "y"]  # Cores
		colors = [name for name, hex in matplotlib.colors.cnames.items()]
		colors.remove("black")
		colors.remove("white")
		random.shuffle(colors)

		cont = 0  # Contador para acessar o nome do vertice
		for i in range(T, 0, -1):  # T -> 0, decrementa
			for j in range(1, T + 1, 1):  # 1 -> T + 1, incrementa
				# Adiciona o vértice ao grafo
				self.G.add_node(vertices[cont].id, pos=(j, i), node_color=colors[vertices[cont].cor - 1])
				cont += 1

		pos = nx.get_node_attributes(self.G, 'pos')  # Obtém as posições

		# =====================================================================
		# Desenha conexões (arestas)
		matriz = []

		for i in range(1, T + 1, 1):
			linha = [j + T * i - T for j in range(1, T + 1, 1)]
			matriz.append(linha)
		
		for i in range(T):
			for j in range(T):
				valor_casa = matriz[i][j]

				vertices_linha = matriz[i].copy()
				vertices_linha.remove(valor_casa)

				vertices_coluna = [matriz[x][j] for x in range(T)]
				vertices_coluna.remove(valor_casa)

				vertices_quadrante = []
				tam_quadrante = int(sqrt(T))
				quadrante_coluna = j // tam_quadrante
				quadrante_linha = i // tam_quadrante

				# Percorre vértices do quadrante
				for m in range(quadrante_linha * tam_quadrante, tam_quadrante * quadrante_linha + tam_quadrante):
					for n in range(tam_quadrante * quadrante_coluna, tam_quadrante * quadrante_coluna + tam_quadrante):
						if m != i and n != j:
							vertices_quadrante.append(matriz[m][n])

				vertices_conexao = vertices_linha + vertices_coluna + vertices_quadrante
				for vertice in vertices_conexao:
					self.G.add_edge(valor_casa, vertice)
		
		# =====================================================================
		# Desenha Grafo

		node_colors = nx.get_node_attributes(self.G, 'node_color')  # Obtém as cores
		nx.draw(self.G, pos, with_labels=False, arrows=False, node_color=list(node_colors.values()), node_size=600, ax=self.ax)  # Desenha o grafo

		# Adiciona os números do sudoku invés dos nomes de cada vértice
		labels = {}
		for node in self.G.nodes():
			labels[node] = str(vertices[node - 1].cor)
		nx.draw_networkx_labels(self.G, pos, labels, ax=self.ax)
