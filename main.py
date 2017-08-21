import random
TIME=1000
from organism import Organism
organisms=[]
for t in range(TIME):
	o=Organism()
	x=random.randint(0,1000)
	y=random.randint(0,1000)
	z=random.randint(0,1000)
	obs=[x,y,z]
	desired_response=x*y+z
	response=o.step(obs)
	if response:
#		print str(t)+':'+str(response)
		fitness=abs(response-desired_response)
	else:
		fitness=9999
	organisms.append([fitness,o])
organisms.sort()
#print organisms
