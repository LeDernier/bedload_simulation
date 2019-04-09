
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

class frCrea: # Framework Creation
	#############################################################################################
	#############################################################################################
	@staticmethod
	def createPeriodicCell():
		# Defining the domain periodic
		O.periodic = True
		# Defining cell with good dimensions
		O.cell.hSize = Matrix3(
				pM.l, 0, 0,
				0, pM.w, 0,
				0, 0, pM.h
				)
	
	#############################################################################################
	#############################################################################################
	@staticmethod
	def createGround():
		# Creating ground at (0, 0, 0) with right length, width and orientation
		ground = box(center = (0.0, 0.0, pM.z_ground), extents = (1.0e5*pM.l, 1.0e5*pM.w, 0.0), fixed = True, wire = True, color = (0.,0.5,0.), material = 'mat') # Flat bottom plane 
		groundDisplay = box(center = (pM.l/2.0, pM.w/2.0, pM.z_ground), extents = (pM.l/2.0, pM.w/2.0, 0.0), fixed = True, wire = False, color = (0.,0.5,0.), material = 'mat', mask = -1) # Display of flat bottom plane
		O.bodies.append(ground)
		O.bodies.append(groundDisplay)
		return (len(O.bodies)-2, len(O.bodies)-1) 
	
	#############################################################################################
	#############################################################################################
	@staticmethod
	def createDisplayFluidHeight():
		display = box(center = (pM.l/2.0, pM.w/2.0, pF.z), extents = (pM.l/2.0, pM.w/2.0, 0.0), fixed = True, wire = False, color = (0.,0.5,0.), material = 'mat', mask = -1)
		O.bodies.append(display)
		return len(O.bodies)-1 
	
	#############################################################################################
	#############################################################################################
	@staticmethod
	def createDisplayG():
		display = box(center = (pM.l/2.0,pM.w/2.0,pM.h/1.5), extents = (pM.w/50.0, pM.w/50.0, pM.h/10.0), orientation = Quaternion((0, -1, 0), theta), fixed = True, wire = False, color = (0.5,0.,0.), material = 'mat', mask = -1)
		O.bodies.append(display)
		return len(O.bodies)-1 
	
	#############################################################################################
	#############################################################################################
	@staticmethod
	def createBox(**kwargs):
		# Parameters
		center =  kwargs.get('center', Vector3(0.0, 0.0, 0.0))
		extents = kwargs.get('extents', Vector3(0.0, 0.0, 0.0))
		orientation = kwargs.get('orientation', Quaternion(Vector3(0.0, 1.0, 0.0), 0.0))
		wire = kwargs.get('wire', False)
		color = kwargs.get('color', Vector3(1.0, 1.0, 1.0))
		mask = kwargs.get('mask', 1)
	
		# Creating ground at (0, 0, 0) with right length, width and orientation
		new_box = box(center = center, extents = extents, orientation = orientation, fixed = True, wire = wire, color = color, material = 'mat', mask = mask) # Flat bottom plane 
		O.bodies.append(new_box)
		return len(O.bodies) - 1 
	
	#############################################################################################
	#############################################################################################
	@staticmethod
	def createSphere(center, radius, color, wire, mask):
		# Creating ground at (0, 0, 0) with right length, width and orientation
		new_sphere = sphere(center = center, radius = radius, fixed = True, wire = wire, color = color, material = 'mat', mask = mask) # Flat bottom plane 
		O.bodies.append(new_sphere)
		return len(O.bodies) - 1 
	
	#############################################################################################
	#############################################################################################
	@staticmethod
	def createParticles():
		"""Creates a particules cloud in a box at the top of the channel.
		
		Parameters:
		- slopeChannel  -- slope of the channel.
		- diameterPart  -- diameter of the spheres
		- number        -- number of particles
		
		"""
	
		randRange = pP.r * 0.2
		d_eff = pP.d * 1.2
		r_eff = pP.r * 1.2
		n_i = len(O.bodies)
		n_max = n_i + pM.n

		# Create particles
		z = pM.z_ground + d_eff
		while z < pM.h-r_eff and len(O.bodies) < n_max:
			x = -pM.l/2.0 + r_eff
			while x < pM.l/2.0-r_eff and len(O.bodies) < n_max:
				y = -pM.w/2.0 + r_eff
				while y < pM.w/2.0-r_eff and len(O.bodies) < n_max:
					O.bodies.append(
							sphere(
								center = (
									x+random.randrange(-1,1)*randRange, 
									y+random.randrange(-1,1)*randRange, 
									z+random.randrange(-1,1)*randRange
									),
								radius = pP.r,
								color = (1.0, 1.0, 1.0),
								fixed = False,
								material = 'mat',
								wire = True
								)
							)
					y += d_eff
				x += d_eff
			z += d_eff
	
	#############################################################################################
	#############################################################################################
	@staticmethod
	def createRugosity():
		"""Creates a particules cloud in a box at the top of the channel.
		
		Parameters:
		- slopeChannel  -- slope of the channel.
		- diameterPart  -- diameter of the spheres
		- number        -- number of particles
		
		"""
	
		randRangeZ = pP.d
		randRangeXY = pP.r * 0.5
		d_eff =  pP.d * 0.8
	
		# Create particles
		z = pM.z_ground 
		x = -pM.l/2.0
		while x < pM.l/2.0:
			y = -pM.w/2.0
			while y < pM.w/2.0:
				O.bodies.append(
						sphere(
							center = (
								x + random.randrange(-1,1) * randRangeXY, 
								y + random.randrange(-1,1) * randRangeXY, 
								z + random.randrange(-1,1) * randRangeZ
								),
							radius = pP.r,
							color = (0.0, 0.3, 0.0),
							fixed = True,
							material = 'mat',
							wire = False
							)
						)
				y += d_eff
			x += d_eff
	
	#############################################################################################
	#############################################################################################
	@staticmethod
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
	
		# Sphere list
		ss = []
		# Create first sphere
		ss.append(
				sphere(
					center = (
						x, 
						y, 
						z
						),
					radius = random.randrange(r_min, r_max),
					color = (1.0, 0.0, 0.0),
					fixed = False,
					material = 'mat'
					)
				)
	
		for i in range(n):
			i_rand = random.randint(0, len(ss))
	
			theta = random.randrange(0.0, 2.0*math.pi)
			phi = random.randrange(0.0, math.pi)
			r_s = random.randrange(max(0.0, ss[i_rand].shape.radius - d_min), ss[i_rand].shape.radius)
			
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
						radius = random.randrange(r_min, r_max),
						color = (1.0, 0.0, 0.0),
						fixed = False,
						material = 'mat'
						)
					)
	
	#############################################################################################
	#############################################################################################
	@staticmethod
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
