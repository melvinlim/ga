import random
import sys
import time
import types
DEBUG=True
#DEBUG=False
class Chromosome(object):
	random.seed(time.time())
	def __init__(self,tables,functions=None,functionLength=10,persistentMemory=None):
		if persistentMemory:
			self.myDictionary=persistentMemory
		else:
#			self.myDictionary={}
			self.myDictionary=[]
		self.tables=tables
		self.functionLength=functionLength
		self.numberList=[None]*self.tables.NUMBERLISTLENGTH
		if functions==None:
			self.generateFunctionDict()
		else:
			self.functions=functions
		self.functionsLength=len(self.functions)
		self.generateInstructions()
#	def epigenetic(self,allObs):
#		self.functions=self.generateFunctionDict(allObs)
#		self.rna=self.generateInstructions(allObs)
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
	def NListToString(self,a,a0):
		ret=''
		if a:
			for x in a[a0:]:
				ret+=chr(int(x)%256)
		return ret
	def stringToNList(self,obs):
		val=[]
		for l in obs:
			val.append(ord(l))
		return val
	def execute(self,allObs):
		[self.numericObs,self.stringObs,self.wordList]=allObs
#		print self.wordList
		#print self.numericObs,self.stringObs
		#self.numericLen=len(self.numericObs)
		self.numericLen=2
		numberRep=self.stringToNList(self.stringObs)
		self.numericObs+=numberRep
		self.stringObs=''
		#print self.numericObs,self.stringObs
		#assert False
		self.myString=''
		self.numberList=[0]*self.tables.NUMBERLISTLENGTH
#		self.myDictionary.clear()
		try:
			self.f0(self)
			self.go(self)
			self.f1(self)
			try:
				for i in xrange(len(self.numberList)):
					self.numberList[i]=float(self.numberList[i])
			except:
				if DEBUG:
					print 'huge number was assigned to something'
				self.numberList=None
		except:
			if DEBUG:
				for ins in self.rna:
					print ins
				print "Unexpected error:", sys.exc_info()
				time.sleep(1)
			self.numberList=None
		self.myString=self.NListToString(self.numberList,self.numericLen)
		return [self.numberList,self.myString]
