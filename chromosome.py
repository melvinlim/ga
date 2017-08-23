import random
import time
operator=['=','+=','-=','*=','/=']
OPERATORS=len(operator)
OBSERVATIONS=2	#length of observation vector.
REGISTERS=4	#number of registers.
dnaLib=['RX = OBS','RX OP RX']
DNALIBLENGTH=len(dnaLib)
rnaLib={}
for bp in dnaLib:
	rnaLib[bp]=[]
for i in range(REGISTERS):
	for j in range(OBSERVATIONS):
		rnaLib['RX = OBS'].append('r'+str(i)+'='+'obs['+str(j)+']')
for i in range(REGISTERS):
	for j in range(REGISTERS):
		for k in range(OPERATORS):
			rnaLib['RX OP RX'].append('r'+str(i)+operator[k]+'r'+str(j))
class Chromosome(object):
	random.seed(time.time())
	def __init__(self,dna=None,length=10):
		self.dnaLength=length
		if dna==None:
			self.dna=self.generate()
		else:
			self.dna=dna
		self.rna=self.transcribe()
		self.rnaLength=len(self.rna)
		self.dnaLength=self.rnaLength
	def epigenetic(self,obs):
		self.dna=self.generate(obs)
		self.rna=self.transcribe(obs)
	def genFunc(self,obs=None):
		tmp=[]
		for i in range(self.dnaLength):
			instruction=dnaLib[random.randint(0,DNALIBLENGTH-1)]
			tmp.append(instruction)
		func=''
		for bp in tmp:
			tmp=rnaLib[bp]
			randint=random.randint(0,len(tmp)-1)
			tmp=tmp[randint]
			func+=tmp+'\n'
		return func
	def generate(self,obs=None):
		self.functions=[]
		dna=self.genFunc()
		return dna
	def transcribe(self,obs=None):
		rna=self.dna
		return rna
	def execute(self,obs):
		rna=self.rna
		r0=None
		try:
			exec(rna)
		except:
			r0=None
		return r0
