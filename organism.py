from chromosome import Chromosome
class Organism(object):
	def __init__(self,dna=None):
		self.chromosome=Chromosome(dna)
	def step(self,obs):
		return self.chromosome.execute(obs)
