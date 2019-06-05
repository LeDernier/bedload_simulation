execfile("../common/frameworkCreationUtils.py")

### Useful ids
ids = {}

def frameworkCreation():
	"""Creates the framework
	
	"""

	######################################################################################
	### Framework creation
	######################################################################################

	frCrea.defineMaterials()
	frCrea.createPeriodicCell()
	#frCrea.createGround()
	frCrea.createRugosity()
	#frCrea.createParticles()
	frCrea.createClumpCloud()
	#frCrea.createDisplayG()
	#frCrea.createDisplayFluidHeight()
	
	f = open('.ids','w')
	f.write(str(ids))
	f.close()
