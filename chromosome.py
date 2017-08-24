import random
import time
REGISTERS=4	#number of registers.
OBSERVATIONS=2	#length of observation vector.
operators=['+=','-=','*=','/=']
instructionsTable=[]
for i in range(REGISTERS):
	for j in range(REGISTERS):
		instructionsTable.append('r'+str(i)+'='+'r'+str(j))
for i in range(REGISTERS):
	for j in range(OBSERVATIONS):
		instructionsTable.append('r'+str(i)+'='+'obs['+str(j)+']')
for i in range(REGISTERS):
	for j in range(REGISTERS):
		for operator in operators:
			instructionsTable.append('r'+str(i)+operator+'r'+str(j))
LUTLENGTH=len(instructionsTable)
class Chromosome(object):
	random.seed(time.time())
	def __init__(self,dna=None,length=10):
		self.dnaLength=length
		if dna==None:
			self.generateFunctionList()
		else:
			self.dna=dna
		self.dnaLength=len(self.dna)
		self.generateInstructions()
		self.rnaLength=len(self.rna)
#	def epigenetic(self,obs):
#		self.dna=self.generateFunctionList(obs)
#		self.rna=self.generateInstructions(obs)
	def genFunc(self,obs=None):
		func=[]
		for i in range(self.dnaLength):
			tmp=instructionsTable[random.randint(0,LUTLENGTH-1)]
			func.append(tmp)
		return func
	def generateFunctionList(self,obs=None):
		self.functions=[]
		self.dna=self.genFunc()
	def generateInstructions(self,obs=None):
		ans=''
		for instruction in self.dna:
			ans+=instruction+'\n'
		self.rna=ans
	def execute(self,obs):
		rna=self.rna
		r0=None
		try:
			exec(rna)
		except:
			r0=None
		return r0
