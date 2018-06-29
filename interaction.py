#!/usr/bin/python
from cell import *
from env import *
import numpy as np
import pdb
import matplotlib.pyplot as plt

"""
This class describes interactions between fungus cell environment.
Feel free to use freely.
Citation of *Dow* would be apprecitate
"""
__author__ =  'Adelin Barbacci'
__team__ = 'QIP _(;,;)_'
__version__=  '0.0'
__nonsense__ = 'interaction'

def first(the_iterable, condition = lambda x: True):
	for i in the_iterable:
		if condition(i):
			return i

class interaction:
	def __init__(self,c,e,dol):
		self.c = c
		self.e = e
		self.cont = True
		self.DOL = dol

	def next_ext(self):
		# Results
		# hydrolysed by fungus
		if self.e.Nf[-1]<=self.e.Nf0:
			# Necrosis
			self.e.Nf.append(self.e.Nf[-1]-1)
			if self.DOL == 1:
				self.c.Nf.append(self.c.Nf[-1]+1-0.03*(self.c.Nf[-1]+1))
			else:
				self.c.Nf.append(self.c.Nf[-1]+1-0.03/self.e.mu*(self.c.Nf[-1]+1))
			self.c.func.append("Center")
			self.e.func.append("Necrosis")
		else:
			# Margin
			# pdb.set_trace()
			self.e.Nf.append(self.e.Nf[-1]-1)
			self.c.Nf.append(self.c.Nf[-1]+1-0.03/self.e.mu*(self.c.Nf[-1]+1))
			self.c.func.append("Margin")
			self.e.func.append("QDR")

		# If No Food anymore
		if self.e.Nf[-1]<=0:
			# print "No more food"
			self.e.Nf[-1] = 0
			self.e.func[-1]="Dead"

		self.continu()

	def continu(self):
		if(self.c.Nf[-1] <= 0):
			self.cont = False
			return self.cont

	def view(self):
		color1 = 'tab:red'
		color2 = 'tab:blue'
		fig,ax = plt.subplots(nrows=1, ncols=2, figsize=(14, 7))
		#FOOD
		ax[0].plot(self.c.Nf,'-',color='r')
		ax[0].set_title(self.c.func[-1]+ " Nf")

		ax[1].plot(self.e.Nf,'g-')
		ax[1].set_title("Env Nf")

		if np.min(self.e.Nf)<self.e.Nf0:
			ax[1].plot([0,len(self.e.Nf)],[self.e.Nf0,self.e.Nf0],'-m')
			xs = first(self.e.Nf,lambda i:i<self.e.Nf0)
			xs = self.e.Nf.index(xs)
			ax[1].plot([xs,xs],[0,np.max(self.e.Nf)],'--m')
			ax[0].plot([xs,xs],[0,np.max(self.c.Nf)],'--m')

		plt.show()
		return fig

if __name__ == "__main__":
	c = cell("CC9","C")
	e = env("E9")
	i = interaction(c,e,1)
	for ii in range(0,164):
		i.next_ext()
		print('ii = '+str(ii))
		if i.cont == False:
			print "break"
			break
	i.view()
