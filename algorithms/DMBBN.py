import networkx as nx
from algorithms.utils import changeOrdering,createVetOrder,convert_solution_func
from algorithms.modified_DMBC import modified_dmbc

def dmbbn(dataset, score_type, parents_max, parents_number):
	finalGraph = nx.DiGraph()
	nodes = list(dataset.columns)  # Names of the nodes
	finalGraph.add_nodes_from(nodes)
	estimator = score_type(dataset)

	score = score_type
	original_order_samples = dataset.columns
	initial_order = createVetOrder(original_order_samples)
	#print(f'Ordem original: {initial_order}')
	for i in range(len(initial_order)):
		#print(f'\ninitial_order[{i}]: {initial_order[i]}')
		order = changeOrdering(initial_order, i)
		#print(f'\nOrdem alterada: {order}')
	  # Ordena os dados com base na solução
		ordered_vector = convert_solution_func(dataset, original_order_samples[order])
		#print(f'Ordem do dataset alterada: {ordered_vector}')
		rootVariable = ordered_vector.columns[0]
		#print(f'\n1a variavel: {rootVariable}')
		#localGraph, score_metric = modified_dmbc(ordered_vector, rootVariable, estimator=score(ordered_vector), parents_nmax=parents_max)
		localGraph = nx.DiGraph()
		localGraph = modified_dmbc(ordered_vector, rootVariable, estimator=score(ordered_vector), parents_nmax=parents_max)

		weight = 1
		# para cada filho do atributo
		for node in localGraph.nodes:
			for neighbor in localGraph.neighbors(node):
				if finalGraph.has_edge(node, neighbor):
					finalGraph[node][neighbor]['weight'] = finalGraph.get_edge_data(node, neighbor).get('weight', 0) + 1
				elif not finalGraph.has_edge(node, neighbor):
					if finalGraph.degree[neighbor] < parents_number:
						finalGraph.add_weighted_edges_from([(node, neighbor, weight)])

	# Remove algumas arestas do grafo de acordo com peso
	edges_to_remove = []
	for node in finalGraph.nodes:
		for neighbor in finalGraph.neighbors(node):
			try:
				if finalGraph.get_edge_data(node, neighbor)['weight'] == finalGraph.get_edge_data(neighbor, node)['weight']:
					edges_to_remove.append((node, neighbor)) # Add edge to removal list
					edges_to_remove.append((neighbor, node)) # Add edge to removal list
				elif finalGraph.get_edge_data(node, neighbor)['weight'] > finalGraph.get_edge_data(neighbor, node)['weight']:
					edges_to_remove.append((neighbor, node)) # Add edge to removal list
				else:
					edges_to_remove.append((node, neighbor)) # Add edge to removal list
			except:
				print("An exception occurred")

	# Remove edges after iteration
	for edge in edges_to_remove:
		if finalGraph.has_edge(*edge):
			finalGraph.remove_edge(*edge)

#	print(f'\n imprimindo o grafo ciclico final:')
 #   pos = nx.spring_layout(finalGraph)

  #  options = {
   #	 "font_size": 10,
	#	"node_size": 1000,
	 #   "node_color": "white",
	  #  "edgecolors": "black",
	   # "linewidths": 1,
		#"width": 1,
	#}
	#nx.draw_networkx(finalGraph, pos, **options)

	# Set margins for the axes so that nodes aren't clipped
#	ax = plt.gca()
 #   ax.margins(0.20)
  #  plt.axis("off")
   # plt.show()

	return finalGraph, estimator.score(finalGraph)