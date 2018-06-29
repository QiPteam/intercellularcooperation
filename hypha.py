#!/usr/bin/python
from cell import *
from env import *
from interaction import *
import matplotlib.pyplot as plt
import pandas as pd
import sys
#import pdb

"""
This class describes a fungus hypha in interaction with its environment

"""
__author__ =  'Adelin Barbacci _(;,;)_'
__team__ = 'QIP _(;,;)_'
__version__=  '0.0'
__nonsense__ = 'hypha'

class hypha:
	def __init__(self):
		"""
		Construct a new hypha object:
			no input parameter
			return nothing
		"""
		self.interaction = []
		self.ratio = []


	def append(self,i):
		"""
		Append new interaction in hyphal
		"""
		self.interaction.append(i)

	def next(self):
		"""
		Compute the next step of hyphal development
		"""
		for i in self.interaction:
			i.next_ext()

		self.diffuse()
#		self.divide()

	def diffuse(self):
		"""
		Compute diffusion in hyphal and in environment
		"""
		temp_ratio = 0
		for ii in range(0,len(self.interaction)-1):
			i1 = self.interaction[ii]
			i2 = self.interaction[ii+1]
			# Gradient hyp = same cell volume
			cdf = i1.c.Nf[-1]-i2.c.Nf[-1]
			# New value for the first cell
			i1.c.Nf.append(i1.c.Nf[-1]-i1.c.D*cdf)
			i1.c.func.append(i1.c.func[-1])

			i1.e.Nf.append(i1.e.Nf[-1])
			i1.e.func.append(i1.e.func[-1])

			if (i1.c.func[-1] == "Center") & (i2.c.func[-1] == "Margin"):
				temp_ratio = i1.c.D*cdf
			#i2.e.Nf.append(i2.e.Nf[-1])
			#i2.e.func.append(i2.e.func[-1])
			# Updating tmp value for cell ii+1
			if ii < len(self.interaction)-2:
				i2.c.Nf[-1] = i2.c.Nf[-1]+i1.c.D*cdf
			# New value for the last cell
			if ii == len(self.interaction)-2:
				i2.c.Nf.append(i2.c.Nf[-1]+i1.c.D*cdf)
				i2.c.func.append(i2.c.func[-1])
				i2.e.Nf.append(i2.e.Nf[-1])
				i2.e.func.append(i2.e.func[-1])
				if temp_ratio != 0:
					self.ratio.append(i1.c.D*cdf/temp_ratio)
				else:
					self.ratio.append(0)

	def divide(self):
		"""
		Model the daughter cell creation by the mother cell
		"""
		if (self.interaction[-1].c.Nf[-1] >= self.interaction[-1].c.div_thres) & (self.interaction[-1].c.div_thres !=0):
			#Update Mother cell concentrations
			self.interaction[-1].c.Nf[-1] -= self.interaction[-1].c.div_thres
			self.interaction[-1].c.Nf[-1] *= 0.5
			#New daugther cell
			#print(self.interaction[-2].c.file)
			c1   = cell(self.interaction[-2].c.file)
			c1.Nf[0] = self.interaction[-1].c.Nf[-1]
			# c1.func.append("Margin")
			e1   = self.interaction[-1].e
			n1   = interaction(c1,e1,self.interaction[-1].DOL)
			#Mother cell
#			print(self.interaction[-1].c.file)
			c2    = cell(self.interaction[-1].c.file)
			c2.Nf = self.interaction[-1].c.Nf
			c2.func = self.interaction[-1].c.func
			#c2.func.append("Margin")
			e2    = env(self.interaction[-1].e.file)
			n2    = interaction(c2,e2,self.interaction[-1].DOL)
#			pdb.set_trace()
			# Add the new cell
			self.interaction.pop()
			self.interaction.append(n1)
			self.interaction.append(n2)

	def cont(self):
		test = True
		for ii in range(0,len(self.interaction)):
			if(self.interaction[ii].c.Nf[-1] <= 0):
				test = False
				break
		return test

	def view(self):
		"""
		Display kinetics of intensities/extensities for every interaction composing the hyphal
		"""
		for ii in range(0,len(self.interaction)):
			self.interaction[ii].view()
			# plt.title(str(ii))
#			plt.show()

	def data(self):
		"""
		Display kinetics of intensities/extensities for every interaction composing the hyphal
		"""

		tmax = len(self.interaction[-1].c.Nf)
		out = []
		for ii in range(0,len(self.interaction)):
			offset = tmax-len(self.interaction[ii].c.Nf)
			for jj in range(0,len(self.interaction[ii].c.Nf)):
				# print ii,jj
				#out.append([offset+jj,self.interaction[ii].c.Nf[jj],self.interaction[ii].c.Nv[jj],ii,"C",self.interaction[ii].c.func[jj]])
				# if ii == 3 :
					# pdb.set_trace()
				out.append([offset+jj,self.interaction[ii].c.Nf[jj],ii,"C",self.interaction[ii].c.func[jj]])
		out = np.array(out)
		df1 = pd.DataFrame(out, columns=["t","Nf","id","type","func"])#.to_csv("./save_cell.csv",sep=";")

		out = []
		for ii in range(0,len(self.interaction)):
			offset = tmax-len(self.interaction[ii].e.Nf)
			# if offset < 0 :
				# pdb.set_trace()
			for jj in range(0,len(self.interaction[ii].e.Nf)):
				out.append([offset+jj,self.interaction[ii].e.Nf[jj],ii,"E",self.interaction[ii].e.func[jj]])
		out = np.array(out)
		df2 = pd.DataFrame(out, columns=["t","Nf","id","type","func"])#.to_csv("./save_env.csv",sep=";")
		df1 = df1.append(df2)
		df1.to_csv("./save_83_46.csv",sep=";")

		# plt.plot(out[:,0],out[:,1])
		# plt.show()

	def get_length(self):
		return len(self.interaction)

	def get_N_front_necrose(self):
		N_front = 0
		N_necrose = 0
		for c in self.interaction:
			if c.c.func[-1].find("Margin"):
				N_front += 1
			else :
				N_necrose += 1
		return N_front,N_necrose

if __name__ == "__main__":
	h = hypha()
	if len(sys.argv)==0:
		E="75"
		C="90"
		dol = 1
	else:
		E=sys.argv[1]
		C=sys.argv[2]
		dol=int(sys.argv[3])
	c = cell("CC"+C)
	e = env("E"+E)
	# e.Nf[-1]=900
	i = interaction(c,e,dol)
	h.append(i)
	# Mother cell
	c = cell("CC"+C)
	e = env("E"+E)
#	c,e,K
	i = interaction(c,e,dol)
	h.append(i)
	out = "t\tL\n"
	for j in range(0,1000):
		# print j
		h.next()
		h.divide()
		out += str(j)+"\t"+str(len(h.interaction))+"\n"
		if h.cont() == False:
			break
#			continue
	# h.view()
	# h.data()
	print("./save_"+C+"_"+E+"_"+str(dol)+".txt")
	f=open("./save_"+C+"_"+E+"_"+str(dol)+".txt","w")
	f.write(out)
	f.close()
