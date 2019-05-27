class pyRuns:
	@staticmethod
	def exitWhenFinished():
		if(O.time > pN.t_max):
			print("INFO: Simulation finished at time : " + str(O.time))
			O.pause()

	count = 0
	@staticmethod
	def solveFluid():
		if O.time < pF.solve_begin_time:
			return
		elif pyRuns.count < 1 and O.time < pSave.yadeSavePeriod:
			print("INFO: Starting to apply fluid.\n")
			pyRuns.count = 1
			hydroEngine.dead = False
			hydroEngine.newAverageProfile()
			hydroEngine.newFluidResolution(1., pF.dt)
		# Computes average vx, vy, vz, phi, drag profiles
		hydroEngine.newAverageProfile()
		hydroEngine.newFluidResolution(pF.t, pF.dt)
	
	@staticmethod
	def shaker():
		if O.time > pN.shake_time:
			shaker.dead = True
			return
		else:
			pyRuns.shake(pN.shake_intensity)

	@staticmethod
	def shake(X = 0.1):
		for b in O.bodies:
			rx = random.uniform(-X,X)
			ry = random.uniform(-X,X)
			rz = random.uniform(-X,X)
			if b.dynamic:
				b.state.vel[0] += rx
				b.state.vel[1] += ry
				b.state.vel[2] += rz
	
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
