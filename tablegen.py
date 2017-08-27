import time

class Table(object):
	def initWordListItems(self):
		self.wordListItems=[]
		for i in xrange(self.REGISTERS):
			self.wordListItems.append('self.wordList[int(r'+str(i)+'%len(self.wordList))]')
		for j in xrange(self.NUMBERLISTLENGTH):
			self.wordListItems.append('self.wordList[int(self.numberList['+str(j)+']%len(self.wordList))]')
	def numericObs(self,string):
		return 'self.numericObs[int('+string+'%len(self.numericObs))]'
	def stringObs(self,string):
		return 'self.stringObs[int('+string+'%len(self.stringObs))]'
	def __init__(self):
		self.NUMBERLISTLENGTH=4
		self.REGISTERS=4	#number of registers.
#		OBSERVATIONS=3	#length of observation vector.
		#operators=['+=','-=','*=','/=']
		operators=['+=','-=','*=']
		self.initWordListItems()
		self.miscInstructionsTable=[]
		self.miscInstructionsTable.append('for w1 in self.stringObs:\n\t\tfor w2 in self.wordList:\n\t\t\tself.myDictionary[w1]=w2')
		self.miscInstructionsTable.append('self.wordList.append(self.stringObs)')
		self.miscInstructionsTable.append('self.wordList.insert(0,self.stringObs)')
		self.miscInstructionsTable.append('if len(self.myDictionary)>0:\n\t\tself.myDictionary.popitem()')
		#self.miscInstructionsTable.append('for word in self.stringObs:\n\t\tself.wordList.append(word)')
		#self.miscInstructionsTable.append('for word in self.stringObs:\n\t\tself.wordList.insert(0,word)')
#		for i in xrange(1,self.wordListItems):
		for item1 in self.wordListItems:
			self.miscInstructionsTable.append('self.myString='+item1)
#			self.miscInstructionsTable.append('try:\n\t\tself.myString=next(obj for obj in self.myDictionary if obj.startswith('+item1+'))\n\texcept:\n\t\tpass')
			self.miscInstructionsTable.append('if '+item1+' in self.myDictionary:\n\t\tself.myString=self.myDictionary['+item1+']')
#			self.miscInstructionsTable.append('self.myString=self.myDictionary['+self.stringObs(item1)+']')
			for item2 in self.wordListItems:
				self.miscInstructionsTable.append('self.myDictionary['+item1+']='+item2)
			for i in xrange(self.NUMBERLISTLENGTH):
				self.miscInstructionsTable.append('self.myDictionary['+item1+']='+self.stringObs('self.numberList['+str(i)+']'))
				self.miscInstructionsTable.append('self.myDictionary['+self.stringObs('self.numberList['+str(i)+']')+']='+item1)
#		for i in xrange(0x41,(0x61+26)):
#			self.miscInstructionsTable.append('self.myString=chr('+str(i)+')')
		for i in xrange(self.NUMBERLISTLENGTH):
#			self.miscInstructionsTable.append('self.numberList['+str(i)+']='+'len(self.numericObs)')
			for j in xrange(self.NUMBERLISTLENGTH):
				#self.miscInstructionsTable.append('self.numberList['+str(i)+']='+'self.numericObs[int(self.numberList['+str(j)+']%len(self.numericObs))]')
				self.miscInstructionsTable.append('self.numberList['+str(i)+']='+self.numericObs('self.numberList['+str(j)+']'))
				if i!=j:
					self.miscInstructionsTable.append('self.numberList['+str(i)+']='+'self.numberList['+str(j)+']')
			for j in xrange(self.REGISTERS):
				self.miscInstructionsTable.append('r'+str(j)+'=self.numberList['+str(i)+']')
				self.miscInstructionsTable.append('self.numberList['+str(i)+']=r'+str(j))
		for i in xrange(self.REGISTERS):
#			self.miscInstructionsTable.append('self.myString=chr(int(r'+str(i)+'%256))')
			self.miscInstructionsTable.append('self.myString=self.wordList[int(r'+str(i)+'%len(self.wordList))]')
			for j in xrange(self.REGISTERS):
				if i!=j:
					self.miscInstructionsTable.append('r'+str(i)+'='+'r'+str(j))
				self.miscInstructionsTable.append('r'+str(i)+'='+'self.numericObs[int(r'+str(j)+'%len(self.numericObs))]')
				for operator in operators:
					self.miscInstructionsTable.append('r'+str(i)+operator+'r'+str(j))
					self.miscInstructionsTable.append('self.numberList['+str(i)+']'+operator+'self.numberList['+str(j)+']')
		self.FUNCTIONPREFIX='\t'
		for i in xrange(self.REGISTERS):
			self.FUNCTIONPREFIX+='r'+str(i)+'='
		self.FUNCTIONPREFIX+='0\n'
#		for i in xrange(self.REGISTERS):
#			self.FUNCTIONPREFIX+='\tr'+str(i)+'=len(self.numericObs)\n'
#			self.FUNCTIONPREFIX+='\tr'+str(i)+'=self.numericObs['+str(i%OBSERVATIONS)+']\n'
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
		self.MAINPREFIX='obsType=type(self.numericObs)\n'
		i=0
		for theType in typesList:
			if i>0:
				self.MAINPREFIX+='el'
			self.handleTypeNames.append('handle'+theType)
			self.MAINPREFIX+='if obsType==types.'+theType+':\n\tr0=self.handle'+theType+'(self)\n'
#			self.MAINPREFIX+='if obsType==types.'+theType+':\n\tr0=f1(self.numericObs)\n'
			i+=1
		#for i in xrange(1,self.REGISTERS):
		#	self.MAINPREFIX+='r'+str(i)+'=self.numericObs['+str(i%OBSERVATIONS)+']\n'
		#print self.MAINPREFIX
		condOpers=['<','>','<=','>=','==','!=']
		conditions=[]
		for i in xrange(self.NUMBERLISTLENGTH):
			for j in xrange(self.NUMBERLISTLENGTH):
				if i!=j:
					for condOp in condOpers:
						conditions.append('self.numberList['+str(i)+']'+condOp+'self.numberList['+str(j)+']')

		#assert(False)
		self.FUNCTIONS=2
		self.functionNames=[]
		for i in xrange(2):
			self.functionNames.append('f'+str(i))
		n=self.FUNCTIONS
		self.mainInstructionsTable=[]
		for i in xrange(n):
			self.mainInstructionsTable.append('self.'+self.functionNames[i]+'(self)')
			#for j in xrange(self.REGISTERS):
				#self.mainInstructionsTable.append('r'+str(j)+'=self.'+self.functionNames[i]+'(self)')
			for cond in conditions:
				self.mainInstructionsTable.append('if '+cond+':\n\t\t'+'self.'+self.functionNames[i]+'(self)')
				#for j in xrange(self.NUMBERLISTLENGTH):
					#self.mainInstructionsTable.append('if '+cond+':\n\t\tself.numberList['+str(j)+']'+'=self.'+self.functionNames[i]+'(self)')
#					print('if '+cond+'\n\tself.numberList['+str(j)+']'+'=self.'+self.functionNames[i]+'(self)')
		self.mainInstructionsTable+=self.miscInstructionsTable
		self.MISCITLENGTH=len(self.miscInstructionsTable)
		self.MAINITLENGTH=len(self.mainInstructionsTable)
