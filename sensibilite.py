#!/usr/bin/python
import pdb
from hypha import *
import sys
"""
description
"""
__author__ =  'Adelin Barbacci _(;,;)_'
__version__=  '0.0'
__nonsense__ = 'sensibilite'

def create_hyph(icell,ienv,dol):
	status = "alive"
	h = hypha()

	# cell in necrosis
	c = cell("CC"+str(icell))
	e = env("E"+str(ienv))
	e.Nf[-1]=900
	#
	diff1 = c.D

	i = interaction(c,e,dol)
	h.append(i)

	c = cell("CC"+str(icell))
	e = env("E"+str(ienv))
	i = interaction(c,e,dol)
	h.append(i)

	for j in range(0,1000):
		h.next()
		h.divide()
		if h.cont() == False:
			status = "dead"
			break
#			continue
#	h.view()
#	h.data()
	# n_nec,n_front = h.get_N_front_necrose()

	return h.get_length(),status,diff1/0.5,dol,e.mu,h.ratio[-1]

if __name__ == "__main__":
	ind=0
	N = 100
	out = "h1\tstatus1\tcoop\tdol\tmu\tratio\n"
	for dol in [0,1]:
		for ii in range(0,N):
		 for jj in range(0,N):
			 ind += 1
			 h1,status1,coop,resistance,mu,ratio = create_hyph(ii,jj,dol)
			 sys.stdout.write("_(;,;)_ progress: %d / %d   \r" % (ind,2*N*N) )
			 sys.stdout.flush()
			 out+=str(h1)+"\t"+status1+"\t"+str(coop)+"\t"+str(dol)+"\t"+str(mu)+"\t"+str(ratio)+"\n"

	f = open("./sensi2.txt","w")
	f.write(out)
	f.close()
