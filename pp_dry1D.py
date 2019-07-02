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
	mean_begin_time = 10.0
	mean_end_time = 50.0
	#-------------------#
	# Plot visuals
	#-------------------#
	r = [0.0, 0.5]
	v = [0.5, 0.0]
	b = [0.5, 0.0]
	markers = ["$\mathbf{H}$", "$\mathbf{G}$", "$\mathbf{F}$", "$\mathbf{E}$", "$\mathbf{D}$", "$\mathbf{C}$", "$\mathbf{B}$", "$\mathbf{A}$", "d", "*", "s", "v", "o"]
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
			"qs":r"${Q_s}$",
			"z":r"$z$",
			"time":r"$t$ (s)",
			"mean_z_phi":r"$\phi_{max}$",
			"var_z_phi":r"$\sigma_\phi$",
			"alpha":r"$\alpha$",
			}
	# Plot params
	name_case = "dry"
	param = "pP.A"
	name_param = "A"

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
			"z":"[z for z in data['mean_profiles'][0]]",
			"mean_phi":"data['mean_profiles'][1]",
			"mean_vx":"data['mean_profiles'][2]", 
			},
			{
			# Flows
			"mean_qsx":"[data['mean_phi'][i] * data['mean_vx'][i] for i in range(len(data['mean_phi']))]",
			"qs":"[integration(data['phi'][i], data['vx'][i], pF.dz) for i in range(len(data['profiles']))]",
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
#			"vx":[[], [4, 18]],
#			"qsx":[[], [4, 18]],
#			"phi":[[], [4, 18]],
#			"qs":[[], []],
			}
	plots = {
			"vx":[["mean_vx"], ["z"]],
			"qsx":[["mean_qsx"], ["z"]],
			"phi":[["mean_phi"], ["z"]],
			"qs":[["time"], ["qs"]],
			}
	plotsT = {
#			"vx":[["vx"], ["z"], 20.0],
			}
	plotsExtPath = {
			}
	plotsExt = {
			}
	alimsO = {
			
			}
	orientations = {
			}

class pP2D:
	plot_enable = False
	# Measuring 2D data in the 1D data
	measures = {
			}
	post_process = []
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
