import networkx as nx

def modified_dmbc(dataset, rootVariable, estimator, parents_nmax):
	model = nx.DiGraph()
	nodes = list(dataset.columns)  # Names of the nodes
	model.add_nodes_from(nodes)
	#for node in nodes:
	for i in range(1, len(nodes)):
		node = nodes[i]
		previous_nodes = [n for n in nodes if n != node]  # Nodes in all node list
		#previous_nodes = [n for n in nodes if nodes.index(n) < nodes.index(node)]  # Nodes preceding the current node
		parents = []  # Parents of the current node
		P_old = estimator.local_score(node, parents)
		temp = -1;
		while (len(parents) < parents_nmax) and len(parents) != temp: # While less than max and not stuck on loop
			temp = len(parents)
			# Filtra os nós candidatos que não são pais do nó atual
			candidates = [c for c in previous_nodes if c not in parents]
			best_candidate = None
			count = 0
			for candidate in candidates:
				if (candidate == rootVariable) or (rootVariable in parents):
					P_new = estimator.local_score(node, parents + [candidate])
					if P_new > P_old:
						best_candidate = candidate
						P_old = P_new
				# sai do loop quando não é filho da classe ou a classe nao pertence aos pais
				else:
					break
				if best_candidate is not None:
					parents.append(best_candidate)  # Adiciona o melhor candidato à lista de pais
					model.add_edge(best_candidate, node)  # Adiciona uma aresta do melhor candidato para o nó atual
				else:
					break

	# Retorna o modelo como um DAG e sua pontuação total
	return model#, estimator.score(model)