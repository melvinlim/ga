from chromosome import Chromosome
class Organism(object):
	def __init__(self,tables,functions=None,persistentMemory=None):
		self.chromosome=Chromosome(tables=tables,functions=functions,persistentMemory=persistentMemory)
	def peek(self,i=None):
		if i!=None:
			print self.chromosome.rna[i]
		else:
			for i in xrange(len(self.chromosome.rna)):
				print str(i)+': ',
				print self.chromosome.rna[i].split('\n')[0]
	def step(self,allObs):
		return self.chromosome.execute(allObs=allObs)
	def assign(self,fitness):
		self.fitness=fitness
