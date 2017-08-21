TIME=1000
from organism import Organism
for t in range(TIME):
	o=Organism()
	response=o.step([2,3])
	if response:
		print str(t)+':'+str(response)
