import time

class Table(object):
	def __init__(self):
		self.MYLISTLENGTH=4
		self.REGISTERS=4	#number of registers.
#		OBSERVATIONS=3	#length of observation vector.
		#operators=['+=','-=','*=','/=']
		operators=['+=','-=','*=']
		self.instructionsTable=[]
		for i in xrange(0x41,(0x61+26)):
			self.instructionsTable.append('self.myString+=chr('+str(i)+')')
		for i in xrange(self.MYLISTLENGTH):
			self.instructionsTable.append('self.myList['+str(i)+']='+'len(self.obs)')
			self.instructionsTable.append('r1=self.myList['+str(i)+']')
			for j in xrange(self.MYLISTLENGTH):
				self.instructionsTable.append('self.myList['+str(i)+']='+'self.obs[int(self.myList['+str(j)+']%len(self.obs))]')
				if i!=j:
					self.instructionsTable.append('self.myList['+str(i)+']='+'self.myList['+str(j)+']')
					self.instructionsTable.append('r'+str(i)+'='+'r'+str(j))
			for j in xrange(self.REGISTERS):
					self.instructionsTable.append('self.myList['+str(i)+']=r'+str(j))
		for i in xrange(self.REGISTERS):
			self.instructionsTable.append('self.myString+=chr(int(r'+str(i)+'%256))')
			self.instructionsTable.append('self.myString+=self.myDictionary[int(r'+str(i)+'%len(self.myDictionary))]')
			for j in xrange(self.REGISTERS):
				self.instructionsTable.append('r'+str(i)+'='+'self.obs[int(r'+str(j)+'%len(self.obs))]')
				for operator in operators:
					self.instructionsTable.append('r'+str(i)+operator+'r'+str(j))
					#self.instructionsTable.append('self.myList['+str(i)+']'+operator+'self.myList['+str(j)+']')
		self.FUNCTIONPREFIX='\t'
		for i in xrange(self.REGISTERS):
			self.FUNCTIONPREFIX+='r'+str(i)+'='
		self.FUNCTIONPREFIX+='0\n'
#		for i in xrange(self.REGISTERS):
#			self.FUNCTIONPREFIX+='\tr'+str(i)+'=len(self.obs)\n'
#			self.FUNCTIONPREFIX+='\tr'+str(i)+'=self.obs['+str(i%OBSERVATIONS)+']\n'
		import types
		typesList=dir(types)
		toBeRemoved=[]
		for t in typesList:
			if t[0]=='_':
				toBeRemoved.append(t)
		for t in toBeRemoved:
			typesList.remove(t)
		typesList=['ListType','StringType']
		self.handleTypeNames=[]
		self.MAINPREFIX='obsType=type(self.obs)\n'
		i=0
		for theType in typesList:
			if i>0:
				self.MAINPREFIX+='el'
			self.handleTypeNames.append('handle'+theType)
			self.MAINPREFIX+='if obsType==types.'+theType+':\n\tr0=self.handle'+theType+'(self)\n'
#			self.MAINPREFIX+='if obsType==types.'+theType+':\n\tr0=f1(self.obs)\n'
			i+=1
		#for i in xrange(1,self.REGISTERS):
		#	self.MAINPREFIX+='r'+str(i)+'=self.obs['+str(i%OBSERVATIONS)+']\n'
		#print self.MAINPREFIX
		#assert(False)
		self.FUNCTIONS=2
		self.functionNames=[]
		for i in range(2):
			self.functionNames.append('f'+str(i))
		n=self.FUNCTIONS
		self.mainInstructionsTable=[]
		for i in xrange(n):
			for j in xrange(self.REGISTERS):
				self.mainInstructionsTable.append('r'+str(j)+'=self.'+self.functionNames[i]+'(self)')
		self.LUTLENGTH=len(self.instructionsTable)
		self.MLUTLENGTH=len(self.mainInstructionsTable)
