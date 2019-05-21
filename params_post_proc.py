
# Basic plot parameters
class pPP:
	#-------------------#
	# Saving figures
	#-------------------#
	save_fig_dir = "/home/rmonthil/Documents/post_proc/"
	save_figs = True
	#-------------------#
	# Adimensionalisation
	#-------------------#
	d_ad = "pS.vol/pS.surf"
	d_ad_name = "d_{vs}"
	#-------------------#
	# Mean operation 
	#-------------------#
	mean_begin_time = 200.0
	mean_end_time = 400.0
	#-------------------#
	# Plot visuals
	#-------------------#
	r = [0.0, 0.5]
	v = [0.5, 0.0]
	b = [0.5, 0.0]
	markers = ["$\mathbf{C}$", "$\mathbf{B}$", "$\mathbf{A}$", "d", "*", "s", "v", "o"]
	me = 0.005 
	mew = 0.3
	ms = 7.0
	#-------------------#
	# Plot Names
	#-------------------#
	plots_names = {
			"mean_phi":r"$\bar{\phi$}",
			"mean_vx":r"$\bar{U^p_x}^* = \frac{\bar{U^p_x}}{\sqrt{g"+pPP.d_ad_name+"}}$",
			"mean_vfx":r"$\bar{U^f_x}^* = \frac{\bar{U^p_x}}{\sqrt{g"+pPP.d_ad_name+"}}$",
			"qs":r"${Q_s}^*$",
			"qf":r"${Q_f}^*$",
			"shields":r"$\theta$",
			"z":r"$z^* =  \frac{z}{"+pPP.d_ad_name+"}$",
			"time":r"$t$ (s)",
			}

# 1D plot parameters
class pP1D:
	plot_enable = True
	#-------------------#
	# Measures
	#-------------------#
	measures = {
			"profiles":"getProfiles()",
			"shields":"getShields()",
			"rots":"getOrientationHist()",
			}
	#-------------------#
	# Post Processing
	#-------------------#
	# Time is dealt seperately but data['time'] can be accessed from here.
	post_process = {
			# Exporting profiles
			"phi":"[l[1] for l in data['profiles']]",
			"vx":"[adim(l[2], sqrt(pM.g[2] * d_ad)) for l in data['profiles']]",
			"vfx":"[adim(l[3], sqrt(pM.g[2] * d_ad)) for l in data['profiles']]",
			# Averaging
			"mean_profiles":"average_profile(data['profiles'])",
			"mean_rots":"average_profile(data['rots'], True)",
			# Adimentionalisation.
			"z":"[z/d_ad for z in data['mean_profiles'][0]]",
			"mean_phi":"data['mean_profiles'][1]",
			"mean_vx":"adim(data['mean_profiles'][2], sqrt(pM.g[2] * d_ad))", 
			"mean_vfx":"adim(data['mean_profiles'][3], sqrt(pM.g[2] * d_ad))",
			# Flows
			"qs":"[integration(data['phi'][i], data['vx'][i], data['z'][1]-data['z'][0]) for i in range(len(profiles))]",
			"qf":"[integration(data['phi'][i], data['vfx'][i], data['z'][1]-data['z'][0]) for i in range(len(profiles))]",
			}
	#-------------------#
	# Plot Visuals
	#-------------------#
	r = pPP.r
	v = pPP.v
	b = pPP.b
	markers = pPP.markers[:]
	me = pPP.me
	mew = pPP.mew
	ms = pPP.ms
	#-------------------#
	# Plots
	#-------------------#
	plots = {
			"vx":[["mean_vx"], ["z"]],
			"vfx":[["mean_vfx"], ["z"]],
			"phi":[["mean_phi"], ["z"]],
			"qs":[["time"], ["qs"]],
			"qf":[["time"], ["qf"]],
			"sh":[["time"], ["shields"]],
			}

class pP2D:
	plot_enable = False
	# Plot param
	param = "pS.A"
	param_name = "A"
	# Measuring 2D data in the 1D data
	measures = {
			"qs":"average(data['qs'])"
			"qf":"average(data['qf'])"
			"sh":"average(data['shields'])"
			}
	#-------------------#
	# Plot visuals
	#-------------------#
	r = pPP.r
	v = pPP.v
	b = pPP.b
	markers = pPP.markers[:]
	me = pPP.me
	mew = pPP.mew
	ms = pPP.ms
	#-------------------#
	# Plots
	#-------------------#
	plots = {
			"qs(qf)":[["qf"], ["qs"]],
			"qs(sh)":[["sh"], ["qs"]],
			}
