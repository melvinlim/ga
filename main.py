import random
FAIL=99999999999
TIME=1000
CAPACITY=100	#maintain this many organisms.
REPLACEMENTS=5
from organism import Organism
from environment import Environment
organisms=[]
env=Environment()
for n in range(CAPACITY):
	o=Organism()
	organisms.append(o)
for t in range(TIME):
	rankings=[]
	x=random.randint(0,1000)
	y=random.randint(0,1000)
	z=random.randint(0,1000)
	obs=[x,y,z]
	desired_response=x*y+z
	for i in range(len(organisms)):
		response=organisms[i].step(obs)
		if response:
			try:
				error=response-desired_response
			except:
				fitness=FAIL
			#print str(t)+':'+str(response)
			fitness=abs(error)+len(organisms[i].chromosome.rna)*1
		else:
			fitness=FAIL
			#fitness=None
#		if fitness:
		rankings.append([fitness,organisms[i]])
	rankings.sort()
	print rankings[:3]
	nextOrganisms=[]
	for i in range(CAPACITY-REPLACEMENTS):
		nextOrganisms.append(rankings[i][1])
	for i in range(0,(2*REPLACEMENTS),2):
		nextOrganisms.append(env.crossOrganisms(rankings[i][1],rankings[i][1]))
	organisms=nextOrganisms
#	print organisms
