#-------------------#
# Setting latex
#-------------------#
plt.rc('text', usetex=True)
#-------------------#
# Setting Font
#-------------------#
font = {'family' : 'normal',
#        'weight' : 'bold',
        'size'   : 18}
plt.rc('font', **font)

# Basic plot parameters
class pPP:
	#-------------------#
	# Plot Names
	#-------------------#
	show_figs = False
	#-------------------#
	# Saving figures
	#-------------------#
	save_fig_dir = "/home/rmonthil/Documents/post_proc/"
	save_figs = True
	#-------------------#
	# Adimensionalisation
	#-------------------#
	d_ad = "pP.dvs"
	d_ad_name = "d_{vs}"
	#-------------------#
	# Mean operation 
	#-------------------#
	mean_begin_time = 50.0
	mean_end_time = 100.0
	#-------------------#
	# Plot visuals
	#-------------------#
	r = [0.0, 0.5]
	v = [0.5, 0.0]
	b = [0.5, 0.0]
	markers = ["$\mathbf{C}$", "$\mathbf{B}$", "$\mathbf{A}$", "d", "*", "s", "v", "o"]
	me = 0.05 
	mew = 0.3
	ms = 7.0
	#-------------------#
	# Plot Names
	#-------------------#
	plots_names = {
			"mean_phi":r"$\bar{\phi}$",
			"mean_vx":r"$\bar{U^p_x}$",
			"vx":r"${U^p_x}$",
			"mean_qsx":r"$\bar{Q_s}$",
			"shields":r"$\theta$",
			"z":r"$z^* =  \frac{z}{d}$",
			"time":r"$t$ (s)",
			}

# 1D plot parameters
class pP1D:
	plot_enable = True
	#-------------------#
	# Post Processing
	#-------------------#
	post_process = [
			{
			# Exporting profiles
			"phi":"[l[1] for l in data['profiles']]",
			"vx":"[l[2] for l in data['profiles']]",
			# Averaging
			"mean_profiles":"average_phi_u_profile(data['profiles'], data['time'])",
			},
			{
			# Adimentionalisation.
			"z":"[z/pP.S for z in data['mean_profiles'][0]]",
			"mean_phi":"data['mean_profiles'][1]",
			"mean_vx":"data['mean_profiles'][2]", 
			},
			{
			# Flows
			"mean_qsx":"[data['mean_phi'][i] * data['mean_vx'][i] for i in range(len(data['mean_phi']))]",
			}
			]
	#-------------------#
	# Plot Visuals
	#-------------------#
	r = pPP.r
	v = pPP.v
	b = pPP.b
	colors = []
	markers = pPP.markers[:]
	me = pPP.me
	mew = pPP.mew
	ms = pPP.ms
	#-------------------#
	# Plots
	#-------------------#
	alims = {
			"vx":[[], [4, 9]],
			"qsx":[[], [4, 9]],
			"phi":[[], [4, 9]],
			}
	plots = {
			"vx":[["mean_vx"], ["z"]],
			"qsx":[["mean_qsx"], ["z"]],
			"phi":[["mean_phi"], ["z"]],
			}
	plotsT = {
			}
	plotsExtPath = {
			"Experimental data: 14,\nFrey et al. 2014":"./exp-data/Frey2014_EXP14.py"
			}
	plotsExt = {
			"vx":[["vx"], ["z"]],
			"qsx":[["qsx"], ["z"]],
			"phi":[["phi"], ["z"]],
			}

class pP2D:
	plot_enable = False
	# Plot param
	param = "pP.A"
	param_name = "A"
	# Measuring 2D data in the 1D data
	measures = {
			}
	#-------------------#
	# Plot visuals
	#-------------------#
	r = pPP.r
	v = pPP.v
	b = pPP.b
	colors = []
	markers = pPP.markers[:]
	me = pPP.me
	mew = pPP.mew
	ms = pPP.ms
	#-------------------#
	# Plots
	#-------------------#
	plots = {
			}
