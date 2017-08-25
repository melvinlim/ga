import time

class Table(object):
	def __init__(self):
		self.MYLISTLENGTH=4
		self.REGISTERS=4	#number of registers.
#		OBSERVATIONS=3	#length of observation vector.
		#operators=['+=','-=','*=','/=']
		operators=['+=','-=','*=']
		self.instructionsTable=[]
		for i in xrange(self.MYLISTLENGTH):
			self.instructionsTable.append('self.myList['+str(i)+']='+'len(obs)')
			self.instructionsTable.append('r1=self.myList['+str(i)+']')
			self.instructionsTable.append('self.myList['+str(i)+']=r1')
			for j in xrange(self.MYLISTLENGTH):
				self.instructionsTable.append('self.myList['+str(i)+']='+'obs[int(self.myList['+str(j)+']%len(obs))]')
				if i!=j:
					self.instructionsTable.append('self.myList['+str(i)+']='+'self.myList['+str(j)+']')
					self.instructionsTable.append('r'+str(i)+'='+'r'+str(j))
		for i in xrange(self.REGISTERS):
			for j in xrange(self.REGISTERS):
				self.instructionsTable.append('r'+str(i)+'='+'obs[int(r'+str(j)+'%len(obs))]')
				for operator in operators:
					self.instructionsTable.append('r'+str(i)+operator+'r'+str(j))
		self.FUNCTIONPREFIX=''
		for i in xrange(self.REGISTERS):
			self.FUNCTIONPREFIX+='\tr'+str(i)+'=0\n'
#			self.FUNCTIONPREFIX+='\tr'+str(i)+'=len(obs)\n'
			#self.FUNCTIONPREFIX+='\tr'+str(i)+'=obs['+str(i%OBSERVATIONS)+']\n'
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
		self.MAINPREFIX='obsType=type(obs)\n'
		i=0
		for theType in typesList:
			if i>0:
				self.MAINPREFIX+='el'
			self.handleTypeNames.append('handle'+theType)
			self.MAINPREFIX+='if obsType==types.'+theType+':\n\tr0=self.handle'+theType+'(self,obs)\n'
#			self.MAINPREFIX+='if obsType==types.'+theType+':\n\tr0=f1(obs)\n'
			i+=1
		#for i in xrange(1,self.REGISTERS):
		#	self.MAINPREFIX+='r'+str(i)+'=obs['+str(i%OBSERVATIONS)+']\n'
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
				self.mainInstructionsTable.append('r'+str(j)+'=self.'+self.functionNames[i]+'(self,obs)')
		self.LUTLENGTH=len(self.instructionsTable)
		self.MLUTLENGTH=len(self.mainInstructionsTable)
