import random
import time
REGISTERS=4	#number of registers.
OBSERVATIONS=3	#length of observation vector.
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
PREFIX=''
for i in range(REGISTERS):
	PREFIX+='r'+str(i)+'=obs['+str(i%OBSERVATIONS)+']\n'
LUTLENGTH=len(instructionsTable)
class Chromosome(object):
	random.seed(time.time())
	def __init__(self,functions=None,functionLength=10):
		self.functionLength=functionLength
		if functions==None:
			self.generateFunctionList()
		else:
			self.functions=functions
		self.functionsLength=len(self.functions)
		self.generateInstructions()
		self.rnaLength=len(self.rna)
#	def epigenetic(self,obs):
#		self.functions=self.generateFunctionList(obs)
#		self.rna=self.generateInstructions(obs)
	def genFunc(self,obs=None):
		func=[]
		for i in range(self.functionLength):
			tmp=instructionsTable[random.randint(0,LUTLENGTH-1)]
			func.append(tmp)
		return func
	def generateFunctionList(self,obs=None):
		self.functions=[]
		self.functions.append(self.genFunc())
	def generateInstructions(self,obs=None):
		ans=''
		for function in self.functions[1:]:
			pass
		ans+=PREFIX
		main=self.functions[0]
		for instruction in main:
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
