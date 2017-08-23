import random
TIME=10
CAPACITY=100	#maintain this many organisms.
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
			#print str(t)+':'+str(response)
			fitness=abs(response-desired_response)
		else:
			fitness=9999999999
			#fitness=None
#		if fitness:
		rankings.append([fitness,organisms[i]])
	rankings.sort()
	print rankings[:3]
	nextOrganisms=[]
	for i in range(CAPACITY-5):
		nextOrganisms.append(rankings[i][1])
	for i in range(0,10,2):
		nextOrganisms.append(env.crossOrganisms(rankings[i][1],rankings[i][1]))
	organisms=nextOrganisms
#	print organisms
