#!/usr/bin/python
from numpy import linspace

N = 100
mu = linspace(0.01,0.99,N)
diff = linspace(0.,0.5,N)
ii = 0

#for inp_necy in inp_nec:
for muy in mu:
	out1 = "#Env T1\nNf=1000\nmu="+str(muy)
	f1 = open("./env_data/E"+str(ii)+".txt","w")
	f1.write(out1)
	f1.close()
	ii += 1
ii=0
for diffy in diff:
	out2 = "#Cell T1\nD="+str(diffy)
	f2 = open("./cell_data/CC"+str(ii)+".txt","w")
	f2.write(out2)
	f2.close()
	ii += 1
