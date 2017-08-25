import random
import types
import sys
TIME=200
CAPACITY=200	#maintain this many organisms.
REPLACEMENTS=20
from organism import Organism
from environment import Environment
organisms=[]
env=Environment()
for n in xrange(CAPACITY):
	o=Organism(tables=env.table)
	organisms.append(o)
for t in xrange(TIME):
	rankings=[]
	x=random.randint(0,1000)
	y=random.randint(0,1000)
	z=random.randint(0,1000)
	obs=[x,y,z]
	desired_response=x*y+z
	for organism in organisms:
		response=organism.step(obs)
		if response:
			error=response-desired_response
			#print str(t)+':'+str(response)
			fitness=abs(error)+len(organism.chromosome.rna)*1
			fitness=1.0/(fitness+1.0)
		else:
			fitness=0
		organism.assign(fitness)
			#fitness=None
		rankings.append([fitness,organism])
	rankings.sort()
#	print rankings[-1][1].step(obs),desired_response
	for i in xrange(REPLACEMENTS):
		[x,y,z]=random.sample(xrange(0,CAPACITY),3)
		if organisms[x].fitness>=organisms[y].fitness:
			if organisms[y].fitness>=organisms[z].fitness:
				organisms[z]=env.crossOrganisms(organisms[x],organisms[y])
				organisms[z].assign(0)
			else:
				organisms[y]=env.crossOrganisms(organisms[x],organisms[z])
				organisms[y].assign(0)
		elif organisms[x].fitness>=organisms[z].fitness:
			organisms[z]=env.crossOrganisms(organisms[x],organisms[y])
			organisms[z].assign(0)
		else:
			organisms[x]=env.crossOrganisms(organisms[y],organisms[z])
			organisms[x].assign(0)
				
#	print organisms
print rankings[-1]
b=rankings[-1][1]
