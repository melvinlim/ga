import random
import sys
import time
import types
DEBUG=True
DEBUG=False
class Chromosome(object):
	random.seed(time.time())
	def __init__(self,tables,functions=None,functionLength=10):
		self.tables=tables
		self.functionLength=functionLength
		self.myList=[0]*self.tables.MYLISTLENGTH
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
	def genMainFunc(self,obs=None):
		self.mainFunctionLength=2
		func=[]
		for i in xrange(self.mainFunctionLength):
			tmp=self.tables.mainInstructionsTable[random.randint(0,self.tables.MLUTLENGTH-1)]
			func.append(tmp)
		return func
	def genInputFunc(self,obs=None):
		self.inputFunctionLength=10
		func=[]
		for i in xrange(self.inputFunctionLength):
			tmp=self.tables.mainInstructionsTable[random.randint(0,self.tables.MLUTLENGTH-1)]
			func.append(tmp)
		return func
	def genFunc(self,obs=None):
		func=[]
		for i in xrange(self.functionLength):
			tmp=self.tables.instructionsTable[random.randint(0,self.tables.LUTLENGTH-1)]
			func.append(tmp)
		return func
	def generateFunctionDict(self,obs=None):
		self.functions={}
		self.functions['main']=self.genMainFunc()
		self.functions['misc']=[]
		self.functions['input']={}
		for i in xrange(self.tables.FUNCTIONS):
			self.functions['misc'].append(self.genFunc())
		for name in self.tables.handleTypeNames:
			self.functions['input'][name]=self.genInputFunc()
	def generateInstructions(self,obs=None):
		til=0
		ans=''
		i=0
		for function in self.functions['misc']:
			ans='def f'+str(i)+'(self,obs):\n'
			ans+=self.tables.FUNCTIONPREFIX
			for instruction in function:
				ans+='\t'+instruction+'\n'
			ans+='\treturn r0\n'
			#ans+='self.f'+str(i)+'=types.MethodType(f'+str(i)+',self)\n'
			ans+='self.f'+str(i)+'=f'+str(i)+'\n'
			exec(ans)
			i+=1
		til+=len(ans)
		for function in self.functions['input']:
			ans='def '+function+'(self,obs):\n'
			for instruction in self.functions['input'][function]:
				ans+='\t'+instruction+'\n'
			ans+='\treturn r0\n'
			#ans+='self.'+function+'=types.MethodType('+function+',self)\n'
			ans+='self.'+function+'='+function+'\n'
			exec(ans)
		til+=len(ans)
		ans='def go(self,obs):\n'
		ans+=self.tables.FUNCTIONPREFIX
		main=self.functions['main']
		for instruction in main:
			ans+='\t'+instruction+'\n'
		#ans+='self.go=types.MethodType(go,self)\n'
		ans+='\treturn r0\n'
		ans+='self.go=go\n'
		exec(ans)
		til+=len(ans)
		self.rna=ans
		self.rnaLength=til
	def execute(self,obs):
		rna=self.rna
		r0=None
		try:
			self.myList=[0]*self.tables.MYLISTLENGTH
			r0=self.go(self,obs)
			#r0=self.myList[0]
			try:
				r0=float(r0)
			except:
				if DEBUG:
					print 'r0 assigned huge number'
				r0=None
			#exec(rna)
		except:
			if DEBUG:
				print self.rna
				print "Unexpected error:", sys.exc_info()
				time.sleep(1)
			r0=None
		return r0
