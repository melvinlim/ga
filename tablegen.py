import time

class Table(object):
	def __init__(self):
		self.REGISTERS=4	#number of registers.
		OBSERVATIONS=3	#length of observation vector.
		operators=['+=','-=','*=','/=']
		#operators=['+=','-=','*=']
		self.instructionsTable=[]
		for i in xrange(self.REGISTERS):
			for j in xrange(self.REGISTERS):
				if i!=j:
					self.instructionsTable.append('r'+str(i)+'='+'r'+str(j))
		for i in xrange(self.REGISTERS):
			for j in xrange(OBSERVATIONS):
				self.instructionsTable.append('r'+str(i)+'='+'obs['+str(j)+']')
		for i in xrange(self.REGISTERS):
			for j in xrange(self.REGISTERS):
				for operator in operators:
					self.instructionsTable.append('r'+str(i)+operator+'r'+str(j))
		self.FUNCTIONPREFIX=''
		for i in xrange(self.REGISTERS):
			self.FUNCTIONPREFIX+='\tr'+str(i)+'=obs['+str(i%OBSERVATIONS)+']\n'
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
		#	if i>0:
		#		self.MAINPREFIX+='el'
			self.handleTypeNames.append('handle'+theType)
		#	self.MAINPREFIX+='if obsType==types.'+theType+':\n\tr0=handle'+theType+'(obs)\n'
			i+=1
		#for i in xrange(1,self.REGISTERS):
		#	self.MAINPREFIX+='r'+str(i)+'=obs['+str(i%OBSERVATIONS)+']\n'
		#print self.MAINPREFIX
		#assert(False)
		self.LUTLENGTH=len(self.instructionsTable)
