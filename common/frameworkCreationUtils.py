
#########################################################################################################################################################################
# Author : Remi Monthiller, remi.monthiller@gmail.com
#
# Incline plane simulations
#
#########################################################################################################################################################################

import math
import random

from yade import pack
from yade.gridpfacet import *

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
		O.cell.setBox(pM.w, pM.w, pM.h)
	
	#############################################################################################
	#############################################################################################
	@staticmethod
	def createGround():
		# Creating ground at (0, 0, 0) with right length, width and orientation
		ground = box(center = (0.0, 0.0, pM.z_ground), extents = (1.0e5*pM.l, 1.0e5*pM.w, 0.0), fixed = True, wire = True, color = (0.,0.5,0.), material = 'mat') # Flat bottom plane 
		groundDisplay = box(center = (pM.l/2.0, pM.w/2.0, pM.z_ground), extents = (pM.l/2.0, pM.w/2.0, 0.0), fixed = True, wire = False, color = (0.,0.5,0.), material = 'mat', mask = 0) # Display of flat bottom plane
		O.bodies.append(ground)
		O.bodies.append(groundDisplay)
		return (len(O.bodies)-2, len(O.bodies)-1) 
	
	#############################################################################################
	#############################################################################################
	@staticmethod
	def createDisplayFluidHeight():
		display = box(center = (pM.l/2.0, pM.w/2.0, pF.z), extents = (pM.l/2.0, pM.w/2.0, 0.0), fixed = True, wire = False, color = (0.,0.,0.5), material = 'mat', mask = 0)
		O.bodies.append(display)
		return len(O.bodies)-1 
	
	#############################################################################################
	#############################################################################################
	@staticmethod
	def createDisplayG():
		display = box(center = (pM.l/2.0,pM.w/2.0,pF.z), extents = (pM.w/50.0, pM.w/50.0, pM.h/10.0), orientation = Quaternion((0, -1, 0), pM.alpha), fixed = True, wire = False, color = (0.5,0.,0.), material = 'mat', mask = 0)
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
		n_max = n_i + pP.n

		# Create particles
		z = pM.z_ground + d_eff + 2.0*randRange
		while len(O.bodies) < n_max:
			x = -pM.l/2.0 + r_eff
			while x < pM.l/2.0-r_eff and len(O.bodies) < n_max:
				y = -pM.w/2.0 + r_eff
				while y < pM.w/2.0-r_eff and len(O.bodies) < n_max:
					O.bodies.append(
							sphere(
								center = (
									x+random.uniform(-1,1)*randRange, 
									y+random.uniform(-1,1)*randRange, 
									z+random.uniform(-1,1)*randRange
									),
								radius = pP.r,
								color = (random.uniform(0.0, 0.5), random.uniform(0.0, 0.5), random.uniform(0.0, 0.5)),
								fixed = False,
								material = 'mat',
								wire = False
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
	
		randRangeZ = pP.d_rug/2.0
		randRangeXY = 0.0
		d_eff = pP.d_rug
	
		# Create particles
		z = pM.z_ground 
		x = -pM.l/2.0
		while x < pM.l/2.0:
			y = -pM.w/2.0
			while y < pM.w/2.0:
				O.bodies.append(
						sphere(
							center = (
								x + random.uniform(-1,1) * randRangeXY, 
								y + random.uniform(-1,1) * randRangeXY, 
								z + random.uniform(-1,1) * randRangeZ
								),
							radius = pP.d_rug/2.0,
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
	def createClumpCloud():
		"""Creates a particules cloud in a box at the top of the channel.
		
		Parameters:
		- slopeChannel  -- slope of the channel.
		- diameterPart  -- diameter of the spheres
		- number        -- number of particles
		
		"""
		
		d_eff = pS.d_tot 
		r_eff = pS.d_tot
		n_i = 0 

		# Create particles
		z = pM.z_ground + d_eff + d_eff/2.0
		while n_i < pP.n:
			x = -pM.l/2.0
			while x < pM.l/2.0 - d_eff/2.0 and n_i < pP.n:
				y = -pM.w/2.0
				while y < pM.w/2.0 - d_eff/2.0 and n_i < pP.n:
					(id_clump, ids_clumped) = frCrea.addClump(
							center = Vector3(x, y, z),
							ds = pS.ds,
							iter_vects = pS.iter_vect,
							)
					n_i += 1
					#d_eff = frCrea.computeOutD(id_clump, ids_clumped)
					y += d_eff
				x += d_eff
			z += d_eff
	
	#############################################################################################
	#############################################################################################
	@staticmethod
	def createCylinderCloud():
		"""Creates a particules cloud in a box at the top of the channel.
		
		Parameters:
		- slopeChannel  -- slope of the channel.
		- diameterPart  -- diameter of the spheres
		- number        -- number of particles
		
		"""
		
		d_eff = pS.d_tot 
		r_eff = pS.d_tot
		n_i = 0 

		# Create particles
		z = pM.z_ground + d_eff + d_eff/2.0
		while n_i < pP.n:
			x = -pM.l/2.0
			while x < pM.l/2.0 - d_eff/2.0 and n_i < pP.n:
				y = -pM.w/2.0
				while y < pM.w/2.0 - d_eff/2.0 and n_i < pP.n:
					(id_cyl, ids_nodes) = frCrea.addCylinder(
							center = Vector3(x, y, z),
							l = pS.d_tot,
							s = pS.d_max,
							)
					n_i += 1
					y += d_eff
				x += d_eff
			z += d_eff
	
	#############################################################################################
	#############################################################################################
	
	@staticmethod
	def addClump(**kwargs):
		# Parameters
		center =  kwargs.get('center', Vector3(0.0, 0.0, 0.0))
		ds = kwargs.get('ds', [1.0e-6])
		iter_vects = kwargs.get('iter_vects', [Vector3(ds[0], 0, 0)])

		# Sphere list
		ss = []
		col = (random.uniform(0.0, 0.5), random.uniform(0.0, 0.5), random.uniform(0.0, 0.5))
		d_tot = sum(ds)
		for iter_vect in iter_vects:
			pos = center - d_tot/2.0 * iter_vect 
			for d in ds:
				pos += d/2.0 * iter_vect
				ss.append(
						sphere(
							center = pos,
							radius = d/2.0, 
							color = col,
							fixed = False,
							material = 'mat'
							)
						)
				pos += d/2.0 * iter_vect
		# Adding clump to simulation
		result = O.bodies.appendClumped(ss)
		(id_clump, ids_clumped) = result

		# Random orientation
		O.bodies[id_clump].state.ori = Quaternion((0, 0, 1), random.uniform(0, 2 * math.pi)) * Quaternion((0, 1, 0), random.uniform(0, 2 * math.pi)) * Quaternion((1, 0, 0), random.uniform(0, 2 * math.pi))
		
		return result
	
	#############################################################################################
	#############################################################################################
	@staticmethod
	def addCylinder(**kwargs):
		# Parameters
		center =  kwargs.get('center', Vector3(0.0, 0.0, 0.0))
		l = kwargs.get('l', [1.0e-6])
		s = kwargs.get('s', l/4.0)

		# Sphere list
		col = (random.uniform(0.0, 0.5), random.uniform(0.0, 0.5), random.uniform(0.0, 0.5))
		nodesIds = []
		cylIds = []
		cylinder(center - Vector3((l-s)/2.0, 0.0, 0.0), center + Vector3((l-s)/2.0, 0.0, 0.0), radius=s/2.0, nodesIds=nodesIds, cylIds=cylIds, fixed=False, color=col, intMaterial='cMat', extMaterial='fMat')
		
		# Random orientation
		# c_body = O.bodies[id_clump].state.ori = Quaternion((0, 0, 1), random.uniform(0, 2 * math.pi)) * Quaternion((0, 1, 0), random.uniform(0, 2 * math.pi)) * Quaternion((1, 0, 0), random.uniform(0, 2 * math.pi))
		return (cylIds[0], nodesIds)

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
		rand_r = random.uniform(r_min, r_max)
		ss.append(
				sphere(
					center = (
						x, 
						y, 
						z
						),
					radius = rand_r, 
					color = (1.0, 0.0, 0.0),
					fixed = False,
					material = 'mat'
					)
				)
	
		for i in range(n):
			i_rand = random.randint(0, len(ss) - 1)

			theta = random.uniform(0.0, 2.0*math.pi)
			phi = random.uniform(0.0, math.pi)
			r_s = random.uniform(max(0.0, ss[i_rand].shape.radius - d_min), ss[i_rand].shape.radius)
			
			x = ss[i_rand].state.pos[0] + r_s * cos(theta) * sin(phi)
			y = ss[i_rand].state.pos[1] + r_s * sin(theta) * sin(phi)
			z = ss[i_rand].state.pos[2] + r_s * cos(phi)
			
			rand_r = random.uniform(r_min, r_max)
			ss.append(
					sphere(
						center = (
							x, 
							y, 
							z
							),
						radius = rand_r, 
						color = (1.0, 0.0, 0.0),
						fixed = False,
						material = 'mat'
						)
					)
		# Adding clump to simulation
		result = O.bodies.appendClumped(ss)
		(id_clump, ids_clumped) = result

		printParticleShapeInfo(id_clump, ids_clumped)
		
		return result

	@staticmethod
	def printParticleShapeInfo(id_clump, ids_clumped):
		# Debug prints after generation of random clump
		body_c = O.bodies[id_clump]
		print("Clump mass : " + str(body_c.state.mass))
		sum_mass = 0.0
		for b_id in ids_clumped:
			sum_mass += O.bodies[b_id].state.mass
		print("Sum mass : " + str(sum_mass))
		in_d = 0.0
		for b_ids in ids_clumped:
			in_d = max(in_d, O.bodies[b_id].shape.radius)
		in_d *= 2.0
		print("In d : " + str(in_d))
		out_d = frCrea.computeOutD(id_clump, ids_clumped)
		print("Out d : " + str(out_d))
		print("Ratio in_d/out_d : " + str(in_d/out_d))


	#############################################################################################
	#############################################################################################
	@staticmethod
	def computeOutD(id_clump, ids_clumped):
		out_d = 0
		for i in range(len(ids_clumped) - 1):
			b_id = ids_clumped[i]
			b = O.bodies[b_id]
			for j in range(i+1, len(ids_clumped)):
				test_id = ids_clumped[j]
				t = O.bodies[test_id]
				test_d = ((t.state.pos - b.state.pos).norm() + t.shape.radius + b.shape.radius)
				if test_d > out_d:
					out_d = test_d
		return out_d
	
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
