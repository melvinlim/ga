import random
import types
import sys
TIME=200
CAPACITY=200	#maintain this many organisms.
REPLACEMENTS=20
MAXFITNESS=1.0
from organism import Organism
from environment import Environment
myDictionary=[]
myDictionary.append('hi')
myDictionary.append('??')
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
	a=random.randint(0,1000)
	obs=[x,y,z,a]
	desired_response=[]
	desired_response+=[x*y+z*a]
	desired_response+=[x+y+z+a]
	desired_string_response=[]
	command=random.randint(0,1)
	if command==1:
		desired_string_response+='hi'
	else:
		desired_string_response+='??'
	obs.append(command)
	for organism in organisms:
		total_response=organism.step([obs,myDictionary])
		if total_response:
			[numerical_response,string_response]=total_response
			error=0

			if numerical_response:
				for i in range(len(desired_response)):
					error+=abs(numerical_response[i]-desired_response[i])
			else:
				error+=sum(desired_response)

			n=min(len(string_response),len(desired_string_response))
			for i in range(n):
				error+=abs(ord(string_response[i])-ord(desired_string_response[i]))
			m=max(len(string_response),len(desired_string_response))
			error+=(m-n)*100

			lengthPenalty=organism.chromosome.rnaLength*1
			fitness=1.0/((error)+1.0+lengthPenalty)
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
				organisms[z].assign(MAXFITNESS)
			else:
				organisms[y]=env.crossOrganisms(organisms[x],organisms[z])
				organisms[y].assign(MAXFITNESS)
		elif organisms[x].fitness>=organisms[z].fitness:
			organisms[z]=env.crossOrganisms(organisms[x],organisms[y])
			organisms[z].assign(MAXFITNESS)
		else:
			organisms[x]=env.crossOrganisms(organisms[y],organisms[z])
			organisms[x].assign(MAXFITNESS)
				
#	print organisms
print rankings[-1]
b=rankings[-1][1]
print b.step([obs,myDictionary])
print desired_response,desired_string_response
