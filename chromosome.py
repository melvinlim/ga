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
FUNCTIONPREFIX=''
for i in range(REGISTERS):
	FUNCTIONPREFIX+='\tr'+str(i)+'=obs['+str(i%OBSERVATIONS)+']\n'
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
		print self.rna
		self.rnaLength=len(self.rna)
#	def epigenetic(self,obs):
#		self.functions=self.generateFunctionList(obs)
#		self.rna=self.generateInstructions(obs)
	def genMainFunc(self,obs=None):
		self.mainFunctionLength=10
		n=len(self.functionNames)
		mainInstructionsTable=[]
		for i in range(n):
			for j in range(REGISTERS):
				mainInstructionsTable.append('r'+str(j)+'='+self.functionNames[i]+'(obs)')
		MLUTLENGTH=len(mainInstructionsTable)
		func=[]
		for i in range(self.mainFunctionLength):
			tmp=mainInstructionsTable[random.randint(0,MLUTLENGTH-1)]
			func.append(tmp)
		return func
	def genFunc(self,obs=None):
		func=[]
		for i in range(self.functionLength):
			tmp=instructionsTable[random.randint(0,LUTLENGTH-1)]
			func.append(tmp)
		return func
	def generateFunctionList(self,obs=None):
		FUNCTIONS=2
		self.functionNames=[]
		for i in range(FUNCTIONS):
			self.functionNames.append('f'+str(i))
		self.functions=[]
		self.functions.append(self.genMainFunc())
		for i in range(FUNCTIONS):
			self.functions.append(self.genFunc())
	def generateInstructions(self,obs=None):
		ans=''
		i=0
		for function in self.functions[1:]:
			ans+='def f'+str(i)+'(obs):\n'
			ans+=FUNCTIONPREFIX
			for instruction in function:
				ans+='\t'+instruction+'\n'
			ans+='\treturn r0\n'
			i+=1
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
