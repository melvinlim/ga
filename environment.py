import random
from organism import *
def randint(a,b):
	return random.randint(a,b)
def heads():
	if randint(0,1):
		return True
	return False
def concatDNA(x,y):
	xt=randint(1,len(x))
	yt=randint(0,len(y)-1)
	c=x[:xt]+y[yt:]
	return c
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
		x=a.chromosome.dna
		y=b.chromosome.dna
		c=self.crossDNA(x,y)
		return Organism(c)
