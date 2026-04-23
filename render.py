
import matplotlib.pyplot as plt
import networkx as nx
import os

class render():
	def __init__(self):
		super().__init__()
		self.options = {}
		self.pltSetup()
		self.path = "results"

	def pltSetup(self):
		self.options = {
			'node_color': 'lightblue',
			#'node_size': 100,
			#'width': 3,
			#'arrowstyle': '-|>',
			#'arrowsize': 12,
		}

	def renderGraph(self, graph):
		pos = nx.spring_layout(graph)
		nx.draw_networkx_nodes(graph, pos, cmap=plt.get_cmap('jet'), node_size = 500)
		nx.draw_networkx_labels(graph, pos)
		nx.draw_networkx_edges(graph, pos, arrows=True)
		plt.show()

	def renderComparationGraph(self, ogGraph, newGraph, namePath):
		fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
		nx.draw(ogGraph, ax=ax1, with_labels=True, **self.options)
		ax1.set_title("Original")

		nx.draw(newGraph, ax=ax2, with_labels=True, **self.options)
		ax2.set_title("Novo")

		plt.savefig(os.path.join(self.path, namePath + '.png'))
		plt.show()
