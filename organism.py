from chromosome import Chromosome
class Organism(object):
	def __init__(self,dna=None):
		self.chromosome=Chromosome(dna)
	def peek(self):
		return self.chromosome.rna
	def step(self,obs):
		return self.chromosome.execute(obs)
