 #########################################################################################################################################################################
# Author : Remi Monthiller, remi.monthiller@etu.enseeiht.fr
# Adapted from the code of Raphael Maurin, raphael.maurin@imft.fr
# 30/10/2018
#
# Incline plane simulations
#
#########################################################################################################################################################################

# Import files
execfile("framework.py")
execfile("../common/pyRunMeasures.py")

####################################################################################################################################
####################################################  DATA LOGGING  #########################################################
####################################################################################################################################

logExecs=[]
def resetLogs():
	global logExecs
	for [f, evalfunc] in logExecs:
		f.close()
	logExecs=[]

def addLogData(fileName,evalfunc):
	"""Creates a new log file and prepare to store values returned by execfunc during the simulation. 
	
	Parameters:
	- fileName  -- name of the log file
	- execfunc  -- python expression to evaluate and so that its result will be stored
	
	"""
	try:
		# Create data Directory
		os.mkdir('data')
	except:
		pass
	f = open('data/'+fileName,"w")
	logExecs.append([f, evalfunc])
	
def logData():
	"""Loggs the data.
	
	"""
	for [f, evalfunc] in logExecs:
		f.write(str(eval(evalfunc)))
		f.write("\n")

####################################################################################################################################
####################################################  SIMULATION DEFINITION  #########################################################
####################################################################################################################################

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
	engineCreation()
	O.saveTmp() # User can reload simulation

#############################################################################################
#############################################################################################

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
	engineCreation()
	O.run() # Run the simulation
	O.wait()

#############################################################################################
#############################################################################################

def engineCreation():
	"""Creates the engine.
	
	Parameters:
	- idsToRemove -- the ids (as an list) of the objects you want to remove after 1 sec of simulation.
	
	"""
	######################################################################################
	### Simulation loop
	######################################################################################
	
	O.engines = [
		### Reset the forces
		ForceResetter(),
		### Detect the potential contacts
		InsertionSortCollider(
			[Bo1_Sphere_Aabb(), Bo1_Wall_Aabb(), Bo1_Facet_Aabb(), Bo1_Box_Aabb()],
			label='contactDetection',
			allowBiggerThanPeriod = True
			),
		### Calculate the different interactions
		InteractionLoop(
			[Ig2_Sphere_Sphere_ScGeom(), Ig2_Box_Sphere_ScGeom(),Ig2_Facet_Sphere_ScGeom()],
			[Ip2_ViscElMat_ViscElMat_ViscElPhys()],
			[Law2_ScGeom_ViscElPhys_Basic()],
			label = 'interactionLoop'
			),
		### inSimulationUtils Calls
		PyRunner(command='logData()', virtPeriod = 0.01, label = 'logs'),
		PyRunner(command='exitWhenFinished()', virtPeriod = 0.1, label = 'exit'),
		### GlobalStiffnessTimeStepper, determine the time step for a stable integration
		GlobalStiffnessTimeStepper(defaultDt=1e-4, viscEl=True, timestepSafetyCoefficient=0.7, label='GSTS'),
		### Integrate the equation and calculate the new position/velocities...
		NewtonIntegrator(gravity=g, label='newtonIntegr')
		]
	
	logs.dead = False
	exit.dead = False

####################################################################################################################################
#################################################### USEFUL PYRUNNERS  #########################################################
####################################################################################################################################

def exitWhenFinished():
	if(O.time > t_max):
		logFile.write("Simulation time, " + str(t_max) +  "s, elapsed.\nEnd of simulation.")
		logFile.write("\n")
		O.pause()
		logs.dead = True
		exit.dead = True
	else:
		logFile.write("Simulation time progress: " + str(int(100.0 * O.time/t_max)) + "%")
		logFile.write("\n")
