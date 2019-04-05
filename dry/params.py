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

	"""

import math

### Simulation parameters
t_max = 100.0

### Macroscopic parameters
n = 1000.0
theta = 0.14 * math.pi
l = 1.0e-1
w = 0.5e-1
h = 3.0e-1
z_ground = h/3.0

### Physical parameters
g = Vector3(9.81 * sin(theta), 0, -9.81 * cos(theta))

### Shape
d_tetra = 2e-3
### Particles
d = 1.7*d_tetra
rho_p = 2.5e3
c_r = 0.7
phi_max = 0.61
mu = atan(0.5)
### Fluid
rho_f = 0.0

### Useful deducted parameters
## Recomputed
n = 2e-4/pow(d, 3.0)
## Computation of the radius
r = d / 2.0
## Estimated number of particles layer
n_l = n / (l * w / (d * d))
## Estimated number of initial particles layer
n_ll = n / (l * w / (1.2 * d * 1.2 * d))

# Save interval
saveInterval = 1.0
