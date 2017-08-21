from chromosome import Chromosome
class Organism(object):
	def __init__(self):
		self.chromosome=Chromosome()
		self.chromosome.generate()
	def step(self,obs):
		rna=self.chromosome.rna
#		print rna
		r0=None
		try:
			exec(rna)
		except:
			r0=None
		return r0
