import random
import sys
import time
import types
DEBUG=True
#DEBUG=False
class Chromosome(object):
	random.seed(time.time())
	def __init__(self,tables,functions=None,functionLength=10):
		self.myDictionary={}
		self.tables=tables
		self.functionLength=functionLength
		self.myList=[None]*self.tables.MYLISTLENGTH
		if functions==None:
			self.generateFunctionDict()
		else:
			self.functions=functions
		self.functionsLength=len(self.functions)
		self.generateInstructions()
#	def epigenetic(self,obs):
#		self.functions=self.generateFunctionDict(obs)
#		self.rna=self.generateInstructions(obs)
	def genMainFunc(self,obs=None):
		self.mainFunctionLength=4
		func=[]
		for i in xrange(self.mainFunctionLength):
			tmp=self.tables.mainInstructionsTable[random.randint(0,self.tables.MAINITLENGTH-1)]
			func.append(tmp)
		return func
	def genInputFunc(self,obs=None):
		self.inputFunctionLength=10
		func=[]
		for i in xrange(self.inputFunctionLength):
			tmp=self.tables.mainInstructionsTable[random.randint(0,self.tables.MAINITLENGTH-1)]
			func.append(tmp)
		return func
	def genMiscFunc(self,obs=None):
		func=[]
		for i in xrange(self.functionLength):
			tmp=self.tables.miscInstructionsTable[random.randint(0,self.tables.MISCITLENGTH-1)]
			func.append(tmp)
		return func
	def generateFunctionDict(self,obs=None):
		self.functions={}
		self.functions['main']=self.genMainFunc()
		self.functions['misc']=[]
		self.functions['input']={}
		for i in xrange(self.tables.FUNCTIONS):
			self.functions['misc'].append(self.genMiscFunc())
		for name in self.tables.handleTypeNames:
			self.functions['input'][name]=self.genInputFunc()
	def generateInstructions(self,obs=None):
		totalInstructionLength=0
		self.rna=[]
		ans=''
		i=0
		for function in self.functions['misc']:
			ans='def f'+str(i)+'(self):\n'
			ans+=self.tables.FUNCTIONPREFIX
			for instruction in function:
				ans+='\t'+instruction+'\n'
			#ans+='\treturn r0\n'
			#ans+='self.f'+str(i)+'=types.MethodType(f'+str(i)+',self)\n'
			ans+='self.f'+str(i)+'=f'+str(i)+'\n'
			exec(ans)
			totalInstructionLength+=len(ans)
			self.rna.append(ans)
			i+=1
		for function in self.functions['input']:
			ans='def '+function+'(self):\n'
			ans+=self.tables.FUNCTIONPREFIX
			for instruction in self.functions['input'][function]:
				ans+='\t'+instruction+'\n'
			#ans+='\treturn r0\n'
			#ans+='self.'+function+'=types.MethodType('+function+',self)\n'
			ans+='self.'+function+'='+function+'\n'
			exec(ans)
			totalInstructionLength+=len(ans)
			self.rna.append(ans)
		ans='def go(self):\n'
		ans+=self.tables.FUNCTIONPREFIX
		main=self.functions['main']
		for instruction in main:
			ans+='\t'+instruction+'\n'
		#ans+='self.go=types.MethodType(go,self)\n'
		#ans+='\treturn r0\n'
		ans+='self.go=go\n'
		exec(ans)
		totalInstructionLength+=len(ans)
		self.rna.append(ans)
		self.rnaLength=totalInstructionLength
		self.rnaLength+=len(self.myDictionary)
	def execute(self,obs):
		[self.obs,self.wordList]=obs
		self.myString=''
		self.myList=[0]*self.tables.MYLISTLENGTH
		try:
			#self.myList[0]=self.go(self)
			self.go(self)
			try:
				for i in xrange(len(self.myList)):
					self.myList[i]=float(self.myList[i])
			except:
				if DEBUG:
					print 'huge number was assigned to something'
				self.myList=None
		except:
			if DEBUG:
				print self.rna
				print "Unexpected error:", sys.exc_info()
				time.sleep(1)
			self.myList=None
		return [self.myList,self.myString]
