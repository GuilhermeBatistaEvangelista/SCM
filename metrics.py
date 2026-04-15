
import networkx as nx

class Metrics():
	def __init__(self):
		super().__init__()

		self.originalGraph = None
		self.newGraph = None

		self.value = {
			"distance": 0,
			"correctEdges": 0,
			"additionalEdges": 0,
			"missingEdges": 0,
			"accuracy": 0,
			"reversedEdges": 0,
			"errorEdges": 0,
			"accuracy": 0,
			"TPR": 0,
			"numberOfEdgesNotPresent": 0,
			"FPR": 0,
			"precision": 0,
			"recall": 0,
		}
	def setGraphs(self, originalGraph, newGraph):
		self.originalGraph = originalGraph
		self.newGraph = newGraph

	def getMetrics(self, originalGraph, newGraph):
		self.value['distance'] = nx.graph_edit_distance(originalGraph, newGraph)
		self.value['correctEdges'] = self.getNumberOfCorrectEdges(originalGraph, newGraph)
		self.value['additionalEdges'] = self.getNumberOfAdditionalEdges(originalGraph, newGraph)
		self.value['missingEdges'] = self.getNumberOfMissingEdges(originalGraph, newGraph)
		self.value['accuracy'] = self.calculateAccuracy(originalGraph, newGraph)
		self.value['reversedEdges'] = self.getNumberOfReverseEdges(originalGraph, newGraph)
		self.value['errorEdges'] = self.value['additionalEdges'] + self.value['missingEdges'] + self.value['reversedEdges']
		self.value['accuracy'] = self.value['correctEdges'] / (self.value['correctEdges'] + self.value['errorEdges'])
		self.value['TPR'] = self.value['correctEdges'] / originalGraph.number_of_edges()

		numNodes = originalGraph.number_of_nodes()
		numEdgesTotal = numNodes*(numNodes-1)
		self.value['numberOfEdgesNotPresent'] = numEdgesTotal - originalGraph.number_of_edges()
		self.value['FPR'] = self.value['additionalEdges'] / self.value['numberOfEdgesNotPresent']

		self.value['precision'] = self.value['correctEdges'] / newGraph.number_of_edges()
		self.value['recall'] = self.value['correctEdges'] / originalGraph.number_of_edges()
		
		return self.value
		

	def printMetrics(self):
		print(f'\nDistancia entre os grafos original e induzido: {self.value['distance']}')
		print(f'\nNúmero de arestas corretas: {self.value['correctEdges']}')
		print(f'Número de arestas adicionais: {self.value['additionalEdges']}')
		print(f'Número de arestas faltantes: {self.value['missingEdges']}')
		print(f'Acurácia: {self.value['accuracy']}')
		print(f'TPR: {self.value['TPR']}')
		print(f'FPR: {self.value['FPR']}')
		print(f'Precision: {self.value['precision']}')
		print(f'Recall: {self.value['recall']}')

	def getNumberOfCorrectEdges(self, originalGraph, newGraph):
		correctEdges = 0
		for node in originalGraph.nodes:
			for neighbor in originalGraph.neighbors(node):
				if newGraph.has_edge(node, neighbor):
					correctEdges += 1

		return correctEdges

	def getNumberOfAdditionalEdges(self, originalGraph, newGraph):
		additionalEdges = 0
		for node in newGraph.nodes:
			for neighbor in newGraph.neighbors(node):
				if not originalGraph.has_edge(node, neighbor):
					additionalEdges += 1

		return additionalEdges

	def getNumberOfMissingEdges(self, originalGraph, newGraph):

		missingEdges = 0
		for node in originalGraph.nodes:
			for neighbor in originalGraph.neighbors(node):
				if not newGraph.has_edge(node, neighbor):
					missingEdges += 1

		return missingEdges

	def getNumberOfReverseEdges(self, originalGraph, newGraph):
		reverseEdges = 0
		for node in newGraph.nodes:
			for neighbor in newGraph.neighbors(node):
				if originalGraph.has_edge(neighbor, node):
					reverseEdges += 1

		return reverseEdges

	def calculateAccuracy(self, originalGraph, newGraph):
		# accuracy is the result of acc = correct edges / (correct edges + error edges)
		correctEdges = self.getNumberOfCorrectEdges(originalGraph, newGraph)
		errorEdges = self.getNumberOfAdditionalEdges(originalGraph, newGraph) + self.getNumberOfMissingEdges(originalGraph, newGraph)# + getNumberOfReverseEdges(originalGraph, newGraph)
		accuracy = correctEdges / (correctEdges + errorEdges)

		return accuracy
