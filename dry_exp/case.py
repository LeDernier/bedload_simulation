#########################################################################################################################################################################
# Author : Remi Monthiller, remi.monthiller@etu.enseeiht.fr
# Adapted from the code of Raphael Maurin, raphael.maurin@imft.fr
# 30/10/2018
#
# Incline plane simulations
#
#########################################################################################################################################################################

# import lib
import matplotlib.pyplot as plt

# import simulation
execfile('params.py')
execfile('framework.py')
execfile('../common/simulationDefinition.py')

O.saveTmp() # Saves a "nothing" state

for d in [1.0*d_tetra, 1.5*d_tetra, 2*d_tetra, 4*d_tetra, 8*d_tetra]:
	print("Start simulation for d = " + str(d/d_tetra) + "*d_tetra")
	# Compute radius again
	r = d/2.0
	# Set number of particles
	n = 1e-4/pow(d, 3.0)
	n_l = n / (l*w/(d*d))
	n_ll = n / (l*w/(1.2*d*1.2*d))
	print("Computing with " + str(n) + " particles.")
	# Reset data to log
	resetLogs()
	# Add data to store
	addLogData(str(d)+"_"+"time.dat","O.time") # Store time
	addLogData(str(d)+"_"+"tetra_pos.dat","getObjPos(usefulIds['tetra'])")
	addLogData(str(d)+"_"+"max_z.dat","getMaxZ()")
	addLogData(str(d)+"_"+"mean_vel.dat","getMeanVel()")
	# LaunchSimulation
	iterNb = int(1e5)
	#simulation()
	simulationWait(iterNb)
