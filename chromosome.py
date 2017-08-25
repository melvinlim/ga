import random
import sys
import time
DEBUG=True
DEBUG=False
class Chromosome(object):
	random.seed(time.time())
	def __init__(self,tables,functions=None,functionLength=10):
		self.tables=tables
		self.functionLength=functionLength
		if functions==None:
			self.generateFunctionDict()
		else:
			self.functions=functions
		self.functionsLength=len(self.functions)
		self.generateInstructions()
		#print self.rna
		self.rnaLength=len(self.rna)
#	def epigenetic(self,obs):
#		self.functions=self.generateFunctionDict(obs)
#		self.rna=self.generateInstructions(obs)
	#def genMainFunc(self,obs=None):
	def genInputFunc(self,obs=None):
		self.mainFunctionLength=10
		n=len(self.functionNames)
		mainInstructionsTable=[]
		for i in xrange(n):
			for j in xrange(self.tables.REGISTERS):
				mainInstructionsTable.append('r'+str(j)+'='+self.functionNames[i]+'(obs)')
		MLUTLENGTH=len(mainInstructionsTable)
		func=[]
		for i in xrange(self.mainFunctionLength):
			tmp=mainInstructionsTable[random.randint(0,MLUTLENGTH-1)]
			func.append(tmp)
		return func
	def genFunc(self,obs=None):
		func=[]
		for i in xrange(self.functionLength):
			tmp=self.tables.instructionsTable[random.randint(0,self.tables.LUTLENGTH-1)]
			func.append(tmp)
		return func
	def generateFunctionDict(self,obs=None):
		FUNCTIONS=2
		self.functionNames=[]
		for i in xrange(FUNCTIONS):
			self.functionNames.append('f'+str(i))
		self.functions={}
#		self.functions['main']=self.genMainFunc()
		self.functions['main']=self.genInputFunc()
		self.functions['misc']=[]
		self.functions['input']={}
		for i in xrange(FUNCTIONS):
			self.functions['misc'].append(self.genFunc())
		for name in self.tables.handleTypeNames:
			self.functions['input'][name]=self.genInputFunc()
	def generateInstructions(self,obs=None):
		ans=''
		i=0
		for function in self.functions['misc']:
			ans+='def f'+str(i)+'(obs):\n'
			ans+=self.tables.FUNCTIONPREFIX
			for instruction in function:
				ans+='\t'+instruction+'\n'
			ans+='\treturn r0\n'
			i+=1
		for function in self.functions['input']:
			ans+='def '+function+'(obs):\n'
			for instruction in self.functions['input'][function]:
				ans+='\t'+instruction+'\n'
			ans+='\treturn r0\n'
		ans+=self.tables.MAINPREFIX
		main=self.functions['main']
		for instruction in main:
			ans+=instruction+'\n'
		self.rna=ans
	def execute(self,obs):
		rna=self.rna
		r0=None
		try:
			exec(rna)
		except:
			if DEBUG:
				print self.rna
				print "Unexpected error:", sys.exc_info()
				time.sleep(1)
			r0=None
		return r0
