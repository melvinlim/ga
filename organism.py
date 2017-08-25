from chromosome import Chromosome
class Organism(object):
	def __init__(self,tables,functions=None):
		self.chromosome=Chromosome(tables=tables,functions=functions)
	def peek(self):
		return self.chromosome.rna
	def step(self,obs):
		return self.chromosome.execute(obs)
	def assign(self,fitness):
		self.fitness=fitness
