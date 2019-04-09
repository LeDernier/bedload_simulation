execfile("../common/frameworkCreationUtils.py")

### Useful ids
ids = {}

def frameworkCreation():
	"""Creates the framework and returns [idHouse, [idWallFront, idWallLeft, idWallRight]], ids of some of the objects created in O.bodies.
	
	Parameters:
	- [diameterPart, densPart, phiPartMax, restitCoef, partFrictAngle] -- parameters relative to the particles
	
	"""
	## Estimated max particle pressure from the static load
	p_max = -(rho_p - rho_f) * phi_max * n_l * d * g[2]
	
	## Evaluate the minimal normal stiffness to be in the rigid particle limit (cf Roux and Combe 2002)
	N_s = p_max * d * 1.0e4
	## Young modulus of the particles from the stiffness wanted.
	E = N_s / d
	## Poisson's ratio of the particles. Classical values, does not have much influence.
	nu = 0.5
	## Finaly difining material
	O.materials.append(ViscElMat(en=c_r, et=0., young=E, poisson=nu, density=rho_p, frictionAngle=mu, label='mat')) 

	######################################################################################
	### Framework creation
	######################################################################################

	createPeriodicSlope()
	createParticles()
#	(idTetra, [idS_1, idS_2, idS_3, idS_4]) = addTetra(center = Vector3(l/2.0, w/2.0, h/3.0 + n_ll*d*1.2/2.0), d=d_tetra, l=d_tetra/2.0)
#	
#	ids["tetra"] = idTetra
#	ids["s_1"] = idS_1
#	ids["s_2"] = idS_2
#	ids["s_3"] = idS_3
#	ids["s_4"] = idS_4

	f = open('.ids','w')
	f.write(str(ids))
	f.close()
