
#########################################################################################################################################################################
# Author : Remi Monthiller, remi.monthiller@gmail.com
#
# Incline plane simulations
#
#########################################################################################################################################################################

import math
import random

from yade import pack

"""Call frameworkCreation to create the framework in your simulation. You will need to define the parameters in the frameworkCreation.py file.

"""
#############################################################################################
#############################################################################################

def createPeriodicSlope():
	# Defining the domain periodic
	O.periodic = True
	# Defining cell with good dimensions
	O.cell.hSize = Matrix3(
			l, 0, 0,
			0, w, 0,
			0, 0, h
			)
	# Creating ground at (0, 0, 0) with right length, width and orientation
	ground = box(center = (0.0, 0.0, h/3.0), extents = (1.0e5*l, 1.0e5*w, 0.0), fixed = True, wire = True, color = (0.,0.5,0.), material = 'mat') # Flat bottom plane 
	groundDisplay = box(center = (l/2.0, w/2.0, h/3.0), extents = (l/2.0, w/2.0, 0.0), fixed = True, wire = False, color = (0.,0.5,0.), material = 'mat', mask = -1) # Display of flat bottom plane
	O.bodies.append(ground)
	O.bodies.append(groundDisplay)

#############################################################################################
#############################################################################################

def createParticles():
	"""Creates a particules cloud in a box at the top of the channel.
	
	Parameters:
	- slopeChannel  -- slope of the channel.
	- diameterPart  -- diameter of the spheres
	- number        -- number of particles
	
	"""

	randRange = r * 0.2
	d_eff = d * 1.2
	r_eff = r * 1.2
	n_i = len(O.bodies)
	n_max = n_i + n

	# Create particles
	z =  h/3.0 + r_eff
	while z < h and len(O.bodies) < n_max:
		x = -l/2.0 + r_eff
		while x < l/2.0 and len(O.bodies) < n_max:
			y = -w/2.0 + r_eff
			while y < w/2.0 and len(O.bodies) < n_max:
				O.bodies.append(
						sphere(
							center = (
								x+random.random()*randRange, 
								y+random.random()*randRange, 
								z+random.random()*randRange
								),
							radius = r,
							color = (1.0, 1.0, 1.0),
							fixed = False,
							material = 'mat',
							wire = True
							)
						)
				y += d_eff
			x += d_eff
		z += d_eff

def addRandomClump(**kwargs):
	# Parameters
	center =  kwargs.get('center', Vector3(0.0, 0.0, 0.0))
	d_min = kwargs.get('d_min', 1.0e-6)
	d_max = kwargs.get('d_max', 1.0e-6)
	n = kwargs.get('n', 10)

	x = center[0]
	y = center[1]
	z = center[2]
	r_min = d_min/2.0
	r_max = d_max/2.0

	# Spher list
	ss = []
	# Create first sphere
	ss.append(
			sphere(
				center = (
					x, 
					y, 
					z
					),
				radius = random.random(r_min, r_max),
				color = (1.0, 0.0, 0.0),
				fixed = False,
				material = 'mat'
				)
			)


	for i in range(n):
		i_rand = random.randint(0, len(ss))

		theta = random.random(0.0, 2.0*math.pi)
		phi = random.random(0.0, math.pi)
		r_s = random.random(max(0.0, ss[i_rand].shape.radius - d_min), ss[i_rand].shape.radius)
		
		x = ss[i_rand].state.pos[0] + r_s * cos(theta) * sin(phi)
		y = ss[i_rand].state.pos[1] + r_s * sin(theta) * sin(phi)
		z = ss[i_rand].state.pos[2] + r_s * cos(phi)
		
		ss.append(
				sphere(
					center = (
						x, 
						y, 
						z
						),
					radius = random.random(r_min, r_max),
					color = (1.0, 0.0, 0.0),
					fixed = False,
					material = 'mat'
					)
				)



def addTetra(**kwargs):
	# Parameters
	center =  kwargs.get('center', Vector3(0.0, 0.0, 0.0))
	d_tetra = kwargs.get('d', 1.0e-6)
	l_tetra = kwargs.get('l', d_tetra)
	
	x = center[0]
	y = center[1]
	z = center[2]
	r_tetra = d_tetra/2.0
	
	s_1 = sphere(
			center = (
				x + l_tetra, 
				y, 
				z - l_tetra*sin(math.pi/6.0),
				),
			radius = r_tetra,
			color = (1.0, 0.0, 0.0),
			fixed = False,
			material = 'mat'
			) 
	s_2 = sphere(
			center = (
				x - l_tetra*sin(math.pi/6.0),
				y - l_tetra*cos(math.pi/6.0),
				z - l_tetra*sin(math.pi/6.0)
				),
			radius = r_tetra,
			color = (1.0, 0.0, 0.0),
			fixed = False,
			material = 'mat'
			)
	s_3 = sphere(
			center = (
				x - l_tetra*sin(math.pi/6.0),
				y + l_tetra*cos(math.pi/6.0),
				z - l_tetra*sin(math.pi/6.0)
				),
			radius = r_tetra,
			color = (1.0, 0.0, 0.0),
			fixed = False,
			material = 'mat'
			)
	s_4 = sphere(
			center = (
				x, 
				y, 
				z + l_tetra,
				),
			radius = r_tetra,
			color = (1.0, 0.0, 0.0),
			fixed = False,
			material = 'mat'
			)
	return O.bodies.appendClumped([s_1, s_2, s_3, s_4])
