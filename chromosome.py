import random
import sys
import time
import types
DEBUG=True
#DEBUG=False
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
		func=[]
		for i in xrange(self.mainFunctionLength):
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
#		self.functions['main']=self.genMainFunc()
		self.functions['main']=self.genInputFunc()
		self.functions['misc']=[]
		self.functions['input']={}
		for i in xrange(self.tables.FUNCTIONS):
			self.functions['misc'].append(self.genFunc())
		for name in self.tables.handleTypeNames:
			self.functions['input'][name]=self.genInputFunc()
	def generateInstructions(self,obs=None):
		ans=''
		i=0
		for function in self.functions['misc']:
			ans='def f'+str(i)+'(obs):\n'
			ans+=self.tables.FUNCTIONPREFIX
			for instruction in function:
				ans+='\t'+instruction+'\n'
			ans+='\treturn r0\n'
			#ans+='self.f'+str(i)+'=types.MethodType(f'+str(i)+',self)\n'
			ans+='self.f'+str(i)+'=f'+str(i)+'\n'
			exec(ans)
			i+=1
		for function in self.functions['input']:
			ans='def '+function+'(obs):\n'
			for instruction in self.functions['input'][function]:
				ans+='\t'+instruction+'\n'
			ans+='\treturn r0\n'
			#ans+='self.'+function+'=types.MethodType('+function+',self)\n'
			ans+='self.'+function+'='+function+'\n'
			exec(ans)
		ans='def go(self,obs):\n'
		ans+=self.tables.FUNCTIONPREFIX
		main=self.functions['main']
		for instruction in main:
			ans+='\t'+instruction+'\n'
		#ans+='self.go=types.MethodType(go,self)\n'
		ans+='\treturn r0\n'
		ans+='self.go=go\n'
		exec(ans)
		self.rna=ans
	def execute(self,obs):
		rna=self.rna
		r0=None
		try:
			r0=self.go(self,obs)
			#exec(rna)
		except:
			if DEBUG:
				print self.rna
				print "Unexpected error:", sys.exc_info()
				time.sleep(1)
			r0=None
		return r0
