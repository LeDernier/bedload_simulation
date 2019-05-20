
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
			print(body.state.refOri)
			rot = body.state.rot()
			rotx.append(math.fmod(2*math.pi + rot[0], 2*math.pi))
			roty.append(math.fmod(2*math.pi + rot[1], 2*math.pi))
			rotz.append(math.fmod(2*math.pi + rot[2], 2*math.pi))
	binsNb = 20
	rotx, bins = np.histogram(rotx, bins=binsNb, normed=False)
	roty, bins = np.histogram(roty, bins=binsNb, normed=False)
	rotz, bins = np.histogram(rotz, bins=binsNb, normed=False)
	bin_centers = 0.5*(bins[1:] + bins[:-1])
	return [bin_centers, rotx, roty, rotz]

#############################################################################################
#############################################################################################

def getOrientationHist():
	rotx = []
	roty = []
	rotz = []
	for body in O.bodies :
		if body.dynamic == True and body.isClump:
			u = body.state.ori * Vector3(1.0, 0.0, 0.0)
			u_yOz = Vector3(0, u[1], u[2])
			u_xOz = Vector3(u[0], 0, u[2])
			u_xOy = Vector3(u[0], u[1], 0)
			rotx.append(math.acos(u.dot(u_yOz)/(u.norm() * u_yOz.norm())))
			roty.append(math.acos(u.dot(u_xOz)/(u.norm() * u_xOz.norm())))
			rotz.append(math.acos(u.dot(u_xOy)/(u.norm() * u_xOy.norm())))
	binsNb = 20
	rotx, bins = np.histogram(rotx, bins=binsNb, normed=False)
	roty, bins = np.histogram(roty, bins=binsNb, normed=False)
	rotz, bins = np.histogram(rotz, bins=binsNb, normed=False)
	bin_centers = 0.5*(bins[1:] + bins[:-1])
	return [bin_centers, rotx, roty, rotz]

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
		return [[i * pF.dz for i in range(pM.n_z)], hydroEngine.phiPart, hydroEngine.vxPart, hydroEngine.vxFluid[0:-1]]
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
				vxPart = pP.vx, ids = partsIds, label = 'hydroEngine', dead = True)
		hydroEngineTmp.ReynoldStresses = np.ones(pM.n_z) * 0.0
		hydroEngineTmp.turbulentFluctuation()
		hydroEngineTmp.averageProfile()
		return [[i * pF.dz for i in range(pM.n_z)], hydroEngineTmp.phiPart, hydroEngineTmp.vxPart, hydroEngineTmp.vxFluid[0:-1]]

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
