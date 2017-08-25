from chromosome import Chromosome
class Organism(object):
	def __init__(self,tables,functions=None):
		self.chromosome=Chromosome(tables=tables,functions=functions)
	def peek(self,i=None):
		if i!=None:
			print self.chromosome.rna[i]
		else:
			for i in range(len(self.chromosome.rna)):
				print str(i)+': ',
				print self.chromosome.rna[i].split('\n')[0]
	def step(self,obs):
		return self.chromosome.execute(obs)
	def assign(self,fitness):
		self.fitness=fitness
