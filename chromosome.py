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
	def epigenetic(self,obs):
		self.dna=self.generate(obs)
		self.rna=self.transcribe(obs)
	def generate(self,obs=None):
		dna=[]
		for i in range(self.dnaLength):
			tmp=dnaLib[random.randint(0,DNALIBLENGTH-1)]
			dna.append(tmp)
		return dna
	def transcribe(self,obs=None):
		rna=''
		for bp in self.dna:
			tmp=rnaLib[bp]
			randint=random.randint(0,len(tmp)-1)
			tmp=tmp[randint]
			rna+=tmp+'\n'
		return rna
