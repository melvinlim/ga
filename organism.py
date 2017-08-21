from chromosome import Chromosome
class Organism(object):
	def __init__(self):
		self.chromosome=Chromosome()
	def step(self,obs):
		return 0
