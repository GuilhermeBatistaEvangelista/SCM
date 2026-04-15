import os
import pandas as pd
import networkx as nx

class FileHandler():
	def __init__(self):
		super().__init__()

		self.path = "datasets"
		self.datasetFiles = []

	def list_files(self):
		filesList = []
		for root, dirs, files in os.walk(self.path):
			for file in files:
					filesList.append(os.path.join(root, file))
		
		self.datasetFiles = filesList
		return filesList

	def read_dataset(self, file):
		dataset = pd.read_csv(os.path.join(self.path, file + '.csv'))
		return dataset

	def file_to_graph(self, fileGraph):
		graph = nx.DiGraph()

		with open(os.path.join(self.path, fileGraph + '.txt'), 'r') as arquivo:
			conteudo = arquivo.read()
			print(f'Arquivo SCM:\n {conteudo}')

		# Measurement part:
		# add the variables as nodes in graph
		for linhas in conteudo.split('\n'):
			if linhas.find('=~')!=-1:
				#print(f'\nlinhas: {linhas}')
				for linha in linhas.split():
					if linha != '=~' and linha != '+' and not graph.has_node(linha):
						graph.add_node(linha)

		# add the edges in graph
		for linhas in conteudo.split('\n'):
			if linhas.find('~')!=-1:
				str_aux = []
				#print(f'\nlinhas: {linhas}')
				for linha in linhas.split():
					if linha != '~' and linha != '+':
						str_aux.append(linha)
				node = str_aux[0]
				#print(f'\nnode: {node}')
				for i in range(len(str_aux)-1):
					#print(f'node: {str_aux[i+1]} -> {node}')
					graph.add_edge(str_aux[i+1], node)

		# # Structural part:
		# add the variables as nodes in graph
		for linhas in conteudo.split('\n'):
			if linhas.find('~')!=-1:
				#print(f'\nlinhas: {linhas}')
				for linha in linhas.split():
					if linha != '~' and linha != '+' and not graph.has_node(linha):
						graph.add_node(linha)

		# add the edges in graph
		for linhas in conteudo.split('\n'):
			if linhas.find('~')!=-1:
				str_aux = []
				#print(f'\nlinhas: {linhas}')
				for linha in linhas.split():
					if linha != '~' and linha != '+':
						str_aux.append(linha)
				node = str_aux[0]
				#print(f'\nnode: {node}')
				for i in range(len(str_aux)-1):
					#print(f'node: {str_aux[i+1]} -> {node}')
					graph.add_edge(str_aux[i+1], node)

		#print(f'\nNodes do grafo: {graph.nodes}')
		#print(f'\nArestas do grafo: {graph.edges()}')

		return graph

	def graph_to_string(self, graph):
		graph_to_iterate = nx.DiGraph()
		graph_to_iterate.add_nodes_from(graph.nodes)

		str_nome = ''
		str_structural = '# structural part' + '\n'
		str_measurement = '\n# measurement part' + '\n'
		str_covariances = '\n# covariance part' + '\n'
		str_file = ''

		for node in graph.nodes:
			for neighbor in graph.neighbors(node):
				if graph.has_edge(node, neighbor):
					graph_to_iterate.add_edge(node, neighbor)

		# para construir a parte estrutural e de medição
		#print(f'\nArestas do grafo: {graph_to_iterate.edges.data()}')
		for node in graph_to_iterate.nodes:
			str_nome = node + '~'
			predecessors = list(graph_to_iterate.predecessors(node))
			if predecessors!=[]:
				str_nome = node + ' ~ '
				for i in range(len(predecessors)):
					str_nome = str_nome + predecessors[i] # Access by index instead of pop
					if i < len(predecessors) - 1: # Add '+' only if there are more successors
						str_nome = str_nome + ' + '
				str_structural = str_structural + str_nome + '\n'

			# para construir a parte de medição
			#sucessors = list(graph.successors(node))
			#if sucessors!=[]:
			#   str_nome = node + ' =~ '
			#  print(f'\nsucessores de cada node: {sucessors}')
				# Iterate using index to remove elements correctly
			#  for i in range(len(sucessors)):
			#     str_nome = str_nome + sucessors[i] # Access by index instead of pop
				#    if i < len(sucessors) - 1: # Add '+' only if there are more successors
				#       str_nome = str_nome + ' + '
				#str_measurement = str_measurement + str_nome + '\n'

		# Para construir a parte de covariancias
		#graph_to_iterate.clear()
		#graph_to_iterate.add_nodes_from(graph.nodes)
		#for a, b in graph.edges:
		#   if graph.has_edge(b, a) and graph.has_edge(a, b):
		#     if not graph_to_iterate.has_edge(a, b) and not graph_to_iterate.has_edge(b, a):
		#       graph_to_iterate.add_edge(a, b)

		#for a, b in graph_to_iterate.edges:
		#   str_nome = a + ' ~~ ' + b + '\n'
		#  str_covariances = str_covariances + str_nome

		str_file = str_structural + str_measurement + str_covariances
		print(f'\n {str_file}')
		return str_file


	def writeResultFile(self, nameFile, model, score, metrics, fitModel, inspection, stats):
		namePath = "results"
		file = open(os.path.join(namePath, nameFile + '.txt'), 'w')
		file.write(model + '\n' + score + '\n')
		file.write('distance' + ',' + str(metrics['distance']) + '\n')
		file.write(str(metrics['correctEdges']) + ',' + str(metrics['additionalEdges']) + ',' + str(metrics['missingEdges']) + ',' + str(metrics['TPR']) + ',' + str(metrics['FPR']) + ',' + str(metrics['precision']) + ',' + str(metrics['recall']) + ',' + str(metrics['accuracy']) + '\n')
		file.write(fitModel + '\n')
		file.write(inspection + '\n')
		file.write(stats + '\n')
		file.close()

	def writeExperimentResultsFile(self, nameFile, score, metrics):
		namePath = "results"
		file = open(os.path.join(namePath, nameFile + '.csv'), 'a')
		file.write(nameFile + ',' + score + ',' + str(str(metrics['distance'])) + ',' + str(metrics['correctEdges']) + ',' + str(metrics['additionalEdges']) + ',' + str(metrics['missingEdges']) + ',' + str(metrics['TPR']) + ',' + str(metrics['FPR']) + ',' + str(metrics['precision']) + ',' + str(metrics['recall']) + ',' + str(metrics['accuracy']) + '\n')
		file.close()
