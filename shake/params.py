"""Enter the parameters of the simulation in this file.
	
	Parameters:
	--- Simulation parameters
	- t_max		-- simulation time				-- s		-- 30.0
	--- Macroscopic parameters
	- n			-- number of particles			-- .		-- 10
	- theta		-- slope angle					-- rad		-- 1.5
	- l			-- length of the cell			-- m		-- 1.0
	- w			-- width of the cell			-- m		-- 1.0
	- h			-- heigth of the cell			-- m		-- 1.0
	--- Particles :
	- d			-- diameter of the particles	-- m		-- 6e-3
	- rho_p		-- density of the particles		-- kg/m^3	-- 2.5e3
	- c_r		-- restitution coefficient		-- .		-- 0.7
	- phi_max	-- maximum volume fration		-- .		-- 0.61
	- mu		-- particles' friction angla	-- rad		-- atan(0.5)
	--- Fluid :
	- rho_f		-- density of the fluid			-- kg/m^3	-- 1.0e3
	- nu_f		-- kinematic viscosity			-- m^2/s	-- 1e-6
	- h_f		-- fluid height (above bed)		-- m		-- 0.1
	- dt_f		-- fluid time step				-- s		-- 1e-5
	- t_f		-- time between two resolutions	-- s		-- 1e-2
	-- Define fluid mesh:
	- n_z		-- number of cells (1D)			-- .		-- 900

	"""

import math

class pM: # Param Macro
	### Simulation parameters
	t_max = 10.0
	# Mesh :
	n_z = 900
	### Macroscopic parameters
	alpha = 0.0 
	l = 1.0e-1
	w = 1.0e-1
	h = 20.0e-1
	z_ground = h/2.0
	### Physical parameters
	g_scale = 9.81
	g = Vector3(g_scale * sin(alpha), 0, -g_scale * cos(alpha))
	### Shake
	shake_enable = True
	shake_period = 0.04
	shake_intensity = 0.2
	shake_time = 9.0

class pSave: # Param Save
	yadeSavePeriod = 0.5
	vtkRecorderIterPeriod = 0

### Particles
class pP: # Param Particle
	d = pM.l/10.0
	rho = 2.5e3
	c_r = 0.7
	phi_max = 0.4 #0.64
	mu = atan(0.5)
	# Ground rugosity
	d_rug = d
	# Computed
	r = d/2.0
	n = 0
	# Will be computed after
	n_l = 0
	# Attributes of the particles:w
	vx = [0] * (pM.n_z-1)
	phi = [0] * (pM.n_z-1)

### Shape
class pS: # Param Shape
	A = 0.334
	d_min_star = pP.d * ((1.0/A) - 1.0) / 2.0
	ds = [d_min_star, pP.d, d_min_star] 
	iter_vect = [Vector3(1.0, 0.0, 0.0)]
	# Computation of parameters
	# d_tot = sum(ds)
	# ds = [d * pP.d / d_tot for d in ds]
	d_tot = sum(ds)
	d_min = min(ds)
	d_max = max(ds)
	vol = 0
	surf = 0
	for d in ds:
		vol += math.pi * pow(d, 3) / 6.0
		surf += math.pi * pow(d, 2) / 4.0
	d_vol = pow(6.0 * vol / math.pi, 1.0/3.0)
	d_surf = pow(4.0 * surf / math.pi, 1.0/2.0)


# Computing n_l and n_ll
pP.n = 12.0 * (pP.phi_max * pM.l * pM.w * pS.d_max / pS.vol)
pP.n_l = pP.n / (pP.phi_max * pM.l * pM.w * pS.d_max / pS.vol)
print("Number of particles : " + str(pP.n))
print("Estimated number of particle layers : " + str(pP.n_l))

### Fluid
class pF: # Param Fluid
	enable = False
	solve = False
	solve_begin_time = 0.8
	## Physics
	rho = 1e3
	nu = 1e-6
	init_shields = 0.2
	shields = 0.0 # Will be updated during the simulation. max(hydroEngine.ReynoldStresses)/((densPart-densFluidPY)*diameterPart*abs(gravityVector[2]))
	shields_d = pS.d_max
	if pM.alpha != 0.0:
		h = init_shields * (pP.rho/rho - 1) * shields_d / sin(pM.alpha)
	else:
		h = 0.0
	print("Estimated fluid height : " + str(h))
	dt = 1e-5
	t = 1e-2
	## Fluid mesh
	# Richardson Zaki exponent for the hindrance function of the drag force applied to the particles ???
	expoDrag = 3.1
	# Computed parameters
	z = pP.n_l * pS.d_max + h + pM.z_ground
	dz = (z-pM.z_ground)/float(pM.n_z-1)
	# Attributes of the fluid
	vx = [0] * (pM.n_z+1)
	# Display parameters
	display_enable = False
	display_n = 100
	display_mult = 0
