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
	def initWordList(self):
#		try:
#			fp=open('/usr/share/dict/words','r')
#			self.wordList=fp.read().strip('\r ').split('\n')
#			self.wordList.append('42')
#		except:
			self.wordList=[]
			self.wordList.append('nothing')
			self.wordList.append('42')
	def __init__(self,capacity,replacements,maxfitness,evalsPerTimeStep=1):
		self.evalsPerTimeStep=evalsPerTimeStep
		self.CAPACITY=capacity
		self.REPLACEMENTS=replacements
		self.MAXFITNESS=maxfitness
		self.contents=[]
		self.table=tablegen.Table()
		self.initWordList()
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
		self.best=self.rankings[-1][1]
		i=1
		for ex in self.recentExamples:
			[numericObs,stringObs,des]=ex
			print str(i)+'. resp:',
			print self.best.step([numericObs,stringObs,self.wordList])
			print str(i)+'. desi:',
			print des
			i+=1
	def genNumericProb(self,obs):
		x=obs[0]
		y=obs[1]
		z=obs[2]
		a=obs[3]
		desired_numerical_response=[]
		desired_numerical_response+=[x*y+z*a]
		desired_numerical_response+=[x+y+z+a]
		return desired_numerical_response
	def genStringProb(self,obs):
		desired_string_response=[]
		if(obs[4]>=500):
			obs[4]=1
			desired_string_response+='nothing'
		else:
			obs[4]=0
			desired_string_response+='42'
		return desired_string_response
	def getNumericError(self,numerical_response,desired_numerical_response):
		numerical_error=0
		max_numerical_error=0
		for i in xrange(len(desired_numerical_response)):
			max_numerical_error+=abs(desired_numerical_response[i])
		if numerical_response!=None:
			for i in xrange(len(desired_numerical_response)):
				numerical_error+=abs(numerical_response[i]-desired_numerical_response[i])
		else:
			numerical_error=max_numerical_error
		if numerical_error>max_numerical_error:
			numerical_error=max_numerical_error
		#numerical_error/=float(max_numerical_error)
		return numerical_error
	def getStringError(self,string_response,desired_string_response):
		string_error=0
		n=min(len(string_response),len(desired_string_response))
		m=max(len(string_response),len(desired_string_response))
		max_string_error=0
		for i in xrange(n):
			string_error+=abs(ord(string_response[i])-ord(desired_string_response[i]))
			max_string_error+=abs(ord(desired_string_response[i]))
		max_char_error=max_string_error*1.0/float(m)
		string_error+=abs(m-n)*max_char_error
		max_string_error+=abs(m-n)*max_char_error
		if string_error>max_string_error:
			string_error=max_string_error
		if string_response=='':		#high error for not responding with anything.
			string_error=4*max_string_error
		#string_error/=float(max_string_error)
		return string_error
	def getFitness(self,organism,total_response,target):
		if total_response:
			[numerical_response,string_response]=total_response
			[desired_numerical_response,desired_string_response]=target

			numerical_error=self.getNumericError(numerical_response,desired_numerical_response)

			string_error=self.getStringError(string_response,desired_string_response)

			lengthPenalty=organism.chromosome.rnaLength/100.0
			fitness=1.0/(numerical_error+string_error+1.0+lengthPenalty)
		else:
			fitness=0
		return fitness
	def threeWayTournament(self):
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
	def genExample(self):
		numericObs=[]
		numericObsTargetLen=5
		for i in xrange(numericObsTargetLen):
			numericObs.append(random.randint(0,1000))
		desired_numerical_response=self.genNumericProb(numericObs)
		desired_string_response=self.genStringProb(numericObs)
		if desired_string_response=='hi':
			stringObs='Hello.'
		else:
			stringObs='...'
		target=[desired_numerical_response,desired_string_response]
		return [numericObs,stringObs,target]
	def genExamples(self,n):
		examples=[]
		for i in xrange(n):
			examples.append(self.genExample())
		return examples
	def step(self,t):
		self.rankings=[]

		self.recentExamples=self.genExamples(self.evalsPerTimeStep)

		for i in xrange(len(self.organisms)):
			organism=self.organisms[i]
			fitness=0

			for example in self.recentExamples:
				[numericObs,stringObs,target]=example

				total_response=organism.step([numericObs,stringObs,self.wordList])
				if total_response[0]==None:
					self.organisms[i]=Organism(tables=self.table)
					self.organisms[i].assign(self.MAXFITNESS)
				else:
					fitness+=self.getFitness(organism,total_response,target)

			organism.assign(fitness)
			self.rankings.append([fitness,organism])

		self.rankings.sort()
		if t%500==0:
			self.status()

		for i in xrange(self.REPLACEMENTS):
			self.threeWayTournament()
