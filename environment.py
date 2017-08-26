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
	def __init__(self,capacity,replacements,maxfitness):
		self.CAPACITY=capacity
		self.REPLACEMENTS=replacements
		self.MAXFITNESS=maxfitness
		self.contents=[]
		self.table=tablegen.Table()
		self.myDictionary=[]
		self.myDictionary.append('hi')
		self.myDictionary.append('??')
		self.organisms=[]
		for n in xrange(self.CAPACITY):
			o=Organism(tables=self.table)
			self.organisms.append(o)
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
	def status(self):
		print self.rankings[-1]
		best=self.rankings[-1][1]
		print best.step([self.latest_obs,self.myDictionary])
		#print desired_numerical_response,desired_string_response
		print self.desired_response
	def step(self,t):
		self.rankings=[]
		x=random.randint(0,1000)
		y=random.randint(0,1000)
		z=random.randint(0,1000)
		a=random.randint(0,1000)
		self.latest_obs=[x,y,z,a]
		desired_numerical_response=[]
		desired_numerical_response+=[x*y+z*a]
		desired_numerical_response+=[x+y+z+a]
		desired_string_response=[]
		command=random.randint(0,1)
		if command==1:
			desired_string_response+='hi'
		else:
			desired_string_response+='??'
		self.latest_obs.append(command)
		for organism in self.organisms:
			total_response=organism.step([self.latest_obs,self.myDictionary])
			if total_response:
				[numerical_response,string_response]=total_response

				numerical_error=0
				if numerical_response:
					for i in range(len(desired_numerical_response)):
						numerical_error+=abs(numerical_response[i]-desired_numerical_response[i])
				else:
					numerical_error+=sum(desired_numerical_response)

				string_error=0
				n=min(len(string_response),len(desired_string_response))
				for i in range(n):
					string_error+=abs(ord(string_response[i])-ord(desired_string_response[i]))*40
				m=max(len(string_response),len(desired_string_response))
				string_error+=abs(m-n)*200
#				string_error=0

				lengthPenalty=organism.chromosome.rnaLength*1
				fitness=1.0/(numerical_error+string_error+1.0+lengthPenalty)
			else:
				fitness=0
			organism.assign(fitness)
				#fitness=None
			self.rankings.append([fitness,organism])
		self.rankings.sort()
		self.desired_response=[desired_numerical_response,desired_string_response]
		if t%500==0:
			self.status()

		for i in xrange(self.REPLACEMENTS):
			[x,y,z]=random.sample(xrange(0,self.CAPACITY),3)
			if self.organisms[x].fitness>=self.organisms[y].fitness:
				if self.organisms[y].fitness>=self.organisms[z].fitness:
					self.organisms[z]=self.crossOrganisms(self.organisms[x],self.organisms[y])
					self.organisms[z].assign(self.MAXFITNESS)
				else:
					self.organisms[y]=self.crossOrganisms(self.organisms[x],self.organisms[z])
					self.organisms[y].assign(self.MAXFITNESS)
			elif self.organisms[x].fitness>=self.organisms[z].fitness:
				self.organisms[z]=self.crossOrganisms(self.organisms[x],self.organisms[y])
				self.organisms[z].assign(self.MAXFITNESS)
			else:
				self.organisms[x]=self.crossOrganisms(self.organisms[y],self.organisms[z])
				self.organisms[x].assign(self.MAXFITNESS)
