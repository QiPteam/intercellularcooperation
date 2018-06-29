#!/usr/bin/python
import numpy as np
import matplotlib.pyplot as plt
from xml.dom import minidom

"""
This class describes an environment which could be either an host or a culture medium

"""
__author__ =  'Adelin Barbacci _(;,;)_'
__version__=  '0.0'
__nonsense__ = 'env'

class env:
	def __init__(self,f):
		"""
		Initiation of a env object from a file f in ./env_data/
		 :Nf Quantity of energy at time t
		 :Nf0 threshold below which resistance vanishes
		 :mu ratio between center and periphery
		"""
		self.file = f
		# Energie in a ver of environment
		self.Nf = []
		# Energie flow toward pathogen / used to model level of resistence
		self.type = "E1"
		# Threshold for the switch toward necrosis
		self.Nf0 = 900
		# Verbose level
		self.v = 0
		self.mu = 0
		self.load()
		self.func = ["QDR"]

	def load(self):
		f = open("./env_data/"+str(self.file)+".txt","r")
		for l in f:
			l=l.replace("\n","")
			l=l.replace(" ","")
			if l.find("#")==-1:
				tab = l.split('=')
				if tab[0] == 'Nf':
					self.Nf.append(float(tab[1]))
				if tab[0] == 'mu':
					self.mu = float(tab[1])
		self.m_print("Env: Data loaded",1)
		f.close()

	def form(self):
		s = "-------------------------\n"
		s += self.type+"\n Energy level "+str(self.Nf[-1])+"\n Flux of energy necrosis"+str(self.dNf[0])+"\n Flux of energy margin"+str(self.dNf[1])+"\n Threshold "+str(self.Nf0)
		s += "\n-------------------------"
		return s

	def m_print(self,msg,v):
		if v <= self.v:
			print msg

if __name__=="__main__":
	e = env("E0")
	print e.form()
