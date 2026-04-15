
import matplotlib.pyplot as plt
import networkx as nx

def pltSetup():
	pass
def renderGraph(graph):
	options = {
	'node_color': 'blue',
	'node_size': 100,
	'width': 3,
	'arrowstyle': '-|>',
	'arrowsize': 12,
}
	pos = nx.spring_layout(graph)
	nx.draw_networkx_nodes(graph, pos, cmap=plt.get_cmap('jet'), node_color = values, node_size = 500)
	nx.draw_networkx_labels(graph, pos)
	nx.draw_networkx_edges(graph, pos, arrows=True)
	plt.show()
