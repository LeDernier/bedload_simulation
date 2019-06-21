
#########################################################################################################################################################################
# Author : Remi Monthiller, remi.monthiller@etu.enseeiht.fr
# Adapted from the code of Raphael Maurin, raphael.maurin@imft.fr
# 30/10/2018
#
# Incline plane simulations
#
#########################################################################################################################################################################

import numpy as np

#############################################################################################
#############################################################################################
           
def getMeanPos():
	"""Returns the current mean position value of the dynamic objects as a Vector3
	
	"""
	vect = Vector3(0,0,0)
	n=0.0
	for body in O.bodies :
		if body.dynamic == True and not body.isClump:
			vect += body.state.pos
			n+=1.0
	vect /= n
	return vect

#############################################################################################
#############################################################################################

def getMeanVel():
	"""Returns the current mean velocity value of the dynamic objects as a Vector3
	
	"""
	vect = Vector3(0,0,0)
	n=0.0
	for body in O.bodies :
		if body.dynamic == True and not body.isClump:
			vect += body.state.vel
			n+=1.0
	vect /= n
	return vect

#############################################################################################
#############################################################################################

def getShields():
	"""Returns the current shields number.
	
	"""
	if pF.enable:
		return max(hydroEngine.ReynoldStresses)/((pP.rho-pF.rho) * eval(pPP.d_ad) * abs(pM.g[2])) # pF.shields_d * abs(pM.g[2]))
	else:
		return 0

#############################################################################################
#############################################################################################

def getEulerHist():
	rotx = []
	roty = []
	rotz = []
	for body in O.bodies :
		if body.dynamic == True and body.isClump:
			rot = body.state.rot()
			#rotx.append(rot[0])
			roty.append(rot[1] + 0.375 * pi)
			rotz.append(rot[2] - 0.25 * pi)
			#rotz.append(math.fmod(2*math.pi + rot[2], 2*math.pi))
	binsNb = 20
	rots, y, z = np.histogram2d(roty, rotz, bins=binsNb, normed=False)
	return [rots, y, z]

#############################################################################################
#############################################################################################

def getOrientationHist(binsNb=3, vMin=0.0):
	rotx = []
	roty = []
	rotz = []
	for body in O.bodies :
		if body.dynamic == True and body.isClump and body.state.vel.norm() > vMin:
			u = (O.bodies[body.id - 1].state.pos - O.bodies[body.id - 3].state.pos).normalized()
			if u.dot(Vector3(1.0, 0.0, 0.0)) < 0.0:
				u = -u
			#if u[1] > 0.0:
			#	u[1] = -u[1]
			rotx.append(u[0])
			roty.append(u[1])
			rotz.append(u[2])
	rots, [x, y, z] = np.histogramdd((rotx, roty, rotz), bins=binsNb, normed=False)
	return [rots, x, y, z]

#############################################################################################
#############################################################################################

def getMeanOrientation(vMin=0.0):
	xs = []
	ys = []
	zs = []
	for body in O.bodies :
		if body.dynamic == True and body.isClump and body.state.vel.norm() > vMin:
			u = (O.bodies[body.id - 1].state.pos - O.bodies[body.id - 3].state.pos).normalized()
			if u.dot(Vector3(1.0, 0.0, 0.0)) < 0.0:
				u = -u
			if u[1] > 0.0:
				u[1] = -u[1]
			xs.append(u[0])
			ys.append(u[1])
			zs.append(u[2])
	xs = np.array(xs)
	ys = np.array(ys)
	zs = np.array(zs)
	u_mean = Vector3(xs.mean(), ys.mean(), zs.mean())
	u_var = Vector3(sqrt(xs.var()), sqrt(ys.var()), sqrt(zs.var()))
	return [u_mean, u_var]

#############################################################################################
#############################################################################################

def getOldProfiles():
	dz = h/float(n_z)
	zs = [dz * i for i in range(n_z)]
	phi = [0 for i in range(n_z)]
	vpx = [0 for i in range(n_z)]
	for body in O.bodies :
		if body.dynamic == True and not body.isClump:
			z = body.state.pos[2]
			r = body.shape.radius
			z_min = z - r
			z_max = z + r
			n_min = int(z_min*n_z/h)
			n_max = int(z_max*n_z/h)
			vel = body.state.vel
			for i in range(n_min, n_max+1):
				z_inf = max(zs[i], z_min) - z
				z_sup = min(zs[i+1], z_max) - z
				vol = math.pi * pow(r, 2) * ((z_sup - z_inf) + (pow(z_inf,3) - pow(z_sup, 3))/(3*pow(r, 2)))
				phi[i] += vol
				vpx[i] += vol * vel[0]
	for i in range(n_z):
		if(phi[i] > 0):
			vpx[i] /= phi[i]
			phi[i] /= dz * l * w
	return [zs, phi, vpx] 

#############################################################################################
#############################################################################################

def getProfiles():
	"""Returns the current mean velocity value of the dynamic objects as a Vector3
	
	"""
	if(pF.enable):
		vxPart = []
		if pF.method == "new":
			for i in range(0, len(hydroEngine.vPart)):
				vxPart.append(hydroEngine.vPart[i][0])
		elif pF.method == "old":
			for i in range(0, len(hydroEngine.vxPart)):
				vxPart.append(hydroEngine.vxPart[i])
		return [[i * pF.dz for i in range(pN.n_z)], hydroEngine.phiPart, vxPart, hydroEngine.vxFluid[0:-1]]
	else:
		partsIds = []
		for i in range(len(O.bodies)):
			b = O.bodies[i]
			if not b.isClump:
				partsIds.append(i)
		hydroEngineTmp = HydroForceEngine(
				densFluid = pF.rho, viscoDyn = pF.nu * pF.rho, zRef = pM.z_ground, 
				gravity = pM.g, deltaZ = pF.dz, expoRZ = pF.expoDrag, 
				lift = False, nCell = pN.n_z, vCell = pM.l * pM.w * pF.dz, 
				phiPart = pP.phi, vxFluid = pF.vx, vPart = pP.v, 
				ids = partsIds, label = 'hydroEngine', dead = True)
		hydroEngineTmp.ReynoldStresses = np.ones(pN.n_z) * 0.0
		hydroEngineTmp.turbulentFluctuation()
		hydroEngineTmp.newAverageProfile()
		vxPart = []
		for v in hydroEngineTmp.vPart:
			vxPart.append(v[0])
		return [[i * pF.dz for i in range(pN.n_z)], hydroEngineTmp.phiPart, vxPart, hydroEngineTmp.vxFluid[0:-1]]

#############################################################################################
#############################################################################################

def getInertialProfile():
	"""Returns the current mean velocity value of the dynamic objects as a Vector3
	
	"""
	if(pF.enable):
		# Computation of \dot{\gamma}
		## Starting with vxPart
		vxPart = []
		for i in range(0, len(hydroEngine.vPart)):
			vxPart.append(hydroEngine.vPart[i][0])
		gamma_dot = []
		for i in range(0, len(vxPart)):
			gamma_dot.append((vxPart[i+1][0] - vxPart[i][0])/2.0)
		# Computation of the Granular Pressure : 
		# P_p = (\rho_p - \rho_f) * g * d_{vs} * \int{\phi dz}_z^\inf
		pressure = [0] * len(hydroEngine.phiPart)
		integ = 0
		for i in range(len(hydroEngine.phiPart) - 1, -1, -1):
			integ += hydroEngine.phiPart[i] * pF.dz
			pressure[i] = (pP.rho - pF.rho) * pM.g[2] * pP.dvs * integ
		# Finishing by computing the inertial number profile
		# I = \frac{\dot{\gamma} d}{\sqrt{\frac{P}{\rho_p}}}
		inertial = []
		for i in range(0, len(pressure)):
			inertial.append(gamma_dot[i] * dvs / sqrt(pressure / pP.rho))
		return [[i * pF.dz for i in range(pN.n_z)], inertial]
	else:
		partsIds = []
		for i in range(len(O.bodies)):
			b = O.bodies[i]
			if not b.isClump:
				partsIds.append(i)
		hydroEngineTmp = HydroForceEngine(
				densFluid = pF.rho, viscoDyn = pF.nu * pF.rho, zRef = pM.z_ground, 
				gravity = pM.g, deltaZ = pF.dz, expoRZ = pF.expoDrag, 
				lift = False, nCell = pM.n_z, vCell = pM.l * pM.w * pF.dz, 
				radiusPart= pP.r, phiPart = pP.phi, vxFluid = pF.vx, 
				vPart = pP.v, ids = partsIds, label = 'hydroEngine', dead = True)
		hydroEngineTmp.ReynoldStresses = np.ones(pM.n_z) * 0.0
		hydroEngineTmp.turbulentFluctuation()
		hydroEngineTmp.averageProfile()
		vxPart = []
		for v in hydroEngine.vPart:
			vxPart.append(v[0])
		return [[i * pF.dz for i in range(pM.n_z)], hydroEngineTmp.phiPart, vxPart, hydroEngineTmp.vxFluid[0:-1]]

#############################################################################################
#############################################################################################

def getMaxVel():
	"""Returns the current max velocity value of the dynamic objects as a Vector3
	
	"""
	maxVel = Vector3(0,0,0)
	for body in O.bodies :
		if body.dynamic == True and not body.isClump and body.state.vel.norm > maxVel.norm:
			maxVel = body.state.vel
	return maxVel

#############################################################################################
#############################################################################################

def _getMaxPos(i):
	"""Returns the current max of th i component of the position of the dynamic objects as a float
	
	"""
	max_i = None
	for body in O.bodies :
		if max_i == None or (body.dynamic == True and not body.isClump and body.state.pos[i] > max_i):
			max_i = body.state.pos[i]
	return max_i

#############################################################################################
#############################################################################################

def getMaxX():
	"""Returns the current max x position value of the dynamic objects as a float
	
	"""
	return _getMaxPos(0)

#############################################################################################
#############################################################################################

def getMaxY():
	"""Returns the current max y position value of the dynamic objects as a float
	
	"""
	return _getMaxPos(1)

#############################################################################################
#############################################################################################

def getMaxZ():
	"""Returns the current max y position value of the dynamic objects as a float
	
	"""
	return _getMaxPos(2)

#############################################################################################
#############################################################################################

def getObjPos(idObject):
	"""Returns the total current applied force on an object
	
	Parameter:
	- idObject -- The id of the object
	
	"""
	return O.bodies[idObject].state.pos

#############################################################################################
#############################################################################################

def getObjForce(idObject):
	"""Returns the total current applied force on an object
	
	Parameter:
	- idObject -- The id of the object
	
	"""
	vect = Vector3(0,0,0)
	for intr in O.bodies[idObject].intrs():
		vect += intr.phys.normalForce
		vect += intr.phys.shearForce
	return vect
