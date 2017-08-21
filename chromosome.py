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
	def __init__(self,length=10):
		self.dnaLength=length
		self.dna=self.generate()
		self.rna=self.transcribe()
		self.rnaLength=len(self.rna)
	def generate(self):
		dna=[]
		for i in range(self.dnaLength):
			tmp=dnaLib[random.randint(0,DNALIBLENGTH-1)]
			dna.append(tmp)
		#dna='x=obs[0]\ny=obs[1]\nz=x*y'
		return dna
	def transcribe(self):
		rna=''
		for bp in self.dna:
			tmp=rnaLib[bp]
			randint=random.randint(0,len(tmp)-1)
			tmp=tmp[randint]
			rna+=tmp+'\n'
		return rna
