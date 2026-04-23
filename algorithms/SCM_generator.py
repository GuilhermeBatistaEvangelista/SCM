
import semopy
import random
import os
import time

class Generator():
	def __init__(self):
		super().__init__()
		self.path = "datasets"

	def writeSEMInFile(self, namePath, sem):
		nameFile = os.path.join(self.path, namePath)
		file = open(nameFile, 'w')
		file.write(sem)
		file.close()

	def generateSCM(self, n, n_endo, n_cycles, p_join, namePath):
		random.seed(time.time())

		#Graph
		modgen = semopy.model_generation
		desc = modgen.generate_desc(n_endo, n_exo=0, n_lat=0, n_inds=0, n_cycles=n_cycles, p_join=p_join)
		#desc = modgen.generate_desc(n_endo, n_exo=0, n_lat=0, n_inds=0, n_cycles=3, p_join=0.05)
		print(desc)
		self.writeSEMInFile(namePath + "SEM.txt", desc)

		#Parameters
		params, tmp = modgen.generate_parameters(desc)
		data = modgen.generate_data(tmp, n)
		#print(data.head())
		nameFile = os.path.join(self.path, namePath + ".csv")
		data.to_csv(nameFile, index=False)