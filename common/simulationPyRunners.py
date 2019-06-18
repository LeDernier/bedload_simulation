class pyRuns:
	@staticmethod
	def exitWhenFinished():
		if(O.time > pN.t_max):
			print("INFO: Simulation finished at time : " + str(O.time))
			O.pause()

	@staticmethod
	def save():
		if pF.enable:
			if pF.method == "new":
				hydroEngine.newAverageProfile()
			elif pF.method == "old":
				hydroEngine.averageProfile()
		O.save("data/"+str(O.time)+".yade")

	count = 0
	@staticmethod
	def solveFluid():
		if O.time < pF.solve_begin_time:
			return
		elif pyRuns.count < 1 and O.time < pSave.yadeSavePeriod:
			print("INFO: Starting to apply fluid.\n")
			pyRuns.count = 1
			hydroEngine.dead = False
			if pF.method == "new":
				hydroEngine.newAverageProfile()
				hydroEngine.newFluidResolution(1., pF.dt)
			elif pF.method == "old":
				hydroEngine.averageProfile()
				hydroEngine.fluidResolution(1., pF.dt)
		# Computes average vx, vy, vz, phi, drag profiles
		if pF.method == "new":
			hydroEngine.newAverageProfile()
			hydroEngine.newFluidResolution(pF.t, pF.dt)
		elif pF.method == "old":
			hydroEngine.averageProfile()
			hydroEngine.fluidResolution(pF.t, pF.dt)
	
	@staticmethod
	def computeTurbulentFluctuations():
		if O.time < pF.solve_begin_time:
			return
		# Computes average vx, vy, vz, phi, drag profiles
		if pF.method == "new" or pF.method == "old":
			### Evaluate nBed, the position of the bed which is assumed to be located around the first maximum of concentration when considering decreasing z.
			phi = hydroEngine.phiPart
			nBed = pN.n_z - 2
			while nBed > 0 and not(phi[nBed] < phi[nBed-1] and phi[nBed] > 0.5):
				# If there is a peak and its value is superior to 0.5, 
				# we consider it to be the position of the bed
				nBed -= 1
			waterDepth = (pN.n_z-1 - nBed) * pF.dz
			### Evaluate the bed elevation for the following
			bedElevation = pF.h - waterDepth
			### (Re)Define the bed elevation over which fluid turbulent fluctuations will be applied.
			hydroEngine.bedElevation = bedElevation
			### Impose a unique constant lifetime for the turbulent fluctuation, flucTimeScale
			# Fluid velocity scale in the water depth
			vMeanAboveBed = sum(hydroEngine.vxFluid[nBed:])/(pN.n_z - nBed)
			# TODO : Very stange that it can be 0
			if vMeanAboveBed > 0:
				flucTimeScale = waterDepth/vMeanAboveBed	# time scale of the fluctuation w_d/v, eddy turn over time
				# New evaluation of the random fluid velocity fluctuation for each particle. 
				hydroEngine.turbulentFluctuation() 
				# Actualize when will be calculated the next fluctuations. 
				turbFluct.virtPeriod = flucTimeScale 
	
	shaker_vel = 0.0
	@staticmethod
	def shaker():
		old_shaker_vel = pyRuns.shaker_vel
		pyRuns.shaker_vel = 2.0*pi * pM.shake_f * 0.5*pM.shake_a * sin(O.time * 2.0*pi * pM.shake_f)
		if O.time > pM.shake_time and np.sign(old_shaker_vel) != np.sign(pyRuns.shaker_vel):
			shaker.dead = True
			for b in O.bodies:
				if not b.dynamic:
					b.state.vel[2] = 0.0
		else:
			for b in O.bodies:
				if not b.dynamic:
					b.state.vel[2] = pyRuns.shaker_vel
	
	fluidDisplayIds = []
	@staticmethod
	def updateFluidDisplay():
		if len(yade.qt.views()) > 0:
			# Managing Renderer
			renderer = yade.qt._GLViewer.Renderer()
			renderer.ghosts = False
			# Drawing profile
			dz = (pF.z-pM.z_ground)/pF.display_n
			nn = pN.n_z/pF.display_n
			vx = []
			vmax = 0.001
			for i in pyRuns.fluidDisplayIds:
				O.bodies.erase(i)
			mult = 0.0
			for i in range(pF.display_n):
				vx.append(0.0)
				for j in range(nn):
					vx[i] += hydroEngine.vxFluid[i * nn + j]
				vx[i] /= nn
				if vx[i] > vmax:
					vmax = vx[i]
			if pF.display_mult == 0.0:
				mult = (pM.l-pP.S)/vmax
			else:
				mult = pF.display_mult
			for i in range(pF.display_n):
				z = pM.z_ground + i * dz
				b = 1.0 - vx[i]/vmax
				v = 0.5
				r = 1.0 - b
				pyRuns.fluidDisplayIds.append(
						frCrea.createBox(
							center = (max(pM.l/100.0, vx[i] * mult/2.0), pM.w/2.0, z),
							extents = (max(pM.l/100.0, vx[i] * mult/2.0), pM.w * 0.6, dz/2.0),
							color = (r, v, b),
							wire = True,
							mask = 0
							)
						)
		else:
			for i in pyRuns.fluidDisplayIds:
				O.bodies.erase(i)
			#fluidDisplay.dead = True
