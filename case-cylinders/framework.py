execfile("../common/frameworkCreationUtils.py")

### Useful ids
ids = {}

def frameworkCreation():
	"""Creates the framework and returns [idHouse, [idWallFront, idWallLeft, idWallRight]], ids of some of the objects created in O.bodies.
	
	Parameters:
	- [diameterPart, densPart, phiPartMax, restitCoef, partFrictAngle] -- parameters relative to the particles
	
	"""
	## Estimated max particle pressure from the static load
	p_max = -(pP.rho - pF.rho) * pP.phi_max * pP.n_l * pP.d * pM.g[2]
	
	## Evaluate the minimal normal stiffness to be in the rigid particle limit (cf Roux and Combe 2002)
	N_s = p_max * pP.d * 1.0e4
	## Young modulus of the particles from the stiffness wanted.
	E = N_s / pP.d
	## Poisson's ratio of the particles. Classical values, does not have much influence.
	nu = 0.5
	## Finaly difining material
	# O.materials.append(ViscElMat(en=pP.c_r, et=0., young=E, poisson=nu, density=pP.rho, frictionAngle=pP.mu, label='mat')) 
	O.materials.append(FrictMat(young=E, poisson=nu, density=pP.rho, frictionAngle=pP.mu, label='mat'))  

	#### Create cylinder materials ###
	# material to create the gridConnections
	O.materials.append(CohFrictMat(young=E, poisson=nu, density=pP.rho, frictionAngle=pP.mu, normalCohesion=1e10, shearCohesion=1e10, momentRotationLaw=True, label='cMat'))
	# material for general interactions
	O.materials.append(FrictMat(young=E, poisson=nu, density=pP.rho, frictionAngle=pP.mu, label='fMat'))  

	######################################################################################
	### Framework creation
	######################################################################################

	frCrea.createPeriodicCell()
	#frCrea.createGround()
	frCrea.createRugosity()
	#frCrea.createParticles()
	#frCrea.createClumpCloud()
	frCrea.createCylinderCloud()
	#frCrea.createDisplayG()
	#frCrea.createDisplayFluidHeight()

	f = open('.ids','w')
	f.write(str(ids))
	f.close()
