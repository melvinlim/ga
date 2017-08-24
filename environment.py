import random
from organism import *
def randint(a,b):
	return random.randint(a,b)
def heads():
	if randint(0,1):
		return True
	return False
def concatInstructions(x,y):
	xt=randint(1,len(x))
	yt=randint(0,len(y)-1)
	c=x[:xt]+y[yt:]
	return c
#x and y are lists of functions.  functions are lists of instructions.
#function 0 is the main function.  for now x and y are the same length.
def concatDNA(x,y):
	assert(len(x)==len(y))
	n=len(x)
	result=[]
	for i in range(n):
		result.append(concatInstructions(x[i],y[i]))
	return result
class Environment(object):
	def __init__(self):
		self.contents=[]
	def add(self,x):
		self.contents.append(x)
	def crossDNA(self,x,y):
		if heads():
			return concatDNA(x,y)
		else:
			return concatDNA(y,x)
	def crossOrganisms(self,a,b):
		x=a.chromosome.functions
		y=b.chromosome.functions
		c=self.crossDNA(x,y)
		return Organism(c)
