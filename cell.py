#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt

"""
This class describes a fungus cell.
"""

__author__ =  'Adelin Barbacci _(;,;)_'
__version__=  '0.0'
__nonsense__ = 'cell'

class cell:

	def __init__(self,f):
		"""
		Initiation of a cell object from a file f in ./cell_data/
		 :Nf0 Initial quantity of energy
		 :Nf Quantity of energy at time t
		 :Met energy cost of metabolismes
		"""
		self.file = f
		# Uptake from host
		self.Nf = [0]
		self.dNf = 1
		### Diffusion coefficients
		self.D = 0.0
		### Coop or not
		### function of the cell front / necrose
		self.func = ["Margin"]
		### Threshold of cell division
		self.div_thres = 10
		### Verbose level
		self.v = 0
		self.load()



	def load(self):
		f = open("./cell_data/"+str(self.file)+".txt","r")
		for l in f:
			l=l.replace("\n","")
			l=l.replace(" ","")
			if l.find('#') == -1:
				tab = l.split('=')
				if tab[0] == 'D':
					self.D = float(tab[1])

		self.m_print("Cell: Data loaded",1)
		f.close()


	def form(self):
		"""
		Method to write formated cell data
		"""
		s = "-------------------------\n"
		s += self.type+"\n Energy level "+str(self.Nf[-1])+"\n Metabolic cost necrosis"+str(self.Met[0])+"\n Metabolic cost front"+str(self.Met[1])+"\n Diffusion cell-cell "+str(self.D)+"\n Division threshold "+str(self.div_thres)
		s += "\n-------------------------"
		return s

	def m_print(self,msg,v):
		"""
		Verbose level of the class
		"""
		if v <= self.v:
			print msg

if __name__=="__main__":
	c = cell("CC0","1")
	print c.form()
	import doctest
	doctest.testmod()
