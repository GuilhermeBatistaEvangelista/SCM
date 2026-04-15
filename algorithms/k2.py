import networkx as nx

def k2(dataset, estimator, parents_nmax):
	"""
	Constrói uma Rede Bayesiana utilizando o algoritmo K2.

	Parâmetros:
	dataset: Conjunto de dados contendo as variáveis.
	estimator: Um objeto estimador que fornece o método local_score.
	parents_nmax: Número máximo de pais permitidos para cada nó (padrão é 2).

	Retorna:
	Uma tupla contendo a Rede Bayesiana e sua pontuação.
	"""
	model = nx.DiGraph()
	nodes = list(dataset.columns)  # Names of the nodes
	model.add_nodes_from(nodes)
	#for node in nodes:
	for i in range(1, len(nodes)):
		node = nodes[i]
		#previous_nodes = [n for n in nodes if n != node]  # Nodes in all node list
		previous_nodes = [n for n in nodes if nodes.index(n) < nodes.index(node)]  # Nodes preceding the current node
		parents = []  # Parents of the current node
		P_old = estimator.local_score(node, parents)
		# Enquanto o número de pais for menor que o máximo permitido
		while len(parents) < parents_nmax:
			# Filtra os nós candidatos que não são pais do nó atual
			candidates = [c for c in previous_nodes if c not in parents]
			# Encontra o melhor candidato a pai com base na pontuação local
			best_candidate = max(candidates, key=lambda x: estimator.local_score(node, parents + [x]), default=None)
			#print(candidates)  # Exibe os candidatos a pais

			# Se não houver um candidato melhor ou a pontuação não melhorar, sai do loop
			if best_candidate is None or estimator.local_score(node, parents + [best_candidate]) <= P_old:
				break

			# Atualiza a pontuação anterior com a nova pontuação do melhor candidato
			P_old = estimator.local_score(node, parents + [best_candidate])
			parents.append(best_candidate)  # Adiciona o melhor candidato à lista de pais
			model.add_edge(best_candidate, node)  # Adiciona uma aresta do melhor candidato para o nó atual

	# Retorna o modelo como um DAG e sua pontuação total
	return model, estimator.score(model)