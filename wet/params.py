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
	t_max = 100.0
	
	### Macroscopic parameters
	n = 1000.0
	theta = 0.14 * math.pi
	l = 1.0e-1
	w = 0.5e-1
	h = 3.0e-1
	z_ground = h/3.0
	# Computed parameters
	n_l = 0
	n_ll = 0
	
	### Physical parameters
	g = Vector3(9.81 * sin(theta), 0, -9.81 * cos(theta))

class pSave: # Param Save
	yadeSavePeriod = 1.0

### Shape
class pS: # Param Shape
	d_tetra = 2e-3

### Particles
class pP: # Param Particle
	d = 1.7*pS.d_tetra
	rho = 2.5e3
	c_r = 0.7
	phi_max = 0.61
	mu = atan(0.5)
	# Computed
	r = d/2.0

### Fluid
class pF: # Param Fluid
	enable = False
	## Physics
	rho = 1e-3
	nu = 1e-6
	h = 0.1
	dt = 1e-5
	t = 1e-2
	## Fluid mesh
	n_z = 900
	# Richardson Zaki exponent for the hindrance function of the drag force applied to the particles ???
	expoDrag = 3.1
	# Computed parameters
	z = pM.n_l * pP.d + pM.h
	dz = z/float(n_z)

### Useful deducted parameters
## Recomputed
pM.n = 4e-4/pow(pP.d, 3.0)
## Estimated number of particles layer
pM.n_l = pM.n / (pM.l * pM.w / (pP.d * pP.d))
## Estimated number of initial particles layer
pM.n_ll = pM.n / (pM.l * pM.w / (1.2 * pP.d * 1.2 * pP.d))
