import random
import types
import sys
TIME=200000
CAPACITY=200	#maintain this many organisms.
REPLACEMENTS=20
MAXFITNESS=1.0
EVALSPERTIMESTEP=2
from organism import Organism
from environment import Environment
env=Environment(capacity=CAPACITY,replacements=REPLACEMENTS,maxfitness=MAXFITNESS,evalsPerTimeStep=EVALSPERTIMESTEP)
for t in xrange(TIME):
	env.step(t)
