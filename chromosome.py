instructions=['']
class Chromosome(object):
	def __init__(self,length=10):
		self.dna=self.generate()
		self.length=length
	def generate(self):
		dna=''
#		for i in range(self.length):
		#dna='x=input1\ny=input2\nz=x*y'
		dna='x=obs[0]\ny=obs[1]\nz=x*y'
		return dna
