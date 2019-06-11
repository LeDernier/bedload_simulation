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
	frCrea.createWalls()
#	frCrea.createGround()
	frCrea.createRugosity()
	frCrea.createParticles()
	
	f = open('.ids','w')
	f.write(str(ids))
	f.close()
