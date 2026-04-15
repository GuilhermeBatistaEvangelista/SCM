import os
from FilesHandler import FileHandler
from Test import Test
from algorithms.SCM_generator import Generator

from pgmpy.estimators import K2Score, AICScore, BDeuScore, BDsScore, BicScore

class Cli():
	def __init__(self):
		super().__init__()

		self.fileHandler = FileHandler()
		self.test = Test(self.fileHandler)
		self.generator = Generator()

		self.setup()
		

	def setup(self):
		self.fileHandler.list_files()
		if len(self.fileHandler.datasetFiles) < 1:
			print("No files on /datasets")
			return False
		
		os.system('cls' if os.name == 'nt' else 'clear')
		
		print("File(s):")
		for file in self.fileHandler.datasetFiles:
			print(file)

		os.system('cls' if os.name == 'nt' else 'clear')

		return True

	def show(self):
		os.system('cls' if os.name == 'nt' else 'clear')
		print("Found Files: ")
		for  index, file in enumerate(self.fileHandler.datasetFiles):
			print(f"	{index} - {file[8:]}")

		print("\nCommands:")
		print("	Test: parentsN, namePath")
		print("	Gen: n, n_endo, n_cycles, p_join, namePath")
		print("\nEnter 'exit'|'close'|'quit'|'end'  to end execution.\n")

	def read(self):
		text = input()

		if text.strip().upper() in  ["EXIT", "CLOSE", "QUIT", "END"]:
			return False
		
		command, text = (text.split(':') + [None, None])[:2]
		command = command.strip().upper()
		if(command == "TEST"):
			self.run_test(text)
		if(command == "GEN"):
			self.run_generator(text)
		return True

	def wait(self):
		print("\nConfirm to proceed.")
		input()
		

	def run_test(self, text):
		if(len(text.split(',')) < 2):
			print(f"Missing arguments...")

		parents_number, namePath = text.strip().split(',')

		self.test.test("", K2Score, int(parents_number), namePath.strip())
		self.wait()

	def run_generator(self, text):
		if(len(text.split(',')) < 5):
			print(f"Missing arguments...")

		n, n_endo, n_cycles, p_join, namePath = text.strip().split(',')

		self.generator.generateSCM(int(n), int(n_endo), int(n_cycles), float(p_join), namePath.strip())
		self.wait()