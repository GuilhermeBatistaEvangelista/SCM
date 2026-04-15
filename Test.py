import semopy
import networkx as nx
from metrics import Metrics

from algorithms.DMBBN import dmbbn
from algorithms.DMBCG import dmbcg

#Hints
from FilesHandler import FileHandler


class Test():
	def __init__(self, fileHandler: FileHandler):
		super().__init__()

		self.fileHandler = fileHandler
		self.metricsUtils = Metrics()

	def test(self, stimator, score, parents_number: int, namePath: str):
		graph_origin = nx.DiGraph()

		print(f'Iniciando experimentos....')
		print(f'	Reading file....')
		dataset  = self.fileHandler.read_dataset(namePath + "Data")

		print(f'	Running algorithm....')
		model, score_metric = dmbcg(dataset, score, parents_number, parents_number)
		#model, score_metric = dmbbn(dataset, score, parents_number, parents_number)

		print(f'\nMODELO: {model}\n\nPONTUAÇÃO: {score_metric}')
		graph_origin = self.fileHandler.file_to_graph(namePath + "SEM")


		print(f'\nComparando o grafo induzido pelo DMBBN ao grafo original do SCM:')
		metrics = self.metricsUtils.getMetrics(graph_origin, model)
			
		print(f'\nSCM gerado a partir do DMBBN:')
		scm_str = self.fileHandler.graph_to_string(model)
		scm_cycle = semopy.Model(scm_str)
		print(scm_cycle)

			#  Ajusta o modelo SCM e exibe os resultados
		res = scm_cycle.fit(dataset)
		print(res)
		
		ins = scm_cycle.inspect()
		print(ins)
		print(f'\nFit indices:')
		stats = semopy.calc_stats(scm_cycle)
		print(stats.T)

		self.fileHandler.writeResultFile(namePath, str(model), str(score), metrics, str(res), str(ins), str(stats.T))
		self.fileHandler.writeExperimentResultsFile(namePath, str(score), metrics)
