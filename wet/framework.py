execfile("../common/frameworkCreationUtils.py")

### Useful ids
ids = {}

def frameworkCreation():
	"""Creates the framework and returns [idHouse, [idWallFront, idWallLeft, idWallRight]], ids of some of the objects created in O.bodies.
	
	Parameters:
	- [diameterPart, densPart, phiPartMax, restitCoef, partFrictAngle] -- parameters relative to the particles
	
	"""
	## Estimated max particle pressure from the static load
	p_max = -(pP.rho - pF.rho) * pP.phi_max * pM.n_l * pP.d * pM.g[2]
	
	## Evaluate the minimal normal stiffness to be in the rigid particle limit (cf Roux and Combe 2002)
	N_s = p_max * pP.d * 1.0e4
	## Young modulus of the particles from the stiffness wanted.
	E = N_s / pP.d
	## Poisson's ratio of the particles. Classical values, does not have much influence.
	nu = 0.5
	## Finaly difining material
	O.materials.append(ViscElMat(en=pP.c_r, et=0., young=E, poisson=nu, density=pP.rho, frictionAngle=pP.mu, label='mat')) 

	######################################################################################
	### Framework creation
	######################################################################################

	frCrea.createPeriodicCell()
	frCrea.createGround()
	frCrea.createParticles()
	(idTetra, [idS_1, idS_2, idS_3, idS_4]) = frCrea.addTetra(center = Vector3(pM.l/2.0, pM.w/2.0, pM.h/3.0 + pM.n_ll*pP.d*1.2/2.0), d=pS.d_tetra, l=pS.d_tetra/2.0)
	
	ids["tetra"] = idTetra
	ids["s_1"] = idS_1
	ids["s_2"] = idS_2
	ids["s_3"] = idS_3
	ids["s_4"] = idS_4

	f = open('.ids','w')
	f.write(str(ids))
	f.close()
