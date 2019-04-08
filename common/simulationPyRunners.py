def exitWhenFinished():
	if(O.time > t_max):
		O.pause()
		exit.dead = True
		save.dead = True
