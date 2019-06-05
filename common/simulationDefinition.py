 #########################################################################################################################################################################
# Author : Remi Monthiller, remi.monthiller@etu.enseeiht.fr
# Adapted from the code of Raphael Maurin, raphael.maurin@imft.fr
# 30/10/2018
#
# Incline plane simulations
#
#########################################################################################################################################################################

import numpy as np

class sim: # Simulation
	@staticmethod
	def simulation():
		"""Creates a simulation.
		
		"""
		sim.engineCreation()
		frameworkCreation()
		sim.init()
		# Save tmp so that the user can reload the simulation. 
		O.saveTmp() 

	@staticmethod
	def init():
		""" Initialise the simulation.

		"""
		### Initialisation of fluid
		if pF.enable:
			partsIds = []
			for i in range(len(O.bodies)):
				b = O.bodies[i]
				if not b.isClump:
					partsIds.append(i)
			hydroEngine.ids = partsIds
			hydroEngine.ReynoldStresses = np.ones(pN.n_z) * 0.0
			hydroEngine.turbulentFluctuation()

	####---------------####
	#### Engines Def 
	####---------------####
	
	@staticmethod
	def cylinderContactDetectionCreation(engines):
		""" Add to the engines the engine necessary to cylinder contact detection.
		
		"""
		### Detect the potential contacts
		engines.append(
				InsertionSortCollider(
					[Bo1_GridConnection_Aabb(), Bo1_Sphere_Aabb()],
					label='contactDetection',
					allowBiggerThanPeriod = True
					)
				)

	@staticmethod
	def sphereContactDetectionCreation(engines):
		""" Add to the engines the engine necessary to sphere contact detection.
		
		"""
		### Detect the potential contacts
		engines.append(
				InsertionSortCollider(
					[Bo1_Sphere_Aabb(), Bo1_Box_Aabb()],
					label='contactDetection',
					allowBiggerThanPeriod = True
					)
				)

	@staticmethod
	def cylinderInteractionsCreation(engines):
		""" Add to the engines the engine necessary to the cylinder interactions.
		
		"""
		### Calculate different interactions
		engines.append(
				InteractionLoop(
					[      
						# Sphere interactions
						Ig2_Sphere_Sphere_ScGeom(),
						# Sphere-Cylinder interactions
						Ig2_Sphere_GridConnection_ScGridCoGeom(),
						# Cylinder interactions 
						Ig2_GridNode_GridNode_GridNodeGeom6D(),
						# Cylinder-Cylinder interaction :
						Ig2_GridConnection_GridConnection_GridCoGridCoGeom(),
					],
					[
						# Internal Cylinder Physics
						Ip2_CohFrictMat_CohFrictMat_CohFrictPhys(setCohesionNow=True,setCohesionOnNewContacts=False),
						# Physics for External Interactions (cylinder-cylinder)
						Ip2_FrictMat_FrictMat_FrictPhys()
					],
					[
						# Contact law for sphere-sphere interactions
						Law2_ScGeom_FrictPhys_CundallStrack(),
						# Contact law for cylinder-sphere interactions
						Law2_ScGridCoGeom_FrictPhys_CundallStrack(),
						# Contact law for "internal" cylider forces :
						Law2_ScGeom6D_CohFrictPhys_CohesionMoment(),
						# Contact law for cylinder-cylinder interaction :
						Law2_GridCoGridCoGeom_FrictPhys_CundallStrack()
					],
					label = 'interactionLoop'
					)
				)

	@staticmethod
	def sphereInteractionsCreation(engines):
		""" Add to the engines the engine necessary to the sphere interactions.
		
		"""
		engines.append(
				InteractionLoop(
					[Ig2_Sphere_Sphere_ScGeom(), Ig2_Box_Sphere_ScGeom()],
					[Ip2_ViscElMat_ViscElMat_ViscElPhys()],
					[Law2_ScGeom_ViscElPhys_Basic()],
					label = 'interactionLoop'
					)
				)

	####---------------####
	#### Hydro engine 
	####---------------####
	
	@staticmethod
	def hydroEngineCreation(engines):
		""" Add to the engines the engine necessary to the application of hydrodynamic forces.
		
		"""
		# Creating Hydro Engine
		if pF.method == "new":
			engines.append(
					HydroForceEngine(
						densFluid = pF.rho, viscoDyn = pF.nu * pF.rho, zRef = pM.z_ground, 
						gravity = pM.g, deltaZ = pF.dz, expoRZ = pF.expoDrag, 
						lift = False, nCell = pN.n_z, vCell = pM.l * pM.w * pF.dz, 
						phiPart = pP.phi, vxFluid = pF.vx, vPart = pP.v, ids = [],
						fluidWallFriction = pF.enable_wall_friction,
						dead = True, label = 'hydroEngine')
					)
		elif pF.method == "old":
			engines.append(
					HydroForceEngine(
						densFluid = pF.rho, viscoDyn = pF.nu * pF.rho, zRef = pM.z_ground, 
						gravity = pM.g, deltaZ = pF.dz, expoRZ = pF.expoDrag, 
						lift = False, nCell = pN.n_z, vCell = pM.l * pM.w * pF.dz, 
						radiusPart = pP.S/2.0, phiPart = pP.phi, 
						vxFluid = pF.vx, vxPart = [0.0] * (pN.n_z-1), ids = [],
						wallFriction = pF.enable_wall_friction,
						dead = True, label = 'hydroEngine')
					)
		# Fluid resolution
		if pF.solve:
			engines.append(
					PyRunner(command='pyRuns.solveFluid()', virtPeriod = pF.t, label = 'fluidSolve')
					)
		# Turbulent fluctuations
		if pF.enable_fluctuations:
			engines.append(
					PyRunner(command='pyRuns.computeTurbulentFluctuations()', virtPeriod = pF.t_fluct, label = 'turbFluct')
					)
		# Display fluid velocity profile
		if pF.display_enable:
			engines.append(
					PyRunner(command='pyRuns.updateFluidDisplay()', virtPeriod = pF.t, label = 'fluidDisplay')
					)

	####---------------####
	#### Engines Creation 
	####---------------####
	
	@staticmethod
	def engineCreation():
		"""Creates the engine.
		
		"""
		engines = []
		### Reset the forces
		engines.append(
				ForceResetter()
				)
		### Detect the potential contacts
		if pP.kind == "cylinder":
			sim.cylinderContactDetectionCreation(engines)
		else:
			sim.sphereContactDetectionCreation(engines)
		### Calculate different interactions
		if pP.kind == "cylinder":
			sim.cylinderinteractionsCreation(engines)
		else:
			sim.sphereInteractionsCreation(engines)
		#### Apply hydrodynamic forces
		if pF.enable:
			sim.hydroEngineCreation(engines)
		### GlobalStiffnessTimeStepper, determine the time step for a stable integration
		engines.append(
				GlobalStiffnessTimeStepper(defaultDt=1e-4, viscEl=True, timestepSafetyCoefficient=0.7, label='GSTS')
				)
		### Integrate the equation and calculate the new position/velocities...
		engines.append(
				NewtonIntegrator(damping=0.0, gravity=pM.g, label='newtonIntegr')
				)
		### PyRunner Calls
		# End of simulation
		engines.append(
				PyRunner(command='pyRuns.exitWhenFinished()', virtPeriod = 0.1, label = 'exit')
				)
		# Save data 
		if pSave.yadeSavePeriod:
			engines.append(
				PyRunner(command='O.save("data/"+str(O.time)+".xml")', virtPeriod = pSave.yadeSavePeriod, label = 'save')
				)
		# Shaker
		if pN.shake_enable:
			engines.append(
				PyRunner(command='pyRuns.shaker()', virtPeriod = pN.shake_period, label = 'shaker')
				)
		### Recorder
		if pSave.vtkRecorderIterPeriod > 0:
			engines.append(
				VTKRecorder(iterPeriod=pSave.vtkRecorderIterPeriod,recorders=['spheres', 'velocity', 'force', 'stress'],fileName='./vtk/sim-')
				)
		### Adding engines to Omega
		O.engines = engines

### Reading pyRunners
execfile("../common/simulationPyRunners.py")
