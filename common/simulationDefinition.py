 #########################################################################################################################################################################
# Author : Remi Monthiller, remi.monthiller@etu.enseeiht.fr
# Adapted from the code of Raphael Maurin, raphael.maurin@imft.fr
# 30/10/2018
#
# Incline plane simulations
#
#########################################################################################################################################################################

execfile("../common/simulationPyRunners.py")

class sim: # Simulation
	####################################################################################################################################
	####################################################  SIMULATION DEFINITION  #########################################################
	####################################################################################################################################
	@staticmethod
	def simulation():
		"""Creates a simulation.
		
		Parameters:
		- [diameterPart, densPart, phiPartMax, restitCoef, partFrictAngle] -- parameters relative to the particles
		- [number, lengthBox, widthBox, heightBox]                         -- parameters relative to the particle cloud
		- [normalStiffness, youngMod, poissonRatio]                        -- parameters relative to the particles' material
		- [slopeChannel, lengthChannel, widthChannel, heightChannel]       -- parameters relative to the channel
		- [positionCoef, angleHouse, lengthHouse, widthHouse, heightHouse] -- parameters relative to the house
		
		"""
		frameworkCreation()
		sim.engineCreation()
		O.saveTmp() # User can reload simulation
	
	#############################################################################################
	#############################################################################################
	@staticmethod
	def simulationWait():
		"""Creates a simulation, runs it and wait until its finished.
		
		Parameters:
		- [diameterPart, densPart, phiPartMax, restitCoef, partFrictAngle] -- parameters relative to the particles
		- [number, lengthBox, widthBox, heightBox]                         -- parameters relative to the particle cloud
		- [normalStiffness, youngMod, poissonRatio]                        -- parameters relative to the particles' material
		- [slopeChannel, lengthChannel, widthChannel, heightChannel]       -- parameters relative to the channel
		- [positionCoef, angleHouse, lengthHouse, widthHouse, heightHouse] -- parameters relative to the house
		
		"""
		O.reset()
		frameworkCreation()
		sim.engineCreation()
		O.run() # Run the simulation
		O.wait()
	
	#############################################################################################
	#############################################################################################
	@staticmethod
	def engineCreation():
		"""Creates the engine.
		
		Parameters:
		- idsToRemove -- the ids (as an list) of the objects you want to remove after 1 sec of simulation.
		
		"""
		######################################################################################
		### Simulation loop
		######################################################################################
		engines = []
		### Reset the forces
		engines.append(
				ForceResetter()
				)
		### Detect the potential contacts
		engines.append(
				InsertionSortCollider(
					[Bo1_Sphere_Aabb(), Bo1_Wall_Aabb(), Bo1_Facet_Aabb(), Bo1_Box_Aabb()],
					label='contactDetection',
					allowBiggerThanPeriod = True
					)
				)
		### Calculate different interactions
		engines.append(
				InteractionLoop(
					[Ig2_Sphere_Sphere_ScGeom(), Ig2_Box_Sphere_ScGeom(),Ig2_Facet_Sphere_ScGeom()],
					[Ip2_ViscElMat_ViscElMat_ViscElPhys()],
					[Law2_ScGeom_ViscElPhys_Basic()],
					label = 'interactionLoop'
					)
				)
		#### Apply hydrodynamics
		### Apply an hydrodynamic force to the particles
		# TODO : define vxFluid, phiPart, vxPart, ids
		# TODO : deal with dead = True
		if pF.enable:
			engines.append(
					HydroForceEngine(
						densFluid = pF.rho, viscoDyn = pF.nu * pF.rho, zRef = pM.z_ground, 
						gravity = pM.g, deltaZ = pF.dz, expoRZ = pP.expoDrag, 
						lift = False, nCell = pF.n_z, vCell = pM.l*pM.w*pF.dz, 
						radiusPart=pP.r, vxFluid = np.array(vxFluidPY), phiPart = phiPartPY, 
						vxPart = vxPartPY, ids = idApplyForce, label = 'hydroEngine')
					)
			### Fluid resolution
			# TODO : deal with dead = True
			engines.append(
					PyRunner(command='pyRuns.solveFluid()', virtPeriod = t_f, label = 'fluidSolve')
					)
		### GlobalStiffnessTimeStepper, determine the time step for a stable integration
		engines.append(
				GlobalStiffnessTimeStepper(defaultDt=1e-4, viscEl=True, timestepSafetyCoefficient=0.7, label='GSTS')
				)
		### Integrate the equation and calculate the new position/velocities...
		engines.append(
				NewtonIntegrator(gravity=pM.g, label='newtonIntegr')
				)
		### PyRunner Calls
		engines.append(
				PyRunner(command='pyRuns.exitWhenFinished()', virtPeriod = 0.1, label = 'exit')
				)
		if pSave.yadeSavePeriod:
			engines.append(
				PyRunner(command='O.save("data/"+str(O.time)+".yade")', virtPeriod = pSave.yadeSavePeriod, label = 'save')
				)
		### Recorder
		# TODO : Remove or as an option :
		engines.append(
			VTKRecorder(iterPeriod=10,recorders=['spheres', 'velocity', 'force', 'stress'],fileName='/tmp/rsim-')
			)
		O.engines = engines
