import semopy
import matplotlib.pyplot as plt
import os
import zipfile
#import bnlearn as bn
import numpy as np
import pandas as pd
import networkx as nx
from pgmpy.estimators import K2Score, AICScore, BDeuScore, BDsScore, BicScore
#from pgmpy.models import BayesianNetwork
from typing import List, Tuple


from CLI import Cli
from GUI import Window





def main():
	RUN = True
	cli = Cli()

	while RUN:
		cli.show()

		if not cli.read():
			break

main()

#root = Window()
#root.mainloop()