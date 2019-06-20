"""This is the default parameter file. Do not change this file.

This file is used for convinience and backward compatibility.

Copy this file in your working directory and rename it "params.py" if you
want to use it.

You can still place execfile("../common/default_params.py") on the top of 
your "params.py" if you want to set all of your parameters to default ones 
before changing them so that you do not need to define them all.

"""

# execfile("../common/defaultParams.py")

import math

### Numerical Parameters
class pN:
	### Time of the simulation 
	t_max = 400.0
	### Number of cells of the mesh
	n_z = 900
	### Verbose
	verbose = True

### Particle Parameters
class pP: 
	### Shape and length parameters of the particles
	# Type : "clump" or "cylinder"
	kind = "clump"
	# Characteristic lengh taken for the adimensionalisation within the shields number.
	dvs = 6.0e-3 
	# Shape factor 
	A = 3.0
	# Small characteristic length 
	S = (2.0 * pow(A - 1.0, 2) + 4.0)/(pow(A - 1.0, 3) + 4.0) * dvs
	# Long Characteristic length
	L = A * S
	# Volume and frontale surface that will be computed differently depending on the kind 
	vol = 0
	surf = 0
	### Clump parameters
	if kind == "clump":
		# Diameter of the small spheres
		dss = (L-S)/2.0
		# List of the diameters of the spheres in the clump
		ds = []
		if dss > 0.0:
			ds = [dss, S, dss]
		else:
			ds = [S]
		# Computation of the volume and the surface of the particles
		for d in ds:
			vol += math.pi * pow(d, 3) / 6.0
			surf += math.pi * pow(d, 2) / 4.0
	# Verification
	dvs_calc = 3.0/2.0 * vol/surf
	### Cylinder parameters
	# TODO
	### Density of particles
	rho = 2.5e3
	### Coefficient of restitution
	c_r = 0.5
	### Maximum volume fraction (value set after some simulations) 
	phi_max = 0.61
	### Friction angle
	mu = math.atan(0.5)
	### Initial particle velocity and volume fraction that are given to the HydroEngine
	v = [Vector3(0,0,0)] * (pN.n_z - 1)
	phi = [0] * (pN.n_z - 1)

### Macroscopic Parameters
class pM: 
	### Sediment height
	hs = 10.0 * pP.dvs
	### Framework parameters
	alpha = 0.05 
	l = 30 * pP.dvs
	w = 30 * pP.dvs
	h = 200.0 * pP.dvs
	z_ground = h/2.0
	### Number of Particles
	n = pP.phi_max * l * w * hs / pP.vol
	# Number of particles "layers"
	n_l = n / (pP.phi_max * l * w * pP.S / pP.vol)
	### Gravity parameters
	g_scale = 9.81
	g = Vector3(g_scale * math.sin(alpha), 0, -g_scale * math.cos(alpha))
	### Ground Rugosity
	d_rug = pP.S
	### Shake
	shake_enable = True
	shake_f = 20.0
	shake_dt = 0.05/shake_f
	shake_a = pP.dvs/2.0
	shake_time = 0.6

### Param Save
class pSave:
	# Data will be saved all "yadeSavePeriod" simulation (virtual) time. Disable saving by setting it to 0.
	yadeSavePeriod = 2.0
	# Data will be saved as vtk (for Paraview for example) all "vtkRecorderIterPeriod" iterations. Disable saving by setting it to 0.
	vtkRecorderIterPeriod = 0

### Param Fluid
class pF: 
	enable = True
	solve = True
	# Can be "old" or "new"
	method = "new"
	solve_begin_time = 0.8
	## Physics
	rho = 1e3
	nu = 1e-6
	init_shields = 1.5
	shields_d = pP.dvs
	h = 0.0
	if pM.alpha != 0 and enable and rho != 0:
		h = init_shields * (pP.rho/rho - 1) * shields_d / math.sin(pM.alpha)
	dt = 1e-5
	t = 1e-2
	## Fluid mesh
	# Richardson Zaki exponent for the hindrance function of the drag force applied to the particles ???
	expoDrag = 3.1
	# Computed parameters
	z = pM.hs + h + pM.z_ground
	dz = (z-pM.z_ground)/float(pN.n_z-1)
	# Attributes of the fluid
	vx = [0] * (pN.n_z+1)
	# Display parameters
	display_enable = False
	display_n = 100
	display_mult = 0
	# Mostly useless parameters
	enable_wall_friction = False
	enable_fluctuations = False
	t_fluct = 1e-1

if pN.verbose:
	print("\n")

	print("INFO: Particle volume : " +  str(pP.vol))
	print("INFO: Particle surface : " +  str(pP.surf))
	print("INFO: dvs:" + str(pP.dvs) + " dvs_calc:" + str(pP.dvs_calc))
	print("INFO: Diameter of the spheres: " + str(pP.ds))

	print("INFO: Number of particles : " + str(pM.n))
	print("INFO: Estimated number of particle layers : " + str(pM.n_l))
	
	
	if pF.enable:
		print("INFO: Estimated fluid height : " + str(pF.h))

	print("\n")
