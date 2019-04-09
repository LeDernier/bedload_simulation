class pyRuns:
	def exitWhenFinished():
		if(O.time > t_max):
			O.pause()
	
	def solveFluid():
		# Fluid resolution
		hydroEngine.fluidResolution(fluidResolPeriod, dtFluid)
