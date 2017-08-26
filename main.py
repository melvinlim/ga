import random
import types
import sys
TIME=200000
CAPACITY=2000	#maintain this many organisms.
REPLACEMENTS=20
MAXFITNESS=1.0
from organism import Organism
from environment import Environment
env=Environment(capacity=CAPACITY,replacements=REPLACEMENTS,maxfitness=MAXFITNESS)
for t in xrange(TIME):
	env.step(t)
