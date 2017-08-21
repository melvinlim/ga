from chromosome import Chromosome
class Organism(object):
	def __init__(self):
		self.chromosome=Chromosome()
		self.chromosome.generate()
	def step(self,obs):
		dna=self.chromosome.dna
		print dna
		z=None
		exec(dna)
		return z
