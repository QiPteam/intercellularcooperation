#!/usr/bin/python
import vtk
import pandas as pd
import pdb
import numpy as np

"""
description
"""
__author__ =  'Adelin Barbacci _(;,;)_'
__version__=  '0.0'
__nonsense__ = 'hyphae'

# create a renderwindowinteractor
class visu3d:
	def __init__(self):
		self.I = 0
		self.ren = vtk.vtkRenderer()
		cam = self.ren.GetActiveCamera()
#		cam.SetPosition(0.5,0.5,0.5);
		cam.SetFocalPoint(0,0,0);
		cam.Azimuth(-70)
#		cam.Zoom(0.1)
		self.ren.SetBackground(0.8,0.8,0.8)
		self.renWin = vtk.vtkRenderWindow()
		self.renWin.AddRenderer(self.ren)
		self.renWin.SetSize(400,1000)
		self.iren = vtk.vtkRenderWindowInteractor()
		self.iren.SetRenderWindow(self.renWin)
		self.L = 0.1
		self.data = self.get_data()


	def re_init(self):
		self.ren = vtk.vtkRenderer()
		self.ren.SetBackground(0.8,0.8,0.8)
		self.renWin = vtk.vtkRenderWindow()
		self.renWin.AddRenderer(self.ren)
		self.iren = vtk.vtkRenderWindowInteractor()
		self.iren.SetRenderWindow(self.renWin)
		self.L = 0.1

	def get_data(self):
		df = pd.read_csv('save.csv',sep=";")
		return df

	def get_colour(self,val,typ,mini,maxi,scale,kind):
		if kind == "numeric":
			if mini < 0 :
				print "valeur inf"
			if mini != maxi:
				length = np.log(maxi)-np.log(mini)
			else :
				mini = val-1
				length = 1
			if val>0:
				if scale == "red":
					if typ == 1:
						return [float((np.log(val)-np.log(mini))/length),0,0]
				if scale == "green":
					if typ == 1:
						return [0.84,0.36,0.15]
					if typ == 2:
						return [0.0,float((np.log(val)-np.log(mini))/length),float(0)]
				if scale == "blue":
					if typ == 1:
						return [0,0,float((np.log(val)-np.log(mini))/length)]
				if scale == "yellow":
					if typ == 1:
						return [1,1,0.0]
#						return [1,float((val-mini)/length),0.0]
			if val <= 0:
				if scale == "green" :
					return [0.84,0.36,0.15]
				if scale == "yellow" :
					return [0.84,0.36,0.15]
				else:
					return [1,0,1]
		if kind == "factor":
			if scale == "red" :
				if val == "Front":
					return [1,0,0]
				else :
					return [0,0,0]
			if scale == "green":
				if val == "QDR":
					return [0,1,0]
				else :
					return [0,0,1]

	def create_sphere(self,ii,t,offset):
#		pas = 3*self.L
		pas = 0
		sphere = vtk.vtkSphereSource()
		sphere.SetThetaResolution(100)
		sphere.SetPhiResolution(100)
		sphere.SetCenter(pas*t,self.L*(ii+offset),0)
		sphere.SetRadius(self.L)

		return sphere

	def create_cylinder(self,ii,t,offset):
#		pas = 3*self.L
		pas = 0
		cylinder = vtk.vtkCylinderSource()
		cylinder.SetCenter(pas*t,self.L*(ii+offset),0)
		cylinder.SetRadius(self.L)
		cylinder.SetHeight(self.L)
		cylinder.SetResolution(100)
		return cylinder

	def create_cube(self,ii,t,offset,loc):
#		pas = 3*self.L
		pas = 0
		cube = vtk.vtkCubeSource()
#		[
		if loc == "left":
			cube.SetBounds([pas*t,1.3*self.L+pas*t,-self.L/2+(ii+offset)*self.L,self.L/2+(ii+offset)*self.L,-2*self.L,-self.L])
		if loc == "right":
			cube.SetBounds([-1.3*self.L+pas*t,pas*t,-self.L/2+(ii+offset)*self.L,self.L/2+(ii+offset)*self.L,-2*self.L,-self.L])
		if loc == "both":
			cube.SetBounds([-1.3*self.L+pas*t,1.3*self.L+pas*t,-self.L/2+(ii+offset)*self.L,self.L/2+(ii+offset)*self.L,-2*self.L,-self.L])
		return cube

	def find_function(self,tmp):
		tab1 = tmp[tmp["type"]=="C"]
		tab2 = tmp[tmp["type"]=="E"]
		tab1.is_copy = False
		tab2.is_copy = False
		for ii in range(0,len(tab1)):
			if tab2["Nv"].values[ii]<=0 :
				tab1.loc[ii,"func"] = "Front"
				tab2.loc[ii,"func"] = "QDR"
			else :
				tab1.loc[ii,"func"] = "Necrose"
				tab2.loc[ii,"func"] = "NO"
		return pd.concat([tab1,tab2])

	def create_scene(self):
		to_visu = 'Nf'
		mini1 = self.data[to_visu][self.data['type']=="C"].min(axis=0)
		maxi1 = self.data[to_visu][self.data['type']=="C"].max(axis=0)
		mini2 = self.data[to_visu][self.data['type']=="E"].min(axis=0)
		maxi2 = self.data[to_visu][self.data['type']=="E"].max(axis=0)
		for t in range(0,self.data['t'].max(axis=0)):
			# create source
			tmp = self.find_function(self.data[self.data['t']==t])
			ii_cyl  = 0
			ii_cube = 0
			ii_cube_env = 0
#			pdb.set_trace()
			for row in tmp.iterrows():
				offset = 0
				if  row[1]['type'] == "C":
					apex = tmp[tmp['type']=="C"]["id"].max(axis=0)
#					pdb.set_trace()
					if row[1]['id']==apex:
						obj = self.create_sphere(ii_cyl,t,offset)
						if (to_visu == 'Nv') | (to_visu == 'Nf'):
							color = self.get_colour(row[1][to_visu],1,mini1,maxi1,"red","numeric")
						if to_visu == 'func':
							color = self.get_colour(row[1][to_visu],1,mini1,maxi1,"red","factor")
					else:
						obj = self.create_cylinder(ii_cyl,t,offset)
						if (to_visu == 'Nv') | (to_visu == 'Nf'):
							color = self.get_colour(row[1][to_visu],1,mini1,maxi1,"red","numeric")
						if to_visu == 'func':
							color = self.get_colour(row[1][to_visu],1,mini1,maxi1,"red","factor")
#						pdb.set_trace()
					ii_cyl += 1
				if  row[1]['type'] == "E":
					obj     = self.create_cube(ii_cube,t,offset,"both")
					if (to_visu == 'Nv') | (to_visu == 'Nf'):
						color = self.get_colour(row[1][to_visu],1,mini2,maxi2,"green","numeric")
					if to_visu == 'func':
						color = self.get_colour(row[1][to_visu],1,mini2,maxi2,"green","factor")
					ii_cube += 1

#
#				# mapper
				mapper1 = vtk.vtkPolyDataMapper()
				mapper1.SetInput(obj.GetOutput())
#				# actor

				actor1 = vtk.vtkActor()
				actor1.SetMapper(mapper1)
				actor1.GetProperty().SetColor(color)
#				actor1.GetProperty().SetOpacity(0.99)
#				# assign actor to the renderer
				self.ren.AddActor(actor1)

			self.render()
			#self.save_image()


#			self.re_init()

	def save_image(self):
		path = "./save_image/j6/"
		windowToImageFilter = vtk.vtkWindowToImageFilter()
		windowToImageFilter.SetInput(self.renWin)
		windowToImageFilter.SetInputBufferTypeToRGBA()
		windowToImageFilter.ReadFrontBufferOff()
		windowToImageFilter.Update()
		writer = vtk.vtkPNGWriter()
		writer.SetInputConnection(windowToImageFilter.GetOutputPort())
		writer.SetFileName(path+"test_"+str(self.I)+".png")
		writer.Write()
		self.I += 1

	def render(self):
		self.renWin.Render()
		# enable user interface interactor
		self.iren.Initialize()


		self.ren.ResetCamera();

#		renderWindowInteractor = vtk.vtkRenderWindowInteractor()
#		renderWindowInteractor.SetRenderWindow(self.renWin)
#		renderWindowInteractor.Initialize()
		# Sign up to receive TimerEvent
#		cb = vtkTimerCallback()
#		cb.actor = actor
#		renderWindowInteractor.AddObserver('TimerEvent', cb.execute)
#		timerId = renderWindowInteractor.CreateRepeatingTimer(33);

		#start the interaction and timer
#		renderWindowInteractor.Start()
		self.iren.Start()

if __name__ == "__main__":

	v1 = visu3d()
	v1.create_scene()
#	v1.render()
