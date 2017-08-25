import random
from organism import *
import tablegen
def randint(a,b):
	return random.randint(a,b)
def heads():
	if randint(0,1):
		return True
	return False
def concatInstructions(x,y):
	#these force c to be atleast 2 instructions in size.
	#xt=randint(1,len(x))
	#yt=randint(0,len(y)-1)

	#these allow c to be an empty array.
	xt=randint(0,len(x))
	yt=randint(0,len(y))
	c=x[:xt]+y[yt:]
	return c
#x and y are lists of functions.  functions are lists of instructions.
#function 0 is the main function.  for now x and y are the same length.
def concatDNA(x,y):
	assert(len(x)==len(y))
	result={}
	result['main']=concatInstructions(x['main'],y['main'])
	n=len(x['misc'])
	result['misc']=[]
	for i in xrange(n):
		result['misc'].append(concatInstructions(x['misc'][i],y['misc'][i]))
	result['input']={}
	keys=x['input'].keys()
	for key in keys:
		result['input'][key]=concatInstructions(x['input'][key],y['input'][key])
	return result
class Environment(object):
	def __init__(self):
		self.contents=[]
		self.table=tablegen.Table()
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
		return Organism(tables=self.table,functions=c)
